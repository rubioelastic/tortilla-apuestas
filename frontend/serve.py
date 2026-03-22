#!/usr/bin/env python3
"""
🌐 Servidor web simple para el frontend
Sirve los archivos estáticos en http://localhost:3000
"""

import http.server
import socketserver
import os

# Puerto en el que se servirá el frontend
PORT = 3000

# Cambiar al directorio del frontend
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado con CORS habilitado"""
    
    def end_headers(self):
        # Agregar headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Manejar peticiones OPTIONS (preflight CORS)"""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Log personalizado más limpio"""
        print(f"[Frontend] {args[0]}")

# Crear servidor
Handler = CustomHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  🌶️  TortillApuestas - Frontend Server                       ║
║                                                               ║
║  ✅ Servidor corriendo en: http://localhost:{PORT}              ║
║  📂 Sirviendo archivos desde: {os.getcwd()[:30]}...
║                                                               ║
║  🔗 Abre en tu navegador:                                     ║
║     http://localhost:{PORT}                                      ║
║                                                               ║
║  🛑 Para detener: presiona Ctrl+C                            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        httpd.shutdown()
