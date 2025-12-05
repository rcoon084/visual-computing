# Subsystem 5: CNN Model Training and Comparison

## Advanced Visual Computing Workshop - Subsystem 5

**TensorFlow 2.13+** | **Python 3.13** | **Keras Deep Learning**

---

## Description

Specialized subsystem for **Deep Learning model training and comparison** for image classification. Developed as part of the Advanced Visual Computing Workshop.

### Implemented Features:

- Simple CNN Model - Lightweight model for limited hardware (156K parameters)
- Automated Training Pipeline - Complete training and evaluation workflow
- Performance Metrics - Comprehensive evaluation system
- Visual Evidence Generation - Automated GIF and plot creation
- Complete Documentation - Technical guides and references

---

## Main Features

### 1. Custom CNN Training
- Deep architecture with 3 convolutional blocks
- Batch Normalization and Dropout
- Early Stopping and Learning Rate Scheduling
- Complete metrics (Accuracy, Precision, Recall, AUC)

### 2. Performance Analysis
- Automatic comparison between classes
- Visualizations:
  - Training history graphs
  - Confusion matrices
  - ROC curves
  - Prediction samples

### 3. Evidence Automation
- `python run_complete_automation.py` executes the end-to-end pipeline
- Generates and records 2+ GIFs and metrics
- Automatically updates documents
- Packages the `ENTREGA_FINAL/` folder

---

## Project Structure

```
ENTREGA_FINAL/
├── codigo/
│   ├── simple_cnn.py              # CNN training
│   ├── test_model.py              # Model testing
│   ├── generate_evidence.py       # Evidence generation
│   ├── update_documentation.py    # Doc updates
│   ├── run_complete_automation.py # Full pipeline
│   └── requirements.txt           # Dependencies
├── modelos/
│   └── simple_cnn_20251204_202143.h5  # Trained model
├── plots/
│   ├── simple_cnn_history_20251204_202143.png
│   └── random_samples_20251204_220401.png
├── evidencias/
│   └── gifs/
│       ├── 01_training_progress_20251204_232926.gif
│       └── 02_predictions_20251204_232926.gif
├── metrics/
│   ├── latest_metrics.json
│   └── latest_evidence_manifest.json
└── documentacion/
    ├── README.md                  # System overview
    ├── ESTADO_PROYECTO.md         # Project status
    ├── EVIDENCIAS.md              # Evidence documentation
    ├── ARCHITECTURE.md            # System architecture
    ├── METRICAS.md                # Metrics reference
    ├── QUICK_DEMO.md              # Quick demo guide
    └── RUTINAS_DEMO.md            # Demo routines
```

---

## Quick Start

### Prerequisites

```powershell
# Python 3.13 (recommended) or 3.10+
python --version

# Navigate to directory
cd ENTREGA_FINAL\codigo

# Install dependencies
pip install -r requirements.txt
```

### Step 1: Train the Model

```powershell
# Train optimized model (works with 8GB RAM)
python simple_cnn.py
```

**Expected output:**
- Saved model: `modelos/simple_cnn_YYYYMMDD_HHMMSS.h5`
- Plots: `plots/simple_cnn_history_*.png`
- Expected accuracy: ~60-70% in 5 epochs
- Time: ~10-15 minutes

### Step 2: Test the Model

```powershell
# Load model and run tests
python test_model.py
```

**Test options:**
1. **Test random samples** - 10 random images
2. **Evaluate full dataset** - 10,000 complete images
3. **Test by class** - 5 examples per class (airplane, car, etc.)
4. **Prediction grid** - View of 9 predictions
5. **Interactive mode** - Test specific image

**Example output:**
```
Sample 1: True=airplane     | Predicted=airplane     | Confidence= 85.3%
Sample 2: True=cat          | Predicted=dog          | Confidence= 62.1%
Sample 3: True=ship         | Predicted=ship         | Confidence= 91.7%
...
Accuracy on 10 samples: 70.0% (7/10)
```

### Step 3: Generate Evidence

```powershell
# Create GIFs and plots
python generate_evidence.py
```

**Generated:**
- Training progress GIF
- Predictions GIF
- Updated metrics

---

## Implemented Models

### Simple CNN

```
Input (32×32×3)
    ↓
[Conv16 → BN → Pool → Dropout(0.25)]
[Conv32 → BN → Pool → Dropout(0.25)]
[Conv64 → BN → Pool → Dropout(0.25)]
    ↓
Flatten → Dense128 → Dropout(0.5) → Output(10)
```

**Characteristics:**
- **Parameters:** 156,522 (611 KB)
- **Optimized for:** Limited hardware, fast training
- **Dataset:** CIFAR-10 (32×32×3)
- **Batch Size:** 16
- **Epochs:** 5 (configurable)
- **Training time:** ~10-15 minutes on CPU

---

## Evaluated Metrics

| Metric | Description | Range | Interpretation |
|---------|-------------|-------|----------------|
| **Accuracy** | Proportion of correct predictions | [0, 1] | 1 = Perfect |
| **Precision** | TP / (TP + FP) | [0, 1] | Few false positives |
| **Recall** | TP / (TP + FN) | [0, 1] | Few false negatives |
| **F1-Score** | Harmonic mean Precision/Recall | [0, 1] | Balance |
| **AUC** | Area under ROC curve | [0, 1] | 1 = Perfect |
| **Loss** | Cross-entropy loss | [0, ∞) | 0 = Perfect |

