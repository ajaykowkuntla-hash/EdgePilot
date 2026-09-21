import os
import yaml

def validate_dataset(dataset_path):
    """
    Validates a YOLO-format object detection dataset.

    Args:
        dataset_path (str): The root directory of the dataset.

    Returns:
        dict: A structured result containing:
            - is_valid (bool): Overall validation status.
            - checks (list): List of strings describing passed checks.
            - errors (list): List of strings describing failed checks or issues.
            - num_train_images (int)
            - num_val_images (int)
            - num_classes (int)
    """
    result = {
        "is_valid": False,
        "checks": [],
        "errors": [],
        "num_train_images": 0,
        "num_val_images": 0,
        "num_classes": 0
    }

    # 1. Check if dataset directory exists
    if not os.path.exists(dataset_path):
        result["errors"].append(f"Dataset directory not found: {dataset_path}")
        return result
    result["checks"].append("Dataset directory found")

    # 2. Check for data.yaml
    yaml_path = os.path.join(dataset_path, "data.yaml")
    if not os.path.exists(yaml_path):
        # Allow dataset.yaml as an alternative
        yaml_path = os.path.join(dataset_path, "dataset.yaml")

    if not os.path.exists(yaml_path):
        result["errors"].append("Missing data.yaml or dataset.yaml")
        return result

    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        result["errors"].append(f"Failed to parse YAML: {str(e)}")
        return result

    result["checks"].append(f"YAML configuration found: {os.path.basename(yaml_path)}")

    # Check classes
    if 'names' not in data:
        result["errors"].append("YAML missing 'names' (class names)")
        return result

    num_classes = len(data['names'])
    if num_classes == 0:
        result["errors"].append("YAML 'names' list is empty")
        return result

    result["num_classes"] = num_classes
    result["checks"].append(f"{num_classes} classes defined")

    # 3. Check train and val paths
    if 'train' not in data or 'val' not in data:
        result["errors"].append("YAML missing 'train' or 'val' paths")
        return result

    # Helper to resolve and check image/label paths
    def check_split(split_name, rel_path):
        split_path = os.path.join(dataset_path, rel_path)
        if not os.path.exists(split_path):
            result["errors"].append(f"Missing {split_name} path: {rel_path}")
            return 0

        # Determine labels path based on common YOLO structure (replace images/ with labels/)
        if "images" in split_path:
            labels_path = split_path.replace("images", "labels")
        else:
            # Fallback if structure is different
            labels_path = os.path.join(dataset_path, "labels", split_name)

        if not os.path.exists(labels_path):
            result["errors"].append(f"Missing labels path corresponding to {split_name} images")
            return 0

        # Count images and validate random label format
        valid_image_exts = {'.jpg', '.jpeg', '.png'}
        images = [f for f in os.listdir(split_path) if os.path.splitext(f)[1].lower() in valid_image_exts]

        if len(images) == 0:
            result["errors"].append(f"No valid images found in {split_path}")
            return 0

        # Sample validation of labels (just check the first up to 10 labels if they exist)
        labels_checked = 0
        malformed_count = 0
        for img in images[:10]:
            base = os.path.splitext(img)[0]
            label_file = os.path.join(labels_path, base + ".txt")
            if os.path.exists(label_file):
                labels_checked += 1
                try:
                    with open(label_file, 'r') as lf:
                        lines = lf.readlines()
                        for line in lines:
                            parts = line.strip().split()
                            if len(parts) == 0: continue
                            if len(parts) != 5:
                                malformed_count += 1
                                continue
                            class_id, x, y, w, h = map(float, parts)
                            if int(class_id) < 0 or int(class_id) >= num_classes:
                                malformed_count += 1
                            if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0 and 0.0 <= w <= 1.0 and 0.0 <= h <= 1.0):
                                malformed_count += 1
                except Exception:
                    malformed_count += 1

        if malformed_count > 0:
            result["errors"].append(f"Found malformed YOLO annotations or invalid class IDs in {split_name} labels")

        return len(images)

    train_count = check_split('train', data['train'])
    val_count = check_split('val', data['val'])

    result["num_train_images"] = train_count
    result["num_val_images"] = val_count

    if train_count > 0:
        result["checks"].append(f"{train_count} training images found")
    if val_count > 0:
        result["checks"].append(f"{val_count} validation images found")

    if train_count == 0 or val_count == 0:
        result["errors"].append("Dataset must contain at least one training and one validation image.")

    # Check overall validity
    if len(result["errors"]) == 0:
        result["is_valid"] = True
        result["checks"].append("YOLO annotations valid")

    return result
