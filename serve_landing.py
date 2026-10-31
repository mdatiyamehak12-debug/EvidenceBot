"""
EvidenceBot - Landing Page Server with Optional Public Tunnel
============================================================
Serves the modern, responsive EvidenceBot landing page on port 5173
and optionally launches a Cloudflare Tunnel for worldwide instant browser access.
"""

import http.server
import socketserver
import os
import sys
import threading
import time
import subprocess
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PORT = 5173
ROOT_DIR = Path(__file__).resolve().parent
DIRECTORY = str(ROOT_DIR / "landing")
CLOUDFLARED_BIN = ROOT_DIR / "cloudflared.exe"
URL_FILE = ROOT_DIR / "data" / "landing_public_url.txt"
URL_FILE.parent.mkdir(parents=True, exist_ok=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Silent or concise logging
        pass


def run_http_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()


def run_tunnel():
    if not CLOUDFLARED_BIN.exists():
        print(f"[Tunnel] cloudflared.exe not found at {CLOUDFLARED_BIN}. Running local only.", flush=True)
        return

    cmd = [
        str(CLOUDFLARED_BIN),
        "tunnel",
        "--url", f"http://127.0.0.1:{PORT}",
        "--no-autoupdate"
    ]
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    while True:
        cf_proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1
        )

        url_detected = threading.Event()
        current_url = [None]

        def drain_output():
            try:
                for line in iter(cf_proc.stdout.readline, ""):
                    if not line:
                        break
                    match = url_pattern.search(line)
                    if match and not url_detected.is_set():
                        current_url[0] = match.group(0)
                        url_detected.set()
            except Exception:
                pass

        thread = threading.Thread(target=drain_output, daemon=True)
        thread.start()

        if url_detected.wait(timeout=25) and current_url[0]:
            public_url = current_url[0]
            print("", flush=True)
            print("*" * 75, flush=True)
            print("🎉 EVIDENCEBOT LANDING PAGE IS LIVE WORLDWIDE!", flush=True)
            print(f"👉 PUBLIC LANDING PAGE URL: {public_url}", flush=True)
            print(f"👉 LOCAL URL:               http://localhost:{PORT}", flush=True)
            print("*" * 75, flush=True)
            print("", flush=True)

            with open(URL_FILE, "w", encoding="utf-8") as f:
                f.write(public_url)

        while cf_proc.poll() is None:
            time.sleep(2)

        time.sleep(2)


def main():
    print("=" * 75, flush=True)
    print("           EVIDENCEBOT: STARTING LANDING PAGE WEB SERVER             ", flush=True)
    print("=" * 75, flush=True)
    print(f"Directory: {DIRECTORY}", flush=True)
    print(f"Port:      {PORT}", flush=True)

    # Start HTTP server thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    time.sleep(1)
    print(f"✅ Local server listening at http://localhost:{PORT}", flush=True)

    # Run Cloudflare Tunnel (blocking)
    try:
        run_tunnel()
    except KeyboardInterrupt:
        print("\nStopping landing server...", flush=True)


if __name__ == "__main__":
    main()
