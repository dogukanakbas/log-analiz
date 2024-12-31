from typing import List, Dict
from datetime import datetime, timedelta
from collections import Counter
import pytz

class RAGModel:
    def __init__(self, model_name: str, vector_store):
        self.vector_store = vector_store
        
    def parse_log_time(self, time_str: str) -> datetime:
        """Log tarihini parse eder."""
        try:
            
            dt = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S %z')
            return dt
        except:
            return None
        
    def analyze_logs(self, logs: List[Dict]) -> dict:
        """Logları analiz eder ve istatistikleri çıkarır."""
        stats = {
            'total_requests': len(logs),
            'ip_counts': Counter(),
            'status_codes': Counter(),
            'recent_requests': 0,
            'unique_ips': set(),
            'error_counts': 0,
            'requests': Counter(),
            'methods': Counter(),  
            'paths': Counter(),    
            'hours': Counter(),    
        }
        
        now = datetime.now(pytz.UTC)
        one_hour_ago = now - timedelta(hours=1)
        
        for log in logs:
          
            ip = log.get('remote_addr', 'N/A')
            stats['ip_counts'][ip] += 1
            stats['unique_ips'].add(ip)
            
           
            status = log.get('status', 'N/A')
            stats['status_codes'][status] += 1
            if status.startswith('4') or status.startswith('5'):
                stats['error_counts'] += 1
            
         
            request = log.get('request', 'N/A')
            stats['requests'][request] += 1
            
           
            try:
                method, path, _ = request.split()
                stats['methods'][method] += 1
                stats['paths'][path] += 1
            except:
                pass
            
      
            log_time = self.parse_log_time(log.get('time_local', ''))
            if log_time:
                if log_time >= one_hour_ago:
                    stats['recent_requests'] += 1
                stats['hours'][log_time.hour] += 1
        
       
        stats['top_ips'] = stats['ip_counts'].most_common(5)
        stats['top_requests'] = stats['requests'].most_common(5)
        stats['top_paths'] = stats['paths'].most_common(5)
        stats['busiest_hours'] = stats['hours'].most_common(5)
        
        return stats

    def answer_question(self, question: str) -> str:
        """Kullanıcı sorusunu yanıtlar."""
        try:
      
            relevant_logs = self.vector_store.search(question, k=50)  
            stats = self.analyze_logs(relevant_logs)
            
            question_lower = question.lower()
            
            
            if "ip" in question_lower:
                if "en çok" in question_lower or "en fazla" in question_lower:
                    if stats['top_ips']:
                        top_ip, count = stats['top_ips'][0]
                        others = "\n".join([f"- {ip}: {c} istek" for ip, c in stats['top_ips'][1:]])
                        return f"En çok istek yapan IP: {top_ip} ({count} istek)\n\nDiğer aktif IP'ler:\n{others}"
                if "kaç" in question_lower or "sayısı" in question_lower:
                    return f"Toplam {len(stats['unique_ips'])} farklı IP adresi tespit edildi"
                return "IP istatistikleri:\n" + "\n".join([f"- {ip}: {count} istek" for ip, count in stats['top_ips']])
            
           
            if "saat" in question_lower:
                if "yoğun" in question_lower or "en çok" in question_lower:
                    busy_hours = "\n".join([f"- Saat {hour}:00: {count} istek" for hour, count in stats['busiest_hours']])
                    return f"En yoğun saatler:\n{busy_hours}"
                return f"Son 1 saatte {stats['recent_requests']} yeni istek geldi"
            
           
            if "hata" in question_lower or "error" in question_lower:
                error_details = "\n".join([f"- {status}: {count} istek" for status, count in stats['status_codes'].items() if status.startswith(('4', '5'))])
                return f"Toplam {stats['error_counts']} hatalı istek var:\n{error_details}"
            
            
            if "istek" in question_lower or "request" in question_lower:
                if "metod" in question_lower or "method" in question_lower:
                    methods = "\n".join([f"- {method}: {count}" for method, count in stats['methods'].most_common()])
                    return f"HTTP Metodları:\n{methods}"
                if "yol" in question_lower or "path" in question_lower:
                    paths = "\n".join([f"- {path}: {count}" for path, count in stats['top_paths']])
                    return f"En çok istenen yollar:\n{paths}"
                if "en çok" in question_lower:
                    if stats['top_requests']:
                        top_req, count = stats['top_requests'][0]
                        return f"En çok yapılan istek:\n{top_req}\n({count} kez)"
                return f"Toplam {stats['total_requests']} istek var"
            
            
            if "durum" in question_lower or "status" in question_lower:
                return "Durum kodları:\n" + "\n".join([f"- {status}: {count} istek" for status, count in stats['status_codes'].items()])
            
         
            return (
                f"Güncel Log Analizi:\n"
                f"- Toplam İstek: {stats['total_requests']}\n"
                f"- Son 1 Saatteki İstek: {stats['recent_requests']}\n"
                f"- Benzersiz IP Sayısı: {len(stats['unique_ips'])}\n"
                f"- Hatalı İstek: {stats['error_counts']}\n\n"
                f"En Aktif IP:\n"
                f"- {stats['top_ips'][0][0]}: {stats['top_ips'][0][1]} istek"
            )
            
        except Exception as e:
            return f"Üzgünüm, bir hata oluştu: {str(e)}" 