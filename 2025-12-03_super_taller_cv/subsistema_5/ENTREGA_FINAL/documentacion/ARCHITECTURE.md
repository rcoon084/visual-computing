# Architecture Documentation - Subsystem 5

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Subsystem 5 Architecture                  │
│                                                              │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐│
│  │  Data Layer │───▶│ Training     │───▶│  Evaluation    ││
│  │             │    │ Layer        │    │  Layer         ││
│  │ - CIFAR-10  │    │              │    │                ││
│  │ - Augment   │    │ - CNN        │    │ - Metrics      ││
│  │             │    │              │    │ - Confusion    ││
│  │             │    │              │    │ - ROC Curves   ││
│  └─────────────┘    └──────────────┘    └────────────────┘│
│                            │                   │           │
│                            ▼                   ▼           │
│                     ┌──────────────┐    ┌────────────────┐│
│                     │  Model       │    │  Visualization ││
│                     │  Storage     │    │  Layer         ││
│                     │              │    │                ││
│                     │ - .h5 files  │    │ - Plots        ││
│                     │              │    │ - GIFs         ││
│                     └──────────────┘    │ - Metrics      ││
│                                         └────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Architecture

### Training Pipeline

```
┌────────────┐
│  Raw Data  │
│  (CIFAR10) │
└─────┬──────┘
      │
      ▼
┌────────────────────┐
│  Preprocessing     │
│  - Resize          │
│  - Normalize       │
│  - Augmentation    │
└─────┬──────────────┘
      │
      ▼
┌───────────────────┐
│ CNN Training      │
│                   │
│  - Build Model    │
│  - Train          │
│  - Validate       │
└─────┬─────────────┘
      │
      ▼
┌────────────────────────────┐
│  Model Evaluation          │
│  - Accuracy, Precision     │
│  - Recall, AUC, Loss       │
│  - Confusion Matrix        │
│  - Classification Report   │
└─────┬──────────────────────┘
      │
      ▼
┌────────────────────────────┐
│  Results Storage           │
│  - Models (*.h5)           │
│  - Metrics (*.json)        │
│  - Plots (*.png)           │
└─────┬──────────────────────┘
      │
      ▼
┌────────────────────────────┐
│  Visualization             │
│  - GIFs                    │
│  - Training Plots          │
└────────────────────────────┘
```

---

## Component Architecture

### CNN Module

```python
CNNTrainer
    │
    ├── CNNArchitecture
    │   └── build_model()
    │       ├── Conv Blocks (3x)
    │       ├── BatchNorm Layers
    │       ├── Dropout Layers
    │       └── Dense Layers
    │
    ├── DataLoader
    │   ├── load_cifar10_data()
    │   └── create_data_generators()
    │
    ├── MetricsVisualizer
    │   ├── plot_training_history()
    │   ├── plot_confusion_matrix()
    │   └── plot_roc_curves()
    │
    └── Training Methods
        ├── train_model()
        └── evaluate_model()
```

---

## Data Architecture

### Input Data Structure

```
data/
├── raw/
│   └── cifar-10-batches-py/
│       ├── data_batch_1
│       ├── data_batch_2
│       ├── data_batch_3
│       ├── data_batch_4
│       ├── data_batch_5
│       └── test_batch
│
└── processed/
    ├── train/
    └── test/
```

### Output Data Structure

```
ENTREGA_FINAL/
├── modelos/
│   └── simple_cnn_20251204_202143.h5
│
├── plots/
│   ├── simple_cnn_history_20251204_202143.png
│   └── random_samples_20251204_220401.png
│
├── evidencias/
│   └── gifs/
│       ├── 01_training_progress_20251204_232926.gif
│       └── 02_predictions_20251204_232926.gif
│
└── metrics/
    ├── latest_metrics.json
    └── latest_evidence_manifest.json
```


---

## Design Patterns

### Configuration Management

```python
class Config:
    """Single configuration instance"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Model Creation

```python
class ModelFactory:
    """Create different model types"""

    @staticmethod
    def create_model(model_type, **kwargs):
        if model_type == 'cnn':
            return CNNArchitecture.build_model(**kwargs)
        # Additional models can be added here
```

---

## Performance Optimization

### Data Pipeline Optimization

```python
dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
dataset = dataset.cache()
dataset = dataset.shuffle(buffer_size=10000)
dataset = dataset.batch(BATCH_SIZE)
dataset = dataset.prefetch(tf.data.AUTOTUNE)
```

### Memory Management

```python
# Reduce batch size for limited RAM
BATCH_SIZE = 16  # Instead of 32 or 64

# Use mixed precision if needed
import tensorflow as tf
tf.keras.mixed_precision.set_global_policy('mixed_float16')
```

---

## Logging Architecture

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Training started...")
```

---

**Version:** 1.0
**Last Updated:** December 2025
**Maintainer:** Subsystem 5 Team