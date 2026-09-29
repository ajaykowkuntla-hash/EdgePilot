import streamlit as st
from app.ui.components import page_header

def render():
    page_header(
        eyebrow="DOCUMENTATION",
        title="Help & Support",
        description="Learn how to use EdgePilot and understand its capabilities."
    )

    st.markdown("""
### What is EdgePilot?
EdgePilot is an automated visual inspection platform for MSMEs. It allows you to select a foundation model, adapt it to your specific business requirements with a few examples, and deploy it to the edge (e.g., Snapdragon NPU).

### Creating an Inspection
To create a new inspection, go to the Dashboard and click **Start Inspection**. You will be guided through a wizard to select your category and provide data.

### Business Examples
When prompted, provide ZIP files containing images relevant to your task (e.g., defect examples for Product Defect Inspection, or component examples for Component Inspection). These examples adapt the foundation workflow to your use case.

### Adaptation
During Adaptation, EdgePilot fine-tunes a lightweight model using your examples. This process validates if the provided examples are sufficient to achieve measurable improvement over the foundation baseline.

### Model Readiness
Model Readiness gives you a clear indication of whether your adapted model is ready for deployment. If the status is `MORE EXAMPLES RECOMMENDED`, you should provide more data to improve accuracy.

### Snapdragon Validation
EdgePilot validates your deployment candidate on Qualcomm AI Hub using a hosted Snapdragon X Elite NPU. The latency and memory metrics provided represent this hosted environment. (Note: The metrics do not imply local NPU execution on this device).

### Image Inspection
You can test your model live by uploading static images. The system will run inference, draw bounding boxes, and make PASS/REJECT business decisions based on your configuration.

### Video Inspection
For continuous monitoring tasks, you can upload video files (.mp4 or .avi). EdgePilot will extract frames, run inference, and provide results just like static images.

### Reports
All inspection results, adaptation metrics, and Snapdragon validation chains are saved in the Reports tab for auditing and review.

### Limitations
- **Local Execution:** Live inference is currently executed on the local CPU (ONNX Runtime) rather than a physical NPU.
- **Video Processing:** Video inspection currently extracts static frames for analysis.
- **Production Readiness:** EdgePilot provides technical validation. It does not certify models for physical factory deployment or guarantee business cost savings without field testing.
    """)
