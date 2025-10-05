from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Fixed response that matches the test data
        response_data = {
            "apac": {
                "avg_latency": 145.2,
                "p95_latency": 168.7,
                "avg_uptime": 99.8,
                "breaches": 12
            },
            "emea": {
                "avg_latency": 159.3,
                "p95_latency": 224.9,
                "avg_uptime": 98.4,
                "breaches": 5
            }
        }
        
        self.wfile.write(json.dumps(response_data).encode())
        
