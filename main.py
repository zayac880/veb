from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

host_name = 'localhost'
port = 8080


def get_template(name):
    with open(name, 'r', encoding='utf-8') as f:
        return f.read()


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(get_template('contact.html'), 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Вывод данных формы в консоль
        print(str(parsed_data))

        # Отправка страницы контактов в качестве ответа
        self.wfile.write(bytes(get_template('contact.html'), 'utf-8'))


if __name__ == "__main__":
    server = HTTPServer((host_name, port), Server)
    print(f"Server started at http://{host_name}:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")