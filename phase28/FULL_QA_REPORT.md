# EdgePilot Full QA Report

## 1. Test Environment

*   **OS:** macOS Darwin (arm64)
*   **Python:** 3.14.6 (Virtual Environment)
*   **Browser:** Headless Chrome (via browser subagent), Playwright
*   **Application URL:** `http://localhost:8501`
*   **Git commit:** `5db89d1c07bd27d153a1c7573a870ac0bd92a65f`
*   **Testing date/time:** 2026-09-27

## 2. Executive Summary

*   **Total tests performed:** 20
*   **Passed:** 12
*   **Failed:** 4
*   **Blocked:** 2
*   **Critical issues:** 1
*   **High issues:** 2
*   **Medium issues:** 2
*   **Low issues:** 1

**Major successful workflows:** Authentication flow, Foundation baseline generation, Deployment Candidate (Snapdragon) visualization, and single-image Live Inference.

## 3. Complete Test Matrix

| Test | Result | Evidence | Issue | Severity |
| :--- | :--- | :--- | :--- | :--- |
| 1. Authentication | PASS | Logged in via Firebase | None | N/A |
| 2. Dashboard | PASS | Responsive, navigated successfully | None | N/A |
| 3. Business Workflow | PARTIAL| Navigated using 'Component Inspection' | UI Text Hardcoding | HIGH |
| 4. Business Examples | PASS | Enforces ZIP upload gate | None | N/A |
| 5. Adaptation / AutoML | PASS | Evaluated metrics | None | N/A |
| 6. Model Readiness | PASS | Displayed `MORE_DATA_RECOMMENDED` | None | N/A |
| 7. Snapdragon Validation| PASS | Clearly separated AI Hub metrics | None | N/A |
| 8. Image Inspection | PASS | Detected `pitted_surface` correctly | None | N/A |
| 9. Video Inspection | FAIL | Feature cannot be located in UI | Missing Feature | HIGH |
| 10. Reports | PASS | Displayed full trace | None | N/A |
| 11. Settings / Account | FAIL | Streamlit Exception on Save | Firestore Document Conflict | CRITICAL |
| 12. Help | FAIL | Cannot locate Help section | Missing Feature | LOW |
| 13. Nav Stress Test | PASS | No infinite loops | None | N/A |
| 14. Session Retention | FAIL | Refreshing browser wipes workflow | State Lost on Reload | MEDIUM |
| 15. Error Handling | PASS | Adaptation gracefully handles errors | None | N/A |
| 16. UI/UX Audit | PARTIAL| See Bug ID-02 | Hardcoded 'defects' | MEDIUM |
| 17. Security | PASS | Auth strictly required | None | N/A |
| 18. Performance | PASS | Responsive UI, fast transitions | None | N/A |
| 19. Automated Tests | PASS | 13/13 passed | None | N/A |
| 20. Final User Journey | PARTIAL| Reached live inference, but no video | Blocked by missing video| HIGH |

## 4. Authentication
*   **Result:** PASS
*   **Findings:** Firebase Email/Password login works seamlessly. Attempting to navigate to the app via direct URL without logging in safely redirects to the login view. No API secrets were exposed in the UI.

## 5. Dashboard
*   **Result:** PASS
*   **Findings:** The dashboard successfully lists the active workflow options and available categories. Clicking 'Start Inspection' correctly redirects the user to the interactive wizard.

## 6. Business Automation Workflow
*   **Result:** PARTIAL
*   **Findings:** Evaluated the workflow using the non-default **Component Inspection** category. The workflow successfully transitions from Step 1 to Step 2, identifying the relevant foundation data. However, Step 3 suffers from hardcoded UI text specific to defect inspection (see Bug ID-02).

## 7. AutoML / Adaptation
*   **Result:** PASS
*   **Findings:** The workflow cleanly waits for adaptation and outputs the empirical metrics (mAP50). Crucially, the app correctly states `MORE_DATA_RECOMMENDED` without misleading the user into thinking the model is production-ready. 

## 8. Image Inspection
*   **Result:** PASS
*   **Findings:** Live inference processes uploaded images successfully, drawing bounding boxes and assigning confidence scores correctly.

## 9. Video Inspection
*   **Result:** FAIL
*   **Findings:** The UI does not provide any capability to upload or stream a video file for inspection. Users can only upload static images.

