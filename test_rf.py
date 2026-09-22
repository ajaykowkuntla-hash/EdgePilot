try:
    from roboflow import Roboflow
    rf = Roboflow(api_key="PUBLIC_WORKSPACE_API_KEY") # Usually public datasets can be downloaded with a public key or without one, but mostly needs one.
    project = rf.workspace("spark-intelligence").project("bottle-defect-detection-k7o4h")
    version = project.version(1)
    dataset = version.download("yolov8")
    print("Downloaded!")
except Exception as e:
    print("Error:", e)
