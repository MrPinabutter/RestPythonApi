import http.server
import socketserver
import json

class Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == '/users':
            self.send_response(200)
            db = open("text.txt", "r")

            old_archives = db.readlines()
            if not old_archives:
                old_archives = []
            else:
                all_text = ""
                for text in old_archives:
                    all_text += text
                old_archives = json.loads(all_text)
            
            self.send_header('Content-type','application/json')
            self.end_headers()
            res = {
                "data": old_archives,
                "status": "success"
            }
            return self.wfile.write(json.dumps(res).encode())

    def do_POST(self):
        if self.path == '/users':
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))
            db = open("text.txt", "r")

            # Verifica integridade do objeto
            if not (
                "name" in post_data.keys() and 
                "registration" in post_data.keys() and
                "adress" in post_data.keys() and
                "password" in post_data.keys() and
                "rg" in post_data.keys()
            ):
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                res = {
                    "status": "fail",
                    "message": "missing data"
                }
                return self.wfile.write(json.dumps(res).encode())

            # Verifica o banco de dados
            old_archives = db.readlines()
            if not old_archives:
                old_archives = []
            else:
                all_text = ""
                for text in old_archives:
                    all_text += text
                old_archives = json.loads(all_text)

            for user in old_archives:
                if user["registration"] == post_data["registration"]:
                    self.send_response(400)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    res = {
                        "status": "faill",
                        "message": "user already exists"
                    }
                    return self.wfile.write(json.dumps(res).encode())
            old_archives.append(post_data)
            db.close()

            db = open("text.txt", "w")
            db.writelines(json.dumps(old_archives))
            db.close()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            res = {
                "data": post_data,
                "status": "success"
            }
            return self.wfile.write(json.dumps(res).encode())
        elif self.path == '/login':
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))
            db = open("text.txt", "r")

            old_archives = db.readlines()
            if not old_archives:
                old_archives = []
            else:
                all_text = ""
                for text in old_archives:
                    all_text += text
                old_archives = json.loads(all_text)

            for user in old_archives:
                if user["registration"] == post_data["registration"]:
                    if user["password"] == post_data["password"]:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        res = {
                            "status": "success",
                            "message": "user authenticated"
                        }
                        return self.wfile.write(json.dumps(res).encode())
            db.close()

            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            res = {
                "status": "fail",
                "message": "user unauthenticated"
            }
            return self.wfile.write(json.dumps(res).encode())

    def do_PATCH(self):
        if self.path == '/users':
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))
            db = open("text.txt", "r")

            old_archives = db.readlines()
            if not old_archives:
                old_archives = []
            else:
                all_text = ""
                for text in old_archives:
                    all_text += text
                old_archives = json.loads(all_text)

            copy = old_archives.copy()
            for idx, user in enumerate(copy):
                if user["registration"] == post_data["registration"]:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    
                    copy[idx] = post_data

                    db = open("text.txt", "w")
                    db.writelines(json.dumps(copy))
                    db.close()
                    
                    res = {
                        "data": post_data,
                        "status": "success"
                    }
                    
                    return self.wfile.write(json.dumps(res).encode())
            db.close()
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            res = {
                "data": "",
                "status": "not found"
            }
            return self.wfile.write(json.dumps(res).encode())
    
    def do_DELETE(self):
        if self.path == '/users':
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))
            db = open("text.txt", "r")

            old_archives = db.readlines()
            if not old_archives:
                old_archives = []
            else:
                all_text = ""
                for text in old_archives:
                    all_text += text
                old_archives = json.loads(all_text)

            copy = old_archives.copy()
            for idx, user in enumerate(copy):
                if user["registration"] == post_data["registration"]:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    
                    del(copy[idx])

                    db = open("text.txt", "w")
                    db.writelines(json.dumps(copy))
                    db.close()
                    
                    res = {
                        "data": post_data,
                        "status": "success"
                    }
                    
                    return self.wfile.write(json.dumps(res).encode())
            db.close()
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            res = {
                "data": "",
                "status": "not found"
            }
            return self.wfile.write(json.dumps(res).encode())
            

PORT = 8080

handler = Server

myserver = socketserver.TCPServer(("", PORT), handler)
print("Server init on http://localhost:8080")

try:
    myserver.serve_forever()
except KeyboardInterrupt:
    pass

myserver.server_close()
print("Server Stops")