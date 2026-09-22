import zipfile
import os
import shutil

# Create a malicious ZIP
malicious_zip = "malicious.zip"
with zipfile.ZipFile(malicious_zip, 'w') as z:
    # Add a normal file
    z.writestr("normal.txt", "This is normal.")
    # Add a malicious file
    z.writestr("../escape.txt", "This is malicious.")

dest_dir = "test_extract"
if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)
os.makedirs(dest_dir)

try:
    with zipfile.ZipFile(malicious_zip, 'r') as z:
        dest_dir_abs = os.path.abspath(dest_dir)
        for member in z.infolist():
            member_path = os.path.join(dest_dir_abs, member.filename)
            # We must be careful about Python 3 zipfile stripping leading slashes or resolving ..
            # Actually, standard ZipFile strips `../` unless extract is passed a dangerous path.
            # But just in case, we do the check.
            resolved = os.path.abspath(member_path)
            if resolved.startswith(dest_dir_abs + os.sep) or resolved == dest_dir_abs:
                z.extract(member, dest_dir_abs)
                print(f"Extracted {member.filename}")
            else:
                print(f"BLOCKED: {member.filename} attempts path traversal")
except Exception as e:
    print("Error:", e)

print("Is escape.txt present?", os.path.exists("escape.txt"))

os.remove(malicious_zip)
if os.path.exists("escape.txt"):
    os.remove("escape.txt")
shutil.rmtree(dest_dir)
