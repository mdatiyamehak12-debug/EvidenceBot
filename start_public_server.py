"""
EvidenceBot - Public Server with Cloudflare Tunnel (Enterprise Grade)
======================================================================
Starts Streamlit and establishes a high-performance, enterprise-grade public HTTPS tunnel
via Cloudflare Tunnel (trycloudflare.com) that opens instantly in Google Chrome worldwide.
"""

import sys
import subprocess
import time
import re
import threading
from pathlib import Path
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent
CLOUDFLARED_BIN = ROOT_DIR / "cloudflared.exe"
PUBLIC_URL_FILE = ROOT_DIR / "data" / "public_url.txt"
PUBLIC_URL_FILE.parent.mkdir(parents=True, exist_ok=True)


def wait_for_streamlit(port=8501, timeout=30):
    url = f"http://127.0.0.1:{port}/_stcore/health"
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def start_streamlit():
    cmd = [
        sys.executable,
        "-m", "streamlit",
        "run", "app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false",
        "--browser.gatherUsageStats=false"
    ]
    return subprocess.Popen(
        cmd,
        cwd=str(ROOT_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def run_cloudflare_tunnel(st_proc):
    cmd = [
        str(CLOUDFLARED_BIN),
        "tunnel",
        "--url", "http://127.0.0.1:8501",
        "--no-autoupdate"
    ]
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    while True:
        if st_proc.poll() is not None:
            print("Streamlit stopped. Exiting tunnel.", flush=True)
            break

        print("[Tunnel] Starting Cloudflare Tunnel edge connection...", flush=True)
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
            print("🎉 EVIDENCEBOT IS LIVE! DIRECT PUBLIC CLOUDFLARE URL:", flush=True)
            print(f"👉 PUBLIC URL: {public_url}", flush=True)
            print("*" * 75, flush=True)
            print("This URL opens EvidenceBot directly in Google Chrome / any browser worldwide!", flush=True)
            print("", flush=True)

            with open(PUBLIC_URL_FILE, "w", encoding="utf-8") as f:
                f.write(public_url)
        else:
            print("⚠️ Tunnel initialization taking longer...", flush=True)

        while cf_proc.poll() is None:
            if st_proc.poll() is not None:
                cf_proc.terminate()
                return
            time.sleep(2)

        print("⚠️ Cloudflare tunnel reconnected. Re-establishing...", flush=True)
        time.sleep(2)


def main():
    print("=" * 75, flush=True)
    print("      EVIDENCEBOT: STARTING ENTERPRISE SERVER & CLOUDFLARE TUNNEL      ", flush=True)
    print("=" * 75, flush=True)

    print("[1/2] Starting Streamlit Server...", flush=True)
    st_proc = start_streamlit()

    print("[2/2] Checking local Streamlit health...", flush=True)
    if not wait_for_streamlit(port=8501, timeout=30):
        print("⚠️ Streamlit still starting...", flush=True)
    else:
        print("✅ Streamlit server is active and healthy on port 8501.", flush=True)

    try:
        run_cloudflare_tunnel(st_proc)
    except KeyboardInterrupt:
        print("\nShutting down...", flush=True)
    finally:
        st_proc.terminate()


if __name__ == "__main__":
    main()
