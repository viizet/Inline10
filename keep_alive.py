"""
Keep Alive Server for Replit Deployment
"""

import logging
from threading import Thread
import time
import os

logger = logging.getLogger(__name__)

def run_server():
    """Run a simple HTTP server to keep the bot alive"""
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        class KeepAliveHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                response = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Media Search Bot - Online</title>
                    <meta http-equiv="refresh" content="30">
                    <style>
                        body { 
                            font-family: Arial, sans-serif; 
                            text-align: center; 
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            margin: 0;
                            padding: 50px;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 40px;
                            background: rgba(255,255,255,0.1);
                            border-radius: 15px;
                            backdrop-filter: blur(10px);
                        }
                        h1 { color: #fff; margin-bottom: 20px; }
                        .status { 
                            font-size: 24px; 
                            color: #4CAF50; 
                            margin: 20px 0;
                        }
                        .info {
                            background: rgba(255,255,255,0.2);
                            padding: 20px;
                            border-radius: 10px;
                            margin: 20px 0;
                        }
                        .footer {
                            margin-top: 30px;
                            font-size: 14px;
                            opacity: 0.8;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🤖 Media Search Bot</h1>
                        <div class="status">✅ Online & Running</div>
                        
                        <div class="info">
                            <h3>🔍 Bot Features:</h3>
                            <p>• Inline media search across Telegram channels</p>
                            <p>• Support for videos, documents, audio, photos & GIFs</p>
                            <p>• Advanced filtering and search capabilities</p>
                            <p>• Admin tools for management</p>
                        </div>
                        
                        <div class="info">
                            <h3>📊 System Status:</h3>
                            <p>Server Time: """ + time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()) + """</p>
                            <p>Environment: """ + ('Replit' if os.getenv('REPL_ID') else 'Local') + """</p>
                            <p>Keep-Alive: Active</p>
                        </div>
                        
                        <div class="footer">
                            <p>This page refreshes automatically every 30 seconds</p>
                            <p>Bot is actively monitoring channels and ready for searches</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                self.wfile.write(response.encode())
            
            def log_message(self, format, *args):
                # Suppress HTTP server logs
                return
        
        # Start server on port 5000
        server = HTTPServer(('0.0.0.0', 5000), KeepAliveHandler)
        logger.info("Keep-alive server started on port 5000")
        server.serve_forever()
        
    except Exception as e:
        logger.error(f"Error starting keep-alive server: {e}")

def keep_alive():
    """Start the keep-alive server in a separate thread"""
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    logger.info("Keep-alive service started")

if __name__ == "__main__":
    keep_alive()
    # Keep the script running
    while True:
        time.sleep(60)
