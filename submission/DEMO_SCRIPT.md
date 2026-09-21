# EdgePilot Demo Script

**0:00–0:20: Problem**
"Micro, Small, and Medium Enterprises often lack the ML expertise and expensive hardware required to automate repetitive visual inspection tasks. Setting up computer vision pipelines is historically too complex for a standard factory floor manager."

**0:20–0:40: Introduce EdgePilot**
"This is EdgePilot: an AI automation platform built specifically for the edge. EdgePilot provides a guided, 8-step workflow that abstracts away ML complexity, allowing business owners to configure, train, and deploy task-specific AI using their own domain data."

**0:40–1:10: Configure inspection**
"Let's create a new inspection. We start by defining the business requirement—in this case, detecting defects on a manufacturing line. EdgePilot maps this to a specific ML task behind the scenes. We then set a simple business rule, like 'Reject if any defect is detected above 70% confidence.'"

**1:10–1:35: Upload dataset / AutoML workflow**
"Next, we upload a ZIP file of our business data. EdgePilot's automated pipeline takes over. It validates the data, handles the training of a task-specific YOLOv8 Nano model, and evaluates the results—all without exposing complex hyperparameters to the user."

**1:35–1:55: ONNX deployment**
"Once training is complete, EdgePilot automatically exports the model to the ONNX runtime format. This guarantees that our task-specific model is portable and optimized for edge deployment."

**1:55–2:20: Show Qualcomm AI Hub Snapdragon NPU evidence**
"To guarantee performance, EdgePilot models are validated against real hardware. Here on the Performance page, you can see our hosted Qualcomm AI Hub validations. For this fresh model, we achieved 5.8 milliseconds of latency on a Snapdragon X Elite NPU, proving that this workflow generates highly efficient, edge-ready AI."

**2:20–2:45: Run local inference and show business decision**
"Finally, we can test the model. Using our local ONNX runtime for demonstration, we pass an image through the pipeline. The model detects the defect, and our business decision layer applies the rule we set earlier, resulting in a clear 'REJECT' decision."

**2:45–3:00: Final value proposition**
"EdgePilot converts business-specific inspection data into task-specific ONNX models, and validates those artifacts on Snapdragon hardware. It delivers powerful edge AI, made simple for business owners."
