# EdgePilot: Dataset Discovery Architecture (Phase 20)

## 1. Why EdgePilot Needs Dataset Discovery
EdgePilot provides predefined foundations (like YOLOv8n + NEU-DET for steel) for common industrial inspection tasks. However, manufacturing defects span countless domains. When a user creates a new automation category (e.g., Packaging Inspection), EdgePilot cannot rely on hardcoded datasets. The Dataset Discovery Engine allows EdgePilot to safely discover, filter, and propose relevant public datasets for novel user tasks.

## 2. Supported Sources
The discovery engine uses a unified `DatasetSource` interface. 
- **HuggingFaceSource:** Currently implemented. Queries the public HF Datasets API.
- **RoboflowSource:** Scaffolded but marked unavailable for live unauthenticated requests (requires API keys which are not safely bundled in the public app).
- **GitHubSource:** Scaffolded but marked unavailable due to unauthenticated rate limits.
- **MockSource:** Included explicitly for deterministic testing.

## 3. Normalized Dataset Schema
Every discovered candidate is normalized to the following standard schema before being evaluated:
- `name`: Identifier of the dataset.
- `source`: The origin platform (e.g., Hugging Face).
- `source_url`: Link to the dataset.
- `description`: Text description.
- `task_type`: e.g., "Object Detection".
- `domain`: e.g., "Industrial".
- `classes`: Number of classes (if available).
- `annotation_format`: e.g., "YOLO", "COCO".
- `license`: Extracted license string.
- `license_url`: Link to license details.
- `image_count`: Estimated size (if available).
- `model_available`: Boolean indicating if a pretrained model is linked.
- `model_format`: Format of the model (if available).
- `lightweight_model_compatible`: Boolean indicating compatibility with YOLO-nano.
- `discovery_timestamp`: Unix timestamp of discovery.
- `status`: One of `review_required`, `incompatible`, `license_unknown`, `approved`.

## 4. License States & Handling
This is the most critical safety mechanism. Just because a dataset is "publicly downloadable" does not mean EdgePilot can use it commercially.
- **`incompatible`**: Datasets with `-NC` (Non-Commercial) clauses are explicitly rejected.
- **`license_unknown`**: If the source does not provide a license, it is flagged as unknown and cannot be used for commercial foundations.
- **`review_required`**: Datasets with permissive licenses (MIT, Apache, CC BY) are flagged for review. **The engine NEVER auto-approves external datasets** without a human-in-the-loop validation step.
- **`approved`**: Only explicitly vetted datasets (or deterministic mock tests) achieve this status.

## 5. Compatibility Rules
Beyond licensing, candidates are filtered based on ML viability:
- **Task Type**: Must be "Object Detection" (or Unknown/extrapolated). Image Classification datasets are marked `incompatible`.
- **Lightweight Suitability**: The dataset must be compatible with bounding-box regression tasks suited for YOLOv8-N.

## 6. Security Restrictions
- **No execution:** The engine parses JSON metadata only. It does not download or execute any Python scripts or GitHub repositories.
- **No blind training:** Discovered datasets are presented as *candidates*. No automatic downloading or YOLO training occurs in Phase 20.

## 7. What Is Implemented
- The `DatasetDiscoveryEngine` abstracting source querying and caching.
- Hugging Face integration via public API.
- Compatibility and License filtering logic.
- UI integration: New categories correctly show the "No Validated Foundation" warning and trigger the discovery workflow.
- Candidate rendering cards in the Streamlit UI.

## 8. What Is NOT Implemented
- Automatic downloading of datasets.
- Automatic training on discovered datasets.
- Automatic deployment of discovered models.
- Deep web scraping (all discovery is strictly via official APIs).

## 9. Next Steps (Phase 21)
Phase 21 will build upon this foundation by implementing the workflow to securely acquire an *approved* candidate dataset, format it into the expected YOLO structure, and initiate the few-shot training pipeline demonstrated in Phase 19.

**Phase 20 discovers candidate datasets/models. It does not automatically train or deploy them.**
