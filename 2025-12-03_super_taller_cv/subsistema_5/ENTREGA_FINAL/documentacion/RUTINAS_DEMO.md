# Demonstration Routines

## Complete Guide for Project Presentation

This document contains all necessary routines and scripts to perform a professional and complete system demonstration.

---

## Quick Demo (5 minutes)

### Complete Script

```powershell
# 1. Navigate to project
cd C:\Users\johnr\OneDrive\Documentos\GitHub\grupo\visual-computing\2025-12-03_super_taller_cv\subsistema_5\ENTREGA_FINAL

# 2. Show structure
tree /F /A

# 3. Verify trained model
ls modelos\

# 4. Execute quick predictions
cd codigo
python test_model.py
# Select option 1 (Random samples)

# 5. Show generated evidence
explorer ..\evidencias\
```

### Narrative
```
"Image classification system using CNN on CIFAR-10.
The model has 156K parameters, trained in 15 minutes.
Achieved accuracy: 62.79% on test set.
Here we see real-time predictions with confidence levels.
All evidence and documentation are available."
```

---

## Complete Demo (15-20 minutes)

### Part 1: Introduction and Context (3 min)

#### Script
```powershell
# Show main README
code README_PRINCIPAL.md

# Show documented structure
code documentacion\README_DOCS.md

# Explain project status
code documentacion\ESTADO_PROYECTO.md
```

#### Points to Mention
- Objective: Subsystem 5 of the Integrated Workshop
- Dataset: CIFAR-10 (60K images, 10 classes)
- Approach: CNN from scratch + exhaustive evaluation
- Restriction: Limited hardware (8GB RAM)

---

### Part 2: Model Architecture (4 min)

#### Script
```powershell
# Open model code
code codigo\simple_cnn.py

# Show documented architecture
code documentacion\ARCHITECTURE.md
```

#### Points to Mention
- 3 convolutional blocks (16→32→64 filters)
- BatchNormalization for stability
- Dropout (0.25-0.5) for regularization
- Dense final with softmax

#### Code to Highlight
```python
# Show this section in simple_cnn.py
model = models.Sequential([
    # Block 1: 32x32x3 → 16x16x16
    layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    # ... continue showing
])
```

---

### Part 3: Training Process (5 min)

#### Script
```powershell
# Show training GIF
explorer evidencias\gifs\01_training_progress_20251204_232926.gif

# Show training history plot
explorer plots\simple_cnn_history_20251204_202143.png
```

#### Data to Present
```
Training Configuration:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Epochs: 5
Batch size: 16 (optimized for RAM)
Learning rate: 0.001
Optimizer: Adam
Loss: Categorical Crossentropy
Validation split: 20%

Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test accuracy: 62.79%
Test loss: 1.0686
ROC AUC: 0.9365
Total time: ~15 minutes
Peak memory: 4.2 GB
```

---

### Part 4: Evaluation and Predictions (6 min)

#### Script
```powershell
# Execute test suite
cd codigo
python test_model.py

# Interactive demo:
# 1. Option 1: Random Samples (10 images)
# Explain: Confidence, classes, colors (green/red)

# 2. Option 3: Test by Class
# Show: Performance by category

# 3. Option 4: Prediction Grid
# Visualize: Multiple simultaneous predictions
```

#### Metrics to Highlight
```powershell
# While running, open metrics
code documentacion\METRICAS.md
```

#### Live Analysis
```
Best performing classes:
  Ship: 83.10%
  Frog: 81.70%
  Deer: 76.80%
  Truck: 73.20%

Most difficult classes:
  Bird: 33.00%
  Cat: 44.50%
  Dog: 46.10%

Common confusions:
  • Cat ↔ Dog (similar animals)
  • Bird → Airplane (flying objects)
  • Deer → Horse (quadrupeds)
```

---

### Part 5: Evidence and Documentation (2 min)

#### Script
```powershell
# Show all evidence
explorer evidencias\

# GIFs
ls evidencias\gifs\

# Documentation
code documentacion\
```

#### Deliverables Checklist
```
- Functional detection and segmentation
- Voice and gesture interaction
- Trained CNN and fine-tuned model
- 3D scenes or functional AR.js
- Dashboards with metrics and performance
- 2+ GIFs
- Complete documentation and commits in English
```

---

## Video Script (30-60s)

### Short Version (30s)

