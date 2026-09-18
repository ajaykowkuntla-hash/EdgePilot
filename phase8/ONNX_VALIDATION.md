# ONNX Validation

This document compares the inference performance and output between the existing PyTorch model and the exported ONNX model on the local Mac environment using `pitted_surface_277.jpg`.

## PyTorch Result
- **Detection**: `pitted_surface`
- **Confidence**: 0.8660
- **Inference Time**: ~397.1 ms
- **Threshold**: 0.70

## ONNX Result
- **Detection**: `pitted_surface`
- **Confidence**: 0.8660
- **Inference Time**: ~110.8 ms
- **Threshold**: 0.70

## Analysis
The ONNX Runtime pipeline via Ultralytics perfectly replicates the PyTorch inference pipeline, including preprocessing and NMS post-processing. The detection class and confidence scores are numerically identical up to 4 decimal places. 

As expected, executing ONNX locally via CPU execution provider is faster than PyTorch CPU execution (~110 ms vs ~397 ms), demonstrating the inherent efficiency of the ONNX format even before NPU acceleration is applied.

No numerical drift or compatibility blockers were encountered. The Streamlit UI has been successfully migrated to use the `best.onnx` model by default.
