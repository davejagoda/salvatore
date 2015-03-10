#!/usr/bin/python

import BaseHTTPServer, time, urlparse, datetime

class SalvatoreHTTPServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def log_date_time_string(self):
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.gmtime(now)
        s = '%04d-%02d-%02dT%02d:%02d:%02dZ' % (
                year, month, day, hh, mm, ss)
        s = str(datetime.datetime.now())
        s = s.replace(' ', 'Z')
        return s

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write('<!doctype html><html><head><title>Salvatore</title><meta charset="utf-8" /></head><body>Salvatore</body></html>\n')

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        print(length)
        contents = self.rfile.read(length)
        post_data = urlparse.parse_qs(contents.decode('utf-8'))
        filename = self.log_date_time_string()
        with open(filename, 'w') as f:
            f.write(contents)
        for key, value in post_data.iteritems():
            print "%s=%s" % (key, value)
#        time.sleep(1)
        self._set_headers()
        self.wfile.write('<!doctype html><html><head><title>Salvatore</title><meta charset="utf-8" /></head><body>Salvatore</body></html>\n')

def run(server_class=BaseHTTPServer.HTTPServer, handler_class=SalvatoreHTTPServer, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if '__main__' == __name__:
    import sys
    if 2 != len(sys.argv):
        print('must provide a port number')
        sys.exit(1)
    run(port=int(sys.argv[1]))
