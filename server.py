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
            db = open("text.txt", "r")

            old_archives = db.readlines()
            db.close()

            if not old_archives:
                old_archives = []
            else:
                all_text = ""
                for text in old_archives:
                    all_text += text
                old_archives = json.loads(all_text)

            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            
            for it in old_archives:
                del it["password"]
                del it["adress"]
                del it["rg"]

            res = {
                "data": old_archives,
                "status": "success"
            }
            return self.wfile.write(json.dumps(res).encode())
        elif '/users/' in self.path:
            query = self.path[7:]

            db = open("text.txt", "r")

            old_archives = db.readlines()
            db.close()

            if not old_archives:
                old_archives = []
            else:
                all_text = ""
                for text in old_archives:
                    all_text += text
                old_archives = json.loads(all_text)
            
            for it in old_archives:
                if it["registration"] == query:
                    self.send_response(200)
                    self.send_header('Content-type','application/json')
                    self.end_headers()

                    del it["password"]

                    res = {
                        "data": it,
                        "status": "success"
                    }
                    return self.wfile.write(json.dumps(res).encode())
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            res = {
                "status": "fail",
                "message": "user not found"
            }

            return self.wfile.write(json.dumps(res).encode())
        
    def do_POST(self):
        if self.path == '/users':
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))

            db = open("text.txt", "r")
            old_archives = db.readlines()
            db.close()

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

            old_archives = [post_data, *old_archives]

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
            db.close()

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

            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            res = {
                "status": "fail",
                "message": "user unauthenticated"
            }

            return self.wfile.write(json.dumps(res).encode())

    def do_PUT(self):
        if self.path == '/users':
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))

            db = open("text.txt", "r")

            old_archives = db.readlines()
            db.close()
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
                    
                    copy[idx]['name'] = post_data['name']
                    copy[idx]['adress'] = post_data['adress']
                    copy[idx]['rg'] = post_data['rg']

                    db = open("text.txt", "w")
                    db.writelines(json.dumps(copy))
                    db.close()
                    
                    res = {
                        "data": post_data,
                        "status": "success"
                    }
                    
                    return self.wfile.write(json.dumps(res).encode())

            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            res = {
                "message": "user does not exists",
                "status": "not found"
            }

            return self.wfile.write(json.dumps(res).encode())
    
    def do_DELETE(self):
        if self.path == '/users':
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))
            db = open("text.txt", "r")

            old_archives = db.readlines()
            db.close()

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

            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            res = {
                "data": "",
                "status": "not found"
            }

            return self.wfile.write(json.dumps(res).encode())
            
    def do_PATCH(self):
        if self.path == '/change-password':
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length))
            db = open("text.txt", "r")

            old_archives = db.readlines()
            db.close()

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
                    if user["password"] == post_data["oldPassword"]:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        
                        copy[idx]["password"] = post_data["newPassword"]

                        db = open("text.txt", "w")
                        db.writelines(json.dumps(copy))
                        db.close()
                        
                        res = {
                            "message": "Password changed",
                            "status": "success"
                        }
                        
                        return self.wfile.write(json.dumps(res).encode())
                    else:
                        self.send_response(401)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        res = {
                            "message": "User not found",
                            "status": "fail"
                        }

                        return self.wfile.write(json.dumps(res).encode())
            db.close()

            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            res = {
                "message": "Incorrect password for user",
                "status": "fail"
            }

            return self.wfile.write(json.dumps(res).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
        
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Max-Age', '1800')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, PATCH, OPTIONS')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

PORT = 3030

handler = Server

myserver = socketserver.TCPServer(("", PORT), handler)
print("Server init on http://localhost:"+str(PORT))

try:
    myserver.serve_forever()
except KeyboardInterrupt:
    pass

myserver.server_close()
print("Server Stops")