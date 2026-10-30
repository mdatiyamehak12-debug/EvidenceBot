"""
EvidenceBot - Public Server & Live HTTPS Tunnel Launcher
========================================================
Starts the Streamlit application and establishes a live public HTTPS tunnel
so anyone on the internet can access EvidenceBot immediately.
"""

import sys
import subprocess
import time
import re
from pathlib import Path
import urllib.request

# Ensure unbuffered UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent
PUBLIC_URL_FILE = ROOT_DIR / "data" / "public_url.txt"


def wait_for_streamlit(port=8501, timeout=25):
    """Waits until Streamlit server responds on health check endpoint."""
    url = f"http://localhost:{port}/_stcore/health"
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


def main():
    print("=" * 70, flush=True)
    print("       EVIDENCEBOT: STARTING APPLICATION & PUBLIC HTTPS TUNNEL       ", flush=True)
    print("=" * 70, flush=True)

    # 1. Start Streamlit Process
    print("[1/3] Starting Streamlit Application on port 8501...", flush=True)
    streamlit_cmd = [
        sys.executable,
        "-m", "streamlit",
        "run", "app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
    ]
    st_proc = subprocess.Popen(
        streamlit_cmd,
        cwd=str(ROOT_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # 2. Wait for Streamlit to be healthy
    print("[2/3] Waiting for Streamlit server to initialize...", flush=True)
    if not wait_for_streamlit(port=8501, timeout=25):
        print("⚠️ Streamlit taking longer to respond, continuing with tunnel...", flush=True)
    else:
        print("✅ Streamlit server is active and healthy on port 8501.", flush=True)

    # 3. Start SSH Tunnel to localhost.run
    print("[3/3] Establishing live public HTTPS tunnel via localhost.run...", flush=True)
    ssh_cmd = [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-R", "80:localhost:8501",
        "nokey@localhost.run"
    ]

    ssh_proc = subprocess.Popen(
        ssh_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1
    )

    public_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.lhr\.life")

    for line in iter(ssh_proc.stdout.readline, ""):
        # Ignore documentation links
        if "admin.localhost.run" in line or "localhost.run/docs" in line:
            continue

        match = url_pattern.search(line)
        if match:
            public_url = match.group(0)
            break

    if public_url:
        print("", flush=True)
        print("*" * 70, flush=True)
        print("🎉 SUCCESS! EVIDENCEBOT IS NOW LIVE AND ACCESSIBLE WORLDWIDE:", flush=True)
        print(f"👉 PUBLIC URL: {public_url}", flush=True)
        print("*" * 70, flush=True)
        print("", flush=True)
        print("Anyone with this link can now open EvidenceBot directly in their browser!", flush=True)

        with open(PUBLIC_URL_FILE, "w", encoding="utf-8") as f:
            f.write(public_url)
    else:
        print("⚠️ Could not detect tunnel URL automatically.", flush=True)

    try:
        while True:
            time.sleep(1)
            if st_proc.poll() is not None:
                print("Streamlit process stopped.", flush=True)
                break
            if ssh_proc.poll() is not None:
                print("SSH tunnel stopped.", flush=True)
                break
    except KeyboardInterrupt:
        print("\nShutting down...", flush=True)
    finally:
        st_proc.terminate()
        ssh_proc.terminate()


if __name__ == "__main__":
    main()
