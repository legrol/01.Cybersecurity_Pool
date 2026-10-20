import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class VulnerableHandler(BaseHTTPRequestHandler):
    def send_html_form(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <body>
            <h2>Piscine 42 - Vulnerable Login</h2>
            <!-- Este formulario finge ser un punto de entrada a una DB -->
            <form action="/login" method="GET">
                <input type="text" name="username" value="">
                <input type="password" name="password" value="">
                <input type="hidden" name="user_token" value="abc123">
                <input type="submit" value="Login">
            </form>
        </body>
        </html>
        """)

    def handle_injection(self, data_dict):
        # vaccine.py enviara "test'" o "test\"" primero para comprobar vulnerabilidad
        username = data_dict.get('username', [''])[0]
        
        # 1. Comprobacion de vulnerabilidad (provocamos el error para que Vaccine lo detecte)
        if username.endswith("'") or username.endswith('"'):
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Devolvemos un error que Vaccine reconoce ("warning: mysql") y el motor ("mariadb")
            self.wfile.write(b"warning: mysql. You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version")
            return

        # 2. Inyeccion exitosa (Cuando Vaccine empieza a enviar payloads como ' OR 1=1 --)
        payloads_indicators = ["OR", "'", "UNION", "1=1", "LIKE", "SELECT", "AND"]
        if any(p in username.upper() for p in payloads_indicators) and username != "test" and "test" not in username:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Vaccine busca la etiqueta <pre> en la respuesta exitosa para extraer el volcado de la DB
            self.wfile.write(b"""
            <html>
            <body>
                <p>Login bypass successful!</p>
                <pre>
[Database Dump]
Table: users
----------------------
id | username | password
1  | admin    | 42_flag_super_secret_99
2  | robi     | piscine_eval_pass
                </pre>
            </body>
            </html>
            """)
            return

        # 3. Peticion normal sin injeccion
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Invalid login")

    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_html_form()
        elif parsed_path.path == '/login':
            qs = parse_qs(parsed_path.query)
            self.handle_injection(qs)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/login':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            qs = parse_qs(post_data)
            self.handle_injection(qs)
        else:
            self.send_response(404)
            self.end_headers()

    # Silenciar logs para que no ensucien la terminal del alumno
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            ports = [int(sys.argv[1])]
        except ValueError:
            ports = [8080, 8081]
    else:
        ports = [8080, 8081]

    server = None
    port = None
    for candidate in ports:
        try:
            server = HTTPServer(('127.0.0.1', candidate), VulnerableHandler)
            port = candidate
            break
        except OSError:
            continue

    if server is None:
        raise OSError("No free port found for dummy server")

    print("===================================================")
    print("[+] Servidor vulnerable de prueba (Mock) INICIADO.")
    print(f"[+] Escuchando en: http://127.0.0.1:{port}")
    print("===================================================")
    server.serve_forever()
