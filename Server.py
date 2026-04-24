#fayzeh  zghier 1221160
#shahd shewekeh 1222105
#dania abuayyash 1210464
import socket
import os 

student_id = 1221160
port = (student_id % 1000) + 5000 # port = 5160 #spcial port for the server 
host = "127.0.0.1"#local host the sarever will accept the connections from same device only
buffer_size = 1024 #maximum size of the data recevied from the client # sice the header sice offen is 1KB 
HTML_DIR = "html" 

def load_file(path): #this function is to fetch the file from the html directory 
    print(f"[DEBUG] ===== LOADING FILE =====")
    print(f"[DEBUG] Requested path: '{path}'")
    print(f"[DEBUG] Absolute path: '{os.path.abspath(path)}'")
    print(f"[DEBUG] File exists: {os.path.exists(path)}")
    
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                content = f.read()
                print(f"[DEBUG] SUCCESS: Loaded {len(content)} bytes from {path}")
                return content, 200 #status of the html file 200 ok 
        except Exception as e:
            print(f"[DEBUG]  ERROR reading file: {e}")
            return None, 404
    else:
        print(f"[DEBUG]  FILE NOT FOUND: {path}")
       
        dir_path = os.path.dirname(path) #try to list what is actually in the directory
        if os.path.exists(dir_path):
            print(f"[DEBUG] Contents of {dir_path}:")
            try:
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    print(f"[DEBUG]   - {item} ({'file' if os.path.isfile(item_path) else 'dir'})")
            except Exception as e:
                print(f"[DEBUG] Error listing directory: {e}")
        return None, 404 #this if it is not found it will gives this error 
# to tell the broswer ehat of the file we are sending " types of object"
def get_content_type(path): # this function is to get the cintent type of the file 
    if path.endswith(".html"): return "text/html"
    if path.endswith(".css"): return "text/css"
    if path.endswith(".js"): return "application/javascript"
    if path.endswith(".jpg") or path.endswith(".jpeg"): return "image/jpeg"
    if path.endswith(".png"): return "image/png"
    if path.endswith(".gif"): return "image/gif"
    if path.endswith(".ico"): return "image/x-icon"
    if path.endswith(".txt"): return "text/plain"
    if path.endswith(".pdf"): return "application/pdf"
    return "application/binary-stream" #default binary stream unko


def build_response(status_code, content=b"", content_type="text/html"): #this functon is to build response to sent it to client 
    status_messages = {200: "OK", 403: "Forbidden", 404: "Not Found", 400: "Bad Request"} #http status messages 
    status_message = status_messages.get(status_code, "Unknown") # get message or unknown if not found
    headers = f"HTTP/1.1 {status_code} {status_message}\r\n"#http statuse line 
    headers += f"Content-Type: {content_type}\r\n"#content type header 
    headers += f"Content-Length: {len(content)}\r\n"#m content length header 
    headers += "Connection: close\r\n\r\n"#this to convert headers to bytes and append content
    
    print(f"[DEBUG] Response: {status_code} {status_message}, Content-Type: {content_type}, Size: {len(content)} bytes")
    print(f"[DEBUG] Headers:\n{headers}")
    return headers.encode() + content

def detect_language(path):
    if "lang=ar" in path or "_ar" in path or "main_ar" in path or "T020_1221160_ar" in path:
        return "ar"
    else:
        return "en"

def handle_request(request, client_address):#this function to process http requst 
    print(f"\n{'='*50}")#separator for each request
    print(f"[REQUEST] From {client_address}")
    
    try:
        request_line = request.split("\r\n")[0]# get the first line of http requset 
        method, path, _ = request_line.split()#split it into method ,path,version
        print(f"[REQUEST] {method} {path}")
    except:
        print("[ERROR] Bad request format")
        return build_response(400, b"<h1>Bad Request</h1>")#bad requst if it is error 
    original_path = path #URL normalization
    if path in ["/", "/index.html", "/main_en.html", "/en"]: 
        path = "/main_en.html"
    elif path in ["/ar", "/main_ar.html"]:
        path = "/main_ar.html"
    
    if path != original_path:
        print(f"[DEBUG] Path normalized: '{original_path}' -> '{path}'")

   #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.
    if "private" in path:# check for private files befor loading 
        print(f"[403] Private file requested: {path}")
        lang = detect_language(path)#detect the language
        error_page, _ = load_file(os.path.join(HTML_DIR, f"error403_{lang}.html"))
        if not error_page:
            error_page = b"<h1>403 Forbidden</h1>"
        return build_response(403, error_page)
    ###########################################################
    print(f"[DEBUG] Processing path: '{path}'")
    if path.startswith("/css/"):
        file_path = path[1:]#remove leading slash
        print(f"[DEBUG] CSS request: {file_path}")
    elif path.startswith("/imgs/"):
        file_path = path[1:]#remove leading slash
        print(f"[DEBUG] IMAGE request: {file_path}")
    elif path.startswith("/html/"):
        file_path = path[1:]#remove leading slash
        print(f"[DEBUG] HTML request: {file_path}")
    else:
        file_path = os.path.join(HTML_DIR, path.lstrip("/"))#default to html directory
        print(f"[DEBUG] Default request: {file_path}")
    print(f"[DEBUG] Final file path: '{file_path}'")
    content, status = load_file(file_path)# to load the file 
    #here to deal with the file status 
    if status == 200:
        content_type = get_content_type(file_path)
        return build_response(200, content, content_type)#to send the response that it is okay 200
    else:
        lang = detect_language(path)# to detect the language 
        error_page, _ = load_file(os.path.join(HTML_DIR, f"error404_{lang}.html"))
        if not error_page:
            error_page = f"<h1>404 Not Found</h1><p>File not found: {path}</p>".encode() #default error page if the error page not found 
        return build_response(404, error_page)

def start_server(): #this function to start the server 
    print(f"[STARTUP] Server starting on {host}:{port}")
    print(f"[STARTUP] Working directory: {os.getcwd()}")
    print(f"[STARTUP] Server URL: http://{host}:{port}")
    print(f"\n[STARTUP] Directory structure:")#to show the current directory structue 
    for root, dirs, files in os.walk("."): #from the curren t directory 
        if root.startswith("./.git"):#to ignore the .git directory "that is contain commits,branches,history "
            continue
        level = root.replace(".", "").count(os.sep)#/ to see how the deep o f the folder 
        indent = "  " * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = "  " * (level + 1)#to see the leevel 
        for file in files[:5]:  # Limit to first 5 files per directory
            print(f"{subindent}{file}")
        if len(files) > 5:
            print(f"{subindent}... and {len(files)-5} more files")
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#this to creat the socket 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#it is allow to use the port immedatly 
    server_socket.bind((host, port))#to compain the local ip with the port 
    server_socket.listen(5)#limit number in the queue 5 communications maximum 
    print(f"\n[STARTUP] Server is running! Visit: http://{host}:{port}")
   # print(f"[STARTUP] Test images at: http://{host}:{port}/html/test_images.html")
    
    while True:
        try:
            client_socket, client_address = server_socket.accept()#accept communication from the browser 
            request = client_socket.recv(buffer_size).decode()#to read the request 
            if request:
                response = handle_request(request, client_address)
                client_socket.sendall(response)#to send to the client 
            client_socket.close()
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Server stopping...")#if the server closed by me ctrl + c 
            break
        except Exception as e:
            print(f"[ERROR] Server error: {e}")#if we cant read the file in the recv 
    
    server_socket.close()

if __name__ == "__main__":
    start_server()