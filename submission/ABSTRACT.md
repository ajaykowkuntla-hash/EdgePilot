# Abstract

Micro, Small, and Medium Enterprises (MSMEs) struggle with AI adoption for repetitive visual inspection tasks. Existing solutions often require specialized machine learning expertise, complex cloud infrastructure, and expensive hardware. EdgePilot resolves these barriers by providing a simple, business-driven configuration workflow that abstracts away ML complexity.

EdgePilot allows users to define business rules and upload task-specific business data, which is then automatically converted into a task-specific AI model via a streamlined AutoML pipeline. The resulting model is exported to the ONNX format, bridging the gap between local configuration and edge deployment. EdgePilot validates deployment on the Snapdragon X Elite NPU via the hosted Qualcomm AI Hub, ensuring that the generated models achieve performant, localized edge intelligence.

The current EdgePilot prototype serves as a validation and demonstration platform. We demonstrate actual measured results for three distinct inspection tasks, achieving consistent latency below 6.0 milliseconds on the Snapdragon X Elite NPU, proving that EdgePilot can successfully convert business data into highly efficient, task-specific edge inference workloads.
