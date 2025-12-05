# Quick Demo Script - Subsystem 5

## 1. Quick Setup

```powershell
cd codigo
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Complete Execution (Recommended)

```powershell
python run_complete_automation.py
```

The script automatically executes:
1. Environment and model verification.
2. Evidence generation (GIFs + screenshots + metrics).
3. Documentation update.
4. Quick tests execution.
5. Packaging in `ENTREGA_FINAL/`.

## 3. Manual Execution by Stages (Advanced)

```powershell
# Train quick model
python simple_cnn.py

# Test model
python test_model.py

# Generate visual evidence
python generate_evidence.py

# Update documentation
python update_documentation.py
```

## 4. Results Visualization

- Evidence: `evidencias/`
- Models: `modelos/`
- Consolidated final delivery: `ENTREGA_FINAL/`
