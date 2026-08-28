#!/usr/bin/env python3
"""Preview server for local work.

    python3 tools/serve.py [port]

Serves the repo root, mirrors the netlify.toml SPA fallback so deep links like
/#/meals behave the same locally, and sends no-cache headers so a reload always
picks up the file you just edited.
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def send_head(self):
        # SPA fallback: an unknown path that is not an asset request gets index.html,
        # which is what netlify.toml does in production.
        path = self.translate_path(self.path)
        if not os.path.exists(path) and "." not in os.path.basename(self.path):
            self.path = "/index.html"
        return super().send_head()

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("Serving %s on http://localhost:%d  (ctrl-c to stop)" % (ROOT, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
