from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import mysql.connector
import os

HOST = "127.0.0.1"
PORT = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index":
            file_path = "index.html"
            
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")

        elif self.path == "/users":
            self.list_users()

        else:
            self.send_error(404, "Route Not Found")


    def do_POST(self):
        if self.path == "/save":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)

            data = urllib.parse.parse_qs(body.decode())
            name = data.get("name", [""])[0]
            email = data.get("email", [""])[0]

            # Save to DB
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="webdb",
                port=3306
            )

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users(name, email) VALUES (%s, %s)",
                (name, email)
            )
            conn.commit()

            cursor.close()
            conn.close()

            # Response ke browser
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(b"<h3>Data berhasil disimpan!</h3>")
            self.wfile.write(b"<a href='/'>Kembali</a><br>")
            self.wfile.write(b"<a href='/users'>Lihat Data</a>")


    def list_users(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="webdb",
            port=3306
        )

        cursor = conn.cursor()
        cursor.execute("SELECT name, email FROM users")
        rows = cursor.fetchall()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(b"<h2>Daftar User:</h2><ul>")
        for row in rows:
            line = f"<li>{row[0]} - {row[1]}</li>".encode()
            self.wfile.write(line)
        self.wfile.write(b"</ul><br><a href='/'>Kembali</a>")

        cursor.close()
        conn.close()


server = HTTPServer((HOST, PORT), MyServer)
print(f"Server berjalan di http://{HOST}:{PORT}")
server.serve_forever()
