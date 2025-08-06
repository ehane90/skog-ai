import os
import shutil
import sys
import subprocess

# 🛠️ KONFIGURATION
REMOTE_HOST = "ubuntu@207.127.92.131"
REMOTE_PATH = "/home/ubuntu/skog-ai/docs/"
SSH_KEY_PATH = os.path.expanduser("~/.ssh/oracle-skog-ai.pem")

def list_existing_files(remote_path):
    """Hämtar lista över redan uppladdade filer på servern via 
SSH"""
    try:
        result = subprocess.check_output([
            "ssh", "-i", SSH_KEY_PATH, f"{REMOTE_HOST}",
            f"ls {remote_path}"
        ]).decode("utf-8").splitlines()
        return set(result)
    except subprocess.CalledProcessError:
        print("⚠️ Kunde inte hämta lista över existerand dokument.")
        return set()

def main(local_folder):
    if not os.path.isdir(local_folder):
        print(f"❌ Mappen finns inte: {local_folder}")
        return

    allowed_exts = (".pdf", ".docx", ".xls", ".xlsx")
    local_files = [f for f in os.listdir(local_folder) if 
f.lower().endswith(allowed_exts)]
    if not local_files:
        print("📂 Inga giltiga filer hittades att ladda upp.")
        return

    print("📡 Hämtar lista över befintliga dokument på servern...")
    existing_remote = list_existing_files(REMOTE_PATH)

    for f in local_files:
        if f in existing_remote:
            print(f"⏭️  Hoppar över (redan finns på server): {f}")
            continue

        full_path = os.path.join(local_folder, f)
        print(f"⬆️  Laddar upp: {f}")
        try:
            subprocess.check_call([
                "scp", "-i", SSH_KEY_PATH,
                full_path,
                f"{REMOTE_HOST}:{REMOTE_PATH}"
            ])
        except subprocess.CalledProcessError:
            print(f"⚠️  Kunde inte ladda upp: {f}")

    print("✅ Klart!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Användning: python upload_docs.py /sökväg/till/mapp")
    else:
        main(sys.argv[1])

