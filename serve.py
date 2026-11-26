"""Local web server for this site that never lets the browser use stale files.
Run:  py serve.py   then open http://localhost:5500
"""
import functools
import http.server
import os
import socketserver

PORT = 5500
ROOT = os.path.dirname(os.path.abspath(__file__))


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    handler = functools.partial(NoCacheHandler, directory=ROOT)
    with Server(("", PORT), handler) as httpd:
        print(f"Website running at http://localhost:{PORT}  (close this window to stop)")
        httpd.serve_forever()