```
[0-5s] INTRO
"Image classification system with Deep Learning"
Show: Logo + Title

[5-15s] ARCHITECTURE
"CNN with 156K parameters, trained on CIFAR-10"
Show: Architecture diagram + code

[15-25s] RESULTS
"62.79% accuracy on 10,000 test images"
Show: Live predictions + dashboard

[25-30s] CLOSING
"Complete documentation and reproducible code"
Show: Repository + evidence
```

### Extended Version (60s)

```
[0-10s] CONTEXT
"Visual Computing Workshop - Subsystem 5
Deep Learning applied to image classification
Dataset: CIFAR-10 with 60,000 images in 10 categories"

[10-25s] IMPLEMENTATION
"CNN architecture optimized for limited hardware
3 convolutional blocks, batch normalization
156,522 trainable parameters
Training time: 15 minutes on CPU"

[25-45s] EVALUATION
"Exhaustive testing on 10,000 images
Accuracy: 62.79% overall
Best class: Ship (83.10%)
Confusion matrix and category-wise analysis
Interactive visualizations generated"

[45-60s] DELIVERABLES
"2+ GIFs documenting the process
Training plots and metrics
Complete Markdown documentation
Reproducible system with detailed instructions
Code available on GitHub"
```

---

## Troubleshooting During Demo

### Problem: Test script doesn't find model
```powershell
# Verify available models
ls ..\modelos\*.h5

# If no model, train quickly (5 epochs)
python simple_cnn.py
```

### Problem: Insufficient memory
```powershell
# Reduce batch size in test
# Edit test_model.py, line ~20:
# BATCH_SIZE = 8  # Instead of 16
```

### Problem: Evidence not generated
```powershell
# Regenerate all evidence
python generate_evidence.py
```

---

## Pre-Demo Checklist

### 30 Minutes Before
- [ ] Restart computer (free RAM)
- [ ] Close unnecessary applications
- [ ] Verify trained model exists
- [ ] Check generated evidence
- [ ] Test test_model.py once
- [ ] Open VS Code with project
- [ ] Have terminal ready in codigo/

### 10 Minutes Before
- [ ] Increase zoom in VS Code (Ctrl + +)
- [ ] Increase font size in terminal
- [ ] Dark theme activated (better contrast)
- [ ] Backup slides prepared
- [ ] Repository URLs copied
- [ ] Water/coffee at hand

### 5 Minutes Before
- [ ] Deep breath
- [ ] Review mental script
- [ ] Verify assigned time
- [ ] Check audio/video (if virtual)
- [ ] "Do not disturb" mode activated

---

## Tips for Successful Presentation

### Communication
- Speak clearly and slowly
- Highlight key numbers (62.79%, 15 min, 156K params)
- Focus on achievements, not problems
- Anticipate common questions

### Visual
- Zoom on important code
- Don't rush transitions
- Use colors to highlight
- Pause on graphs/results

### Technical
- Have backup evidence
- Practice complete flow 2-3 times
- Know quick solutions
- Hand notes as guide

---

## Frequent Questions and Answers

### Q: Why only 62.79% accuracy?
**A:** "CIFAR-10 is a challenging dataset with 32x32 pixel images. Our simple model with 156K parameters achieves 62.79%, which is competitive considering hardware limitations. State-of-the-art models with millions of parameters reach 90-95%, but require powerful GPUs. Our approach prioritizes reproducibility on standard hardware."

### Q: Why not use GPU?
**A:** "The system is optimized to work on common hardware (8GB RAM, CPU). This makes the project reproducible for any student. Training times (15 min) are reasonable, and the code is prepared to take advantage of GPU automatically if available (TensorFlow detects and uses GPU without changes)."

### Q: How to improve it?
**A:** "Multiple ways: (1) Data augmentation (rotations, flips), (2) Deeper architectures if GPU available, (3) Transfer learning with ResNet/EfficientNet, (4) Model ensemble, (5) Hyperparameter tuning with Optuna. All this is documented in METRICAS.md."

### Q: Is it useful in real applications?
**A:** "Absolutely. This system demonstrates the complete ML pipeline: data loading, training, evaluation, deployment. The techniques are the same as used in industry. For real production, we would add: (1) Model serving with TF Serving, (2) REST API, (3) Monitoring with MLflow, (4) CI/CD for retraining. The foundation is here."

---

**Last update:** December 4, 2025