## 10. Snapdragon Validation
*   **Result:** PASS
*   **Findings:** The deployment candidate page accurately reflects the 5.299 ms latency and clearly attributes this to Qualcomm AI Hub hosted validation, preventing false claims about local Snapdragon hardware execution.

## 11. Reports
*   **Result:** PASS
*   **Findings:** The trace chain successfully logs the model readiness metrics, AI Hub profiles, and business decision outcomes.

## 12. Navigation / Session
*   **Result:** FAIL (Refresh)
*   **Findings:** Because state relies entirely on Streamlit's ephemeral `st.session_state`, hitting "Refresh" in the browser completely deletes the user's progress mid-wizard, returning them to the dashboard.

## 13. Error Handling
*   **Result:** PASS
*   **Findings:** The application fails gracefully when models are missing (thanks to Phase 26 updates). No raw Python tracebacks are exposed to the user during the main workflow.

## 14. Security
*   **Result:** PASS
*   **Findings:** Verified that the Firebase Authentication gates prevent unauthenticated access. 

## 15. Automated Tests
*   **Command:** `.venv/bin/pytest -q`
*   **Result:** `13 passed in 0.16s`
*   **Command:** `.venv/bin/python -m py_compile app.py app/**/*.py`
*   **Result:** `0` (Success)

## 16. Bugs

### ID-01: Settings Page Crash
*   **Severity:** CRITICAL
*   **Category:** Backend / State
*   **Steps to reproduce:** Navigate to Settings, modify a field, and click Save.
*   **Expected behavior:** User preferences are updated.
*   **Actual behavior:** The application throws a raw Python Traceback pointing to a Firestore `AlreadyExists` or permission error, breaking the UI.
*   **Recommended fix:** Ensure `set()` with `merge=True` is used in the Firestore SDK instead of `create()`.

### ID-02: Hardcoded 'Defect' Terminology
*   **Severity:** MEDIUM
*   **Category:** UI/UX
*   **Steps to reproduce:** Start a new inspection for 'Counting & Presence Detection' or 'Component Inspection'. Proceed to Step 3.
*   **Expected behavior:** The instructions should dynamically ask for examples relevant to the selected task (e.g., "Upload examples of components").
*   **Actual behavior:** The text statically states: *"Show EdgePilot examples of the defects you want to detect."*
*   **Recommended fix:** Parameterize the instructions based on the selected category's primary objective.

### ID-03: Session Wipe on Refresh
*   **Severity:** MEDIUM
*   **Category:** UX / State Management
*   **Steps to reproduce:** Reach Step 4 of the wizard. Refresh the browser.
*   **Expected behavior:** User resumes at Step 4.
*   **Actual behavior:** User is kicked to the Dashboard and progress is lost.
*   **Recommended fix:** Persist active workflow ID to Firestore or local storage.

## 17. Missing Features
*   **Video Inspection:** The application currently lacks the ability to process continuous video streams or `.mp4` file uploads.
*   **Help / Documentation UI:** There is no user-facing Help or Tutorial section within the application to guide first-time MSME users.

## 18. Known Limitations
*   **Local Hardware Execution:** The inference runs on the local Mac CPU (ONNX Runtime), while the 5.299 ms latency claim represents hosted Snapdragon validation metrics.
*   **Model Accuracy:** The 25-shot adaptation is an MVP POC; it correctly warns the user that more data is required.

## 19. Judge Risk
*   **HIGH RISK:** If a judge navigates to the Settings page and attempts to save changes, the app will crash with a red Streamlit traceback.
*   **HIGH RISK:** If a judge asks to see a video processing demo, the app currently has no mechanism to accept video input, failing to meet continuous-inspection expectations.
*   **MEDIUM RISK:** If a judge refreshes their browser mid-workflow, they will lose all progress and have to restart.

## 20. Recommended Fix Order

1. **CRITICAL:** Fix the Settings page Firestore crash (ID-01).
2. **HIGH:** Implement Video Inspection functionality (Missing Feature).
3. **MEDIUM:** Fix the hardcoded "defect" terminology in Step 3 (ID-02).
4. **MEDIUM:** Implement URL-parameter or Firestore-backed session recovery (ID-03).
5. **LOW:** Add a basic Help module to the sidebar.
