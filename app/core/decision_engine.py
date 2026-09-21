def evaluate_inspection(detections, confidence_threshold, business_decision_action):
    """
    Evaluates the detections against the business threshold.

    Args:
        detections (list): List of detected bounding box dictionaries with a 'confidence' key.
        confidence_threshold (float): Minimum confidence required to trigger a decision.
        business_decision_action (str): The configured business decision (e.g. "Reject defective product").

    Returns:
        tuple: (decision (str), details (str))
    """
    # Filter detections by the confidence threshold set by the business user
    valid_detections = [d for d in detections if d['confidence'] >= confidence_threshold]

    if not valid_detections:
        return "PASS", "No defects detected above the confidence threshold."

    # If we have valid detections, apply the business decision
    if "Reject" in business_decision_action:
        return "REJECT", f"{len(valid_detections)} defect(s) detected above {confidence_threshold} confidence."
    elif "Alert" in business_decision_action:
        return "ALERT", f"Review required: {len(valid_detections)} defect(s) detected."
    else:
        # Default action
        return "REJECT", f"{len(valid_detections)} defect(s) detected."
