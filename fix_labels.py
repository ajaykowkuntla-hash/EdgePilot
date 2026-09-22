import os
import glob

def fix_dir(path):
    for txt_file in glob.glob(os.path.join(path, "*.txt")):
        with open(txt_file, "r") as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if not parts: continue
            # map all classes to 0, 1, or 2 based on modulo
            new_cls = int(parts[0]) % 3
            parts[0] = str(new_cls)
            new_lines.append(" ".join(parts) + "\n")
            
        with open(txt_file, "w") as f:
            f.writelines(new_lines)

fix_dir("phase9/dataset_b/labels/train")
fix_dir("phase9/dataset_b/labels/val")

print("Labels fixed.")
