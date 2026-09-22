import os
import shutil

target_dir = "phase9/dataset_b"
os.makedirs(target_dir, exist_ok=True)
if os.path.exists(f"{target_dir}/images"):
    shutil.rmtree(f"{target_dir}/images")
if os.path.exists(f"{target_dir}/labels"):
    shutil.rmtree(f"{target_dir}/labels")

shutil.copytree("coco8/images", f"{target_dir}/images")
shutil.copytree("coco8/labels", f"{target_dir}/labels")

data_yaml_content = f"""
path: {os.path.abspath(target_dir)}
train: images/train
val: images/val

names:
  0: Free
  1: Cap
  2: Crumbled
"""
with open(f"{target_dir}/data.yaml", "w") as f:
    f.write(data_yaml_content)

print("Dataset prepared at phase9/dataset_b")
