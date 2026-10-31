"""
EvidenceBot - Public Server & Live HTTPS Tunnel Launcher (Auto-Healing)
========================================================================
Starts the Streamlit application and establishes a resilient, self-healing public HTTPS tunnel
so EvidenceBot remains reliably accessible.
"""

import sys
import subprocess
import time
import re
import threading
from pathlib import Path
import urllib.request

# Ensure unbuffered UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent
PUBLIC_URL_FILE = ROOT_DIR / "data" / "public_url.txt"
PUBLIC_URL_FILE.parent.mkdir(parents=True, exist_ok=True)


def wait_for_streamlit(port=8501, timeout=25):
    """Waits until Streamlit server responds on health check endpoint."""
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
    """Launches the Streamlit server."""
    streamlit_cmd = [
        sys.executable,
        "-m", "streamlit",
        "run", "app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
    ]
    return subprocess.Popen(
        streamlit_cmd,
        cwd=str(ROOT_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def run_tunnel(st_proc):
    """Manages the SSH tunnel with continuous output draining and auto-reconnect."""
    ssh_cmd = [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=20",
        "-o", "ServerAliveCountMax=5",
        "-o", "TCPKeepAlive=yes",
        "-o", "ExitOnForwardFailure=yes",
        "-R", "80:127.0.0.1:8501",
        "nokey@localhost.run"
    ]
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.lhr\.life")

    while True:
        if st_proc.poll() is not None:
            print("Streamlit process stopped. Exiting tunnel.", flush=True)
            break

        print("[Tunnel] Establishing live public HTTPS tunnel via localhost.run...", flush=True)
        ssh_proc = subprocess.Popen(
            ssh_cmd,
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
                for line in iter(ssh_proc.stdout.readline, ""):
                    if not line:
                        break
                    if "admin.localhost.run" in line or "localhost.run/docs" in line:
                        continue
                    match = url_pattern.search(line)
                    if match and not url_detected.is_set():
                        current_url[0] = match.group(0)
                        url_detected.set()
            except Exception:
                pass

        reader_thread = threading.Thread(target=drain_output, daemon=True)
        reader_thread.start()

        # Wait for the tunnel URL to appear
        if url_detected.wait(timeout=20) and current_url[0]:
            public_url = current_url[0]
            print("", flush=True)
            print("*" * 70, flush=True)
            print("🎉 SUCCESS! EVIDENCEBOT IS NOW LIVE AND ACCESSIBLE WORLDWIDE:", flush=True)
            print(f"👉 PUBLIC URL: {public_url}", flush=True)
            print("*" * 70, flush=True)
            print("Anyone with this link can open EvidenceBot in their browser!", flush=True)

            with open(PUBLIC_URL_FILE, "w", encoding="utf-8") as f:
                f.write(public_url)
        else:
            print("⚠️ Waiting for tunnel endpoint...", flush=True)

        # Monitor ssh process
        while ssh_proc.poll() is None:
            if st_proc.poll() is not None:
                ssh_proc.terminate()
                return
            time.sleep(2)

        print("⚠️ SSH tunnel disconnected. Reconnecting in 3 seconds...", flush=True)
        time.sleep(3)


def main():
    print("=" * 70, flush=True)
    print("       EVIDENCEBOT: STARTING APPLICATION & PUBLIC HTTPS TUNNEL       ", flush=True)
    print("=" * 70, flush=True)

    print("[1/2] Starting Streamlit Application on port 8501...", flush=True)
    st_proc = start_streamlit()

    print("[2/2] Waiting for Streamlit server to initialize...", flush=True)
    if not wait_for_streamlit(port=8501, timeout=25):
        print("⚠️ Streamlit taking longer to respond, continuing with tunnel...", flush=True)
    else:
        print("✅ Streamlit server is active and healthy on port 8501.", flush=True)

    try:
        run_tunnel(st_proc)
    except KeyboardInterrupt:
        print("\nShutting down...", flush=True)
    finally:
        st_proc.terminate()


if __name__ == "__main__":
    main()
