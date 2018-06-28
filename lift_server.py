#!/usr/bin/python
import BaseHTTPServer
import SocketServer
import urlparse
import ssl

PORT = 8000
FIFO = "/var/run/gpio.fifo"
auth_token = '7t8ufm4HsEZdrnid'

html = '''
<html>
    <head>
        <title>Up/Down</title>
        <meta charset="utf-8" />
        <style>
            a { text-decoration:none; }
        </style>
<!--
    up pointing finger: &#x261d;
    down pointing finger: &#x1f447;
-->
<title>Remote Light Control</title>
<link rel="apple-touch-icon" href="/greenfire.png">
<meta name="apple-mobile-web-app-title" content="GreenFire Lift">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<style>
<!-- @font-face{ font-family: fontawesome; src: url(/fa-regular-400.ttf); } -->
p{ font-size: 40vh; font-family: fontawesome; margin:0; }
a{ text-decoration:none; padding:0; }
</style>
<script type="text/javascript">
var xhttp = new XMLHttpRequest();
function sendCmd(cmd){
    xhttp.open('GET', '?cmd='+cmd);
    xhttp.send();
}
</script>
    </head>
<body>
<p style="text-align:center">
<a href="javascript:sendCmd('u')" style="color:green">&#x25b2;</a><br/>
<a href="javascript:sendCmd('d')" style="color:red">&#x25bc;</a>
</p></body>
</html>
'''

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def send_cmd(self, cmd):
        if cmd != "u" and cmd != "d":
            return
        with open(FIFO, "a") as fifo:
            fifo.write(cmd + "\n")
        
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(parsed_path.query)
        if ("auth" not in params) or (params['auth'][0] != auth_token):
            self.send_response(403)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("Unauthorized access forbidden.\n")
        elif self.path == "/greenfire.png":
            with open("/usr/local/share/greenfire.png",'r') as icon:
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(icon.read())
        elif "cmd" in params and ( params['cmd'][0] == "u" or params['cmd'][0] == "d" ):
            self.send_cmd(params['cmd'][0])
        else:
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html)

try:
    server = BaseHTTPServer.HTTPServer(("", PORT), MyHandler)
    server.socket = ssl.wrap_socket(server.socket, certfile='/home/chip/greenfire-remote.crt', keyfile='/home/chip/greenfire-remote.key', server_side=True)
    print('Started http server')
    server.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    server.socket.close()

