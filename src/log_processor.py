import re
from datetime import datetime
from typing import List, Dict

class LogProcessor:
    def __init__(self, log_path: str):
        self.log_path = log_path
        
    def parse_log_line(self, line: str) -> Dict:
        """NGINX log satırını parse eder."""
        pattern = r'(?P<remote_addr>[\d\.]+) - (?P<remote_user>[^ ]*) \[(?P<time_local>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<body_bytes_sent>\d+) "(?P<http_referer>.*?)" "(?P<http_user_agent>.*?)"'
        
        match = re.match(pattern, line)
        if match:
            return match.groupdict()
        return {}
        
    def read_logs(self) -> List[Dict]:
        """Log dosyasını okur ve parse edilmiş log kayıtlarını döndürür."""
        parsed_logs = []
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        parsed_log = self.parse_log_line(line.strip())
                        if parsed_log:
                            parsed_logs.append(parsed_log)
                    except Exception as e:
                        print(f"Log satırı parse edilemedi: {e}")
                        continue
                        
        except FileNotFoundError:
            print(f"Log dosyası bulunamadı: {self.log_path}")
            return []
            
        return parsed_logs
    
    def format_log_for_embedding(self, log: Dict) -> str:
        """Log kaydını embedding için uygun formata dönüştürür."""
        return (f"IP: {log.get('remote_addr', 'N/A')} "
                f"Tarih: {log.get('time_local', 'N/A')} "
                f"İstek: {log.get('request', 'N/A')} "
                f"Durum: {log.get('status', 'N/A')} "
                f"User Agent: {log.get('http_user_agent', 'N/A')}") 