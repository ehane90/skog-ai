import os
import hashlib
import shutil

# Ange källmapp (lokalt) och mål (tillfällig lokal mapp för uppladdning)
SOURCE_FOLDER = "/Users/erikhane/Documents/skogsdokument"
TARGET_FOLDER = "/Users/erikhane/Documents/upload_to_server"

# Skapa mål om det inte finns
os.makedirs(TARGET_FOLDER, exist_ok=True)

def file_hash(path):
    """Returnerar SHA256-hash för att identifiera dubbletter 
baserat på innehåll."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

# Hämta befintliga filhashar i mål
existing_hashes = set()
for f in os.listdir(TARGET_FOLDER):
    full_path = os.path.join(TARGET_FOLDER, f)
    if os.path.isfile(full_path):
        existing_hashes.add(file_hash(full_path))

# Kopiera nya filer
new_files = 0
for f in os.listdir(SOURCE_FOLDER):
    full_path = os.path.join(SOURCE_FOLDER, f)
    if not os.path.isfile(full_path):
        continue
    h = file_hash(full_path)
    if h in existing_hashes:
        print(f"🔁 Dubblett, hoppar över: {f}")
        continue
    shutil.copy2(full_path, os.path.join(TARGET_FOLDER, f))
    new_files += 1
    print(f"✅ Lagt till: {f}")

print(f"\n📦 Totalt {new_files} nya filer redo att laddas upp.")

