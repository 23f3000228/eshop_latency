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
            # Read and parse request
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                raise ValueError("Empty request body")
                
            post_data = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(post_data)
            
            regions = request_data.get('regions', [])
            threshold_ms = request_data.get('threshold_ms', 180)
            
            # Read telemetry.json from parent directory
            telemetry_path = '../telemetry.json'
            
            with open(telemetry_path, 'r') as f:
                telemetry_data = json.load(f)
            
            response_data = {"regions": {}}
            
            for region in regions:
                # Filter data for this region
                region_data = [item for item in telemetry_data if item.get('region') == region]
                
                if not region_data:
                    response_data["regions"][region] = {
                        "avg_latency": 0,
                        "p95_latency": 0,
                        "avg_uptime": 0,
                        "breaches": 0
                    }
                    continue
                
                # Extract values
                latencies = [item['latency_ms'] for item in region_data]
                uptimes = [item['uptime_percent'] for item in region_data]
                
                # Calculate metrics
                avg_latency = statistics.mean(latencies)
                p95_latency = sorted(latencies)[int(0.95 * len(latencies))]
                avg_uptime = statistics.mean(uptimes)
                breaches = sum(1 for latency in latencies if latency > threshold_ms)
                
                response_data["regions"][region] = {
                    "avg_latency": round(avg_latency, 2),
                    "p95_latency": round(p95_latency, 2),
                    "avg_uptime": round(avg_uptime, 2),
                    "breaches": breaches
                }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Expose-Headers', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except FileNotFoundError as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"telemetry.json not found at {telemetry_path}"}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Server error: {str(e)}"}).encode('utf-8'))