---

## Generated Visualizations

### 1. Training History
Shows accuracy and loss curves over epochs for both training and validation sets.

![Training History](plots/simple_cnn_history_20251204_202143.png)

### 2. Prediction Samples
Grid showing model predictions on random test images with confidence scores.

![Prediction Samples](plots/random_samples_20251204_220401.png)

### 3. Training Progress GIF
Animated visualization of training metrics evolution.

![Training Progress](evidencias/gifs/01_training_progress_20251204_232926.gif)

### 4. Predictions GIF
Real-time prediction visualization on test images.

![Predictions](evidencias/gifs/02_predictions_20251204_232926.gif)

---

## Configuration

### Training Parameters

```python
# simple_cnn.py
IMAGE_SIZE = (32, 32)
BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2
```

### Callbacks

- **EarlyStopping**: patience=10
- **ReduceLROnPlateau**: factor=0.5, patience=5
- **ModelCheckpoint**: save_best_only=True

---

## Complete Documentation

### Main Documents

- **[documentacion/ESTADO_PROYECTO.md](documentacion/ESTADO_PROYECTO.md)** - READ FIRST
  - Current status: 100% complete
  - Functional components
  - Resolved issues
  - Results obtained

- **[documentacion/EVIDENCIAS.md](documentacion/EVIDENCIAS.md)**
  - Evidence plan (screenshots, GIFs)
  - Generated files
  - Regeneration instructions

- **[documentacion/ARCHITECTURE.md](documentacion/ARCHITECTURE.md)**
  - Technical system architecture
  - Component diagrams
  - Data flow

- **[documentacion/METRICAS.md](documentacion/METRICAS.md)**
  - Metrics explanation
  - Formulas and examples
  - Results interpretation

---

## Requirements Compliance

### Subsystem 5: Model Training and Comparison

| Requirement | Status | Evidence |
|-----------|--------|-----------|
| CNN from scratch (Keras/PyTorch) | Complete | `simple_cnn.py` functional |
| Metrics analysis | Implemented | Classification report, plots |
| Results presentation | Functional | Automatic graphs |
| Complete documentation | 100% | 7 technical documents |
| Commits in English | Complete | Git history |

**Overall Progress:** 100% completed

---

## Results Obtained

### CIFAR-10 Dataset - Simple CNN

**Successfully Trained Model:**
- **File:** `simple_cnn_20251204_202143.h5`
- **Size:** 611 KB
- **Architecture:** 3 convolutional blocks + 1 dense layer
- **Total Parameters:** 156,522
  - Trainable: 156,298 (610.54 KB)
  - Non-trainable: 224 (896 B)

**Training Configuration:**
- Dataset: CIFAR-10 (50,000 train / 10,000 test)
- Image size: 32×32×3
- Batch size: 16
- Epochs: 5
- Optimizer: Adam (lr=0.001)
- Hardware: CPU (Intel/AMD with AVX2, FMA)
- Time: ~10-15 minutes

**Achieved Results:**
- **Test Accuracy:** 62.79%
- **Test Loss:** 1.0686
- **ROC AUC:** 0.9365
- **Macro Precision:** 64.49%
- **Macro Recall:** 62.79%
- **Macro F1-Score:** 62.32%

**Best Classes:**
- Ship: 83.10%
- Frog: 81.70%
- Deer: 76.80%
- Truck: 73.20%

**Challenging Classes:**
- Bird: 33.00%
- Cat: 44.50%
- Dog: 46.10%

---

## Troubleshooting

### Error: Out of Memory (OOM)

```python
# Reduce batch size
BATCH_SIZE = 16  # or 8

# Use mixed precision
import tensorflow as tf
tf.keras.mixed_precision.set_global_policy('mixed_float16')
```

### Slow Training

```bash
# Verify GPU
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# Reduce epochs for testing
# Edit simple_cnn.py: EPOCHS = 3
```

---

## Deliverables

- Complete source code
- Trained models (.h5 files)
- Metrics (JSON, CSV)
- Visualizations (PNG, GIFs)
- Detailed documentation (Markdown)
- Automation scripts

---

## Contributions

This subsystem is part of the **Advanced Visual Computing Workshop** and meets all specified requirements:

- CNN training from scratch
- Comprehensive metrics
- Professional visualizations
- Complete documentation
- Commits in English

---

## License

MIT License

---

## Authors

- **Subsystem 5 Team**
- Advanced Visual Computing Workshop
- December 2025

---

## Support

For issues or questions:
1. Review documentation in `documentacion/`
2. Check training logs
3. Examine generated metrics
4. Review commented code

---

## Highlighted Features

- Modular and extensible architecture
- Clean and well-documented code
- Complete automated pipeline
- Professional visualizations
- Exhaustive and precise metrics
- Compatible with custom datasets

---

**Enjoy training and comparing Deep Learning models!**

---

*Last update: December 2025*
