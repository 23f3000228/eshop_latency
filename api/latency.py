from http.server import BaseHTTPRequestHandler
import json
import statistics
import os

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Expose-Headers', '*')
        self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(post_data)
            
            regions = request_data.get('regions', [])
            threshold_ms = request_data.get('threshold_ms', 180)
            response_data = self._calculate_metrics(regions, threshold_ms)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Expose-Headers', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def _calculate_metrics(self, regions, threshold_ms):
        # Read telemetry data
        with open('../telemetry.json', 'r') as f:
            telemetry_data = json.load(f)
        
        response_data = {"regions": {}}
        
        for region in regions:
            region_data = [item for item in telemetry_data if item.get('region') == region]
            
            # DEBUG: Print what data we're working with
            print(f"Region: {region}, Data points: {len(region_data)}")
            for item in region_data:
                print(f"  Latency: {item['latency_ms']}, Uptime: {item['uptime_percent']}")
            
            latencies = [item['latency_ms'] for item in region_data]
            uptimes = [item['uptime_percent'] for item in region_data]
            
            # Simple average calculation
            avg_latency = sum(latencies) / len(latencies)
            
            # 95th percentile
            sorted_latencies = sorted(latencies)
            p95_index = int(0.95 * len(sorted_latencies))
            p95_latency = sorted_latencies[p95_index]
            
            avg_uptime = sum(uptimes) / len(uptimes)
            breaches = sum(1 for latency in latencies if latency > threshold_ms)
            
            response_data["regions"][region] = {
                "avg_latency": round(avg_latency, 2),
                "p95_latency": round(p95_latency, 2),
                "avg_uptime": round(avg_uptime, 2),
                "breaches": breaches
            }
            
            print(f"Calculated - avg_latency: {avg_latency:.2f}, breaches: {breaches}")
        
        return response_data
