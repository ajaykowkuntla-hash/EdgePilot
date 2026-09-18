import os
import random
import shutil

def convert_to_yolo(txt_path, img_width, img_height):
    yolo_lines = []
    if not os.path.exists(txt_path):
        return []
        
    with open(txt_path, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
            
        x1, y1, x2, y2, type_id = map(float, parts)
        type_id = int(type_id)
        
        # Original: 1-open, 2-short, 3-mousebite, 4-spur, 5-copper, 6-pin-hole
        # YOLO: 0-indexed (0 to 5)
        if type_id < 1 or type_id > 6:
            continue
            
        yolo_class_id = type_id - 1
        
        # Calculate YOLO format (normalized cx, cy, w, h)
        cx = ((x1 + x2) / 2.0) / img_width
        cy = ((y1 + y2) / 2.0) / img_height
        w = (x2 - x1) / img_width
        h = (y2 - y1) / img_height
        
        # Ensure values are within [0, 1]
        cx = max(0.0, min(1.0, cx))
        cy = max(0.0, min(1.0, cy))
        w = max(0.0, min(1.0, w))
        h = max(0.0, min(1.0, h))
        
        yolo_lines.append(f"{yolo_class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n")
        
    return yolo_lines

def main():
    source_dir = "/tmp/DeepPCB/PCBData"
    dest_dir = "/Users/ajaykowkuntla/Desktop/New Pro/app/data/deeppcb_subset"
    
    # Read trainval.txt and test.txt
    trainval_path = os.path.join(source_dir, "trainval.txt")
    test_path = os.path.join(source_dir, "test.txt")
    
    with open(trainval_path, 'r') as f:
        train_lines = f.readlines()
        
    with open(test_path, 'r') as f:
        test_lines = f.readlines()
        
    # We want a small subset. Let's take 40 train and 10 val images.
    # To ensure it's "stratified", we'll just randomly sample for now. 
    # Because defects are dense (3-12 per image), a random sample of 40 will contain all classes.
    random.seed(42)
    sample_train = random.sample(train_lines, 40)
    sample_val = random.sample(test_lines, 10)
    
    # Setup directories
    os.makedirs(os.path.join(dest_dir, "images", "train"), exist_ok=True)
    os.makedirs(os.path.join(dest_dir, "images", "val"), exist_ok=True)
    os.makedirs(os.path.join(dest_dir, "labels", "train"), exist_ok=True)
    os.makedirs(os.path.join(dest_dir, "labels", "val"), exist_ok=True)
    
    def process_split(lines, split_name):
        counts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
        total_images = 0
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
                
            img_rel_path, txt_rel_path = parts
            
            # The img path in txt is like 'group20085/20085/20085000.jpg'
            # The actual defective image is 'group20085/20085/20085000_test.jpg'
            img_base = img_rel_path.replace('.jpg', '')
            actual_img_path = os.path.join(source_dir, f"{img_base}_test.jpg")
            actual_txt_path = os.path.join(source_dir, txt_rel_path)
            
            if not os.path.exists(actual_img_path) or not os.path.exists(actual_txt_path):
                print(f"Missing: {actual_img_path} or {actual_txt_path}")
                continue
                
            yolo_lines = convert_to_yolo(actual_txt_path, 640, 640)
            
            if len(yolo_lines) == 0:
                continue
                
            # Update counts
            for yline in yolo_lines:
                cid = int(yline.split()[0])
                counts[cid] += 1
                
            img_filename = os.path.basename(actual_img_path)
            txt_filename = img_filename.replace('.jpg', '.txt')
            
            dest_img = os.path.join(dest_dir, "images", split_name, img_filename)
            dest_txt = os.path.join(dest_dir, "labels", split_name, txt_filename)
            
            shutil.copy(actual_img_path, dest_img)
            with open(dest_txt, 'w') as f:
                f.writelines(yolo_lines)
                
            total_images += 1
            
        print(f"{split_name.capitalize()} Split - Images: {total_images}, Classes: {counts}")
    
    process_split(sample_train, "train")
    process_split(sample_val, "val")
    
    # Create YAML
    yaml_content = f"""path: {dest_dir}
train: images/train
val: images/val

names:
  0: open
  1: short
  2: mousebite
  3: spur
  4: copper
  5: pin-hole
"""
    with open(os.path.join(dest_dir, "dataset.yaml"), "w") as f:
        f.write(yaml_content)

if __name__ == "__main__":
    main()
