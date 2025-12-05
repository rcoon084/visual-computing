#!/usr/bin/env python
"""
Test Trained Model - Subsystem 5
Load a trained model and test it with new images
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from pathlib import Path

# CIFAR-10 class names
CLASS_NAMES = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

def load_latest_model(models_dir='../../results/models'):
    """Load the most recent trained model"""
    models_path = Path(models_dir)
    
    # Find all .h5 files
    model_files = list(models_path.glob('*.h5'))
    
    if not model_files:
        raise FileNotFoundError(f"No models found in {models_dir}")
    
    # Get the most recent model
    latest_model = max(model_files, key=lambda p: p.stat().st_mtime)
    
    print(f"Loading model: {latest_model.name}")
    model = keras.models.load_model(latest_model)
    
    return model, latest_model.name

def load_test_data():
    """Load CIFAR-10 test dataset"""
    print("Loading CIFAR-10 test dataset...")
    (_, _), (x_test, y_test) = keras.datasets.cifar10.load_data()
    
    # Normalize
    x_test = x_test.astype('float32') / 255.0
    
    print(f"Test dataset: {x_test.shape}")
    print(f"Test labels: {y_test.shape}")
    
    return x_test, y_test

def predict_single_image(model, image, true_label):
    """Predict a single image and show result"""
    # Add batch dimension
    img_batch = np.expand_dims(image, axis=0)
    
    # Predict
    predictions = model.predict(img_batch, verbose=0)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]
    
    # Get true label
    true_class = true_label[0] if isinstance(true_label, (list, np.ndarray)) else true_label
    
    return predicted_class, confidence, predictions[0]

def visualize_prediction(image, true_label, predicted_class, confidence, probabilities):
    """Visualize image with prediction results"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Show image
    ax1.imshow(image)
    ax1.axis('off')
    
    true_class = true_label[0] if isinstance(true_label, (list, np.ndarray)) else true_label
    is_correct = (predicted_class == true_class)
    
    color = 'green' if is_correct else 'red'
    title = f"True: {CLASS_NAMES[true_class]}\nPredicted: {CLASS_NAMES[predicted_class]} ({confidence*100:.1f}%)"
    ax1.set_title(title, color=color, fontsize=12, fontweight='bold')
    
    # Show probability distribution
    ax2.barh(CLASS_NAMES, probabilities)
    ax2.set_xlabel('Probability')
    ax2.set_title('Class Probabilities')
    ax2.set_xlim([0, 1])
    
    # Highlight predicted class
    ax2.get_children()[predicted_class].set_color(color)
    
    plt.tight_layout()
    return fig

def test_random_samples(model, x_test, y_test, num_samples=10, save_images=True):
    """Test model on random samples"""
    print(f"\n{'='*60}")
    print(f"  Testing {num_samples} Random Samples")
    print(f"{'='*60}\n")
    
    # Select random samples
    indices = np.random.choice(len(x_test), num_samples, replace=False)
    
    correct = 0
    predictions_data = []
    
    for i, idx in enumerate(indices):
        image = x_test[idx]
        true_label = y_test[idx]
        
        predicted_class, confidence, probabilities = predict_single_image(model, image, true_label)
        
        true_class = true_label[0] if isinstance(true_label, (list, np.ndarray)) else true_label
        is_correct = (predicted_class == true_class)
        
        if is_correct:
            correct += 1
        
        predictions_data.append({
            'image': image,
            'true_label': true_label,
            'predicted_class': predicted_class,
            'confidence': confidence,
            'probabilities': probabilities,
            'is_correct': is_correct
        })
        
        status = "✓" if is_correct else "✗"
        print(f"{status} Sample {i+1}: True={CLASS_NAMES[true_class]:12s} | "
              f"Predicted={CLASS_NAMES[predicted_class]:12s} | "
              f"Confidence={confidence*100:5.1f}%")
    
    accuracy = (correct / num_samples) * 100
    print(f"\nAccuracy on {num_samples} samples: {accuracy:.1f}% ({correct}/{num_samples})")
    
    # Save visualizations
    if save_images:
        results_dir = Path('../../results/plots')
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Create grid of all samples
        rows = int(np.ceil(num_samples / 3))
        cols = min(3, num_samples)
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
        if num_samples == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        for i, pred_data in enumerate(predictions_data):
            if i < len(axes):
                axes[i].imshow(pred_data['image'])
                axes[i].axis('off')
                
                true_class = pred_data['true_label'][0] if isinstance(pred_data['true_label'], (list, np.ndarray)) else pred_data['true_label']
                color = 'green' if pred_data['is_correct'] else 'red'
                title = f"True: {CLASS_NAMES[true_class]}\nPred: {CLASS_NAMES[pred_data['predicted_class']]}\n{pred_data['confidence']*100:.1f}%"
                axes[i].set_title(title, color=color, fontsize=11, fontweight='bold')
        
        # Hide extra subplots
        for i in range(num_samples, len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = results_dir / f'random_samples_{timestamp}.png'
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\n✓ Predictions saved: {save_path}")
        plt.close(fig)
    
    return accuracy

def test_full_dataset(model, x_test, y_test):
    """Evaluate model on full test dataset"""
    print(f"\n{'='*60}")
    print(f"  Evaluating on Full Test Dataset")
    print(f"{'='*60}\n")
    
    # Convert labels to categorical if needed
    if len(y_test.shape) == 1 or y_test.shape[1] == 1:
        y_test_cat = keras.utils.to_categorical(y_test, 10)
    else:
        y_test_cat = y_test
    
    # Evaluate
    results = model.evaluate(x_test, y_test_cat, verbose=0)
    
    # Get metric names
    metric_names = model.metrics_names
    
    print("Results on 10,000 test images:")
    for name, value in zip(metric_names, results):
        if 'loss' in name.lower():
            print(f"  {name.capitalize()}: {value:.4f}")
        else:
            print(f"  {name.capitalize()}: {value*100:.2f}%")
    
    return results

def visualize_predictions_grid(model, x_test, y_test, num_samples=9):
    """Show a grid of predictions"""
    print(f"\nGenerating prediction grid...")
    
    # Select random samples
    indices = np.random.choice(len(x_test), num_samples, replace=False)
    
    # Create grid
    rows = int(np.sqrt(num_samples))
    cols = int(np.ceil(num_samples / rows))
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 15))
    axes = axes.flatten()
    
    for i, idx in enumerate(indices):
        image = x_test[idx]
        true_label = y_test[idx]
        
        predicted_class, confidence, _ = predict_single_image(model, image, true_label)
        
        true_class = true_label[0] if isinstance(true_label, (list, np.ndarray)) else true_label
        is_correct = (predicted_class == true_class)
        
        # Show image
        axes[i].imshow(image)
        axes[i].axis('off')
        
        color = 'green' if is_correct else 'red'
        title = f"True: {CLASS_NAMES[true_class]}\nPred: {CLASS_NAMES[predicted_class]}\n{confidence*100:.1f}%"
        axes[i].set_title(title, color=color, fontsize=10)
    
    plt.tight_layout()
    return fig

def test_by_class(model, x_test, y_test, samples_per_class=5, save_images=True):
    """Test model showing examples from each class"""
    print(f"\n{'='*60}")
    print(f"  Testing by Class ({samples_per_class} samples each)")
    print(f"{'='*60}\n")
    
    class_accuracy = {}
    all_predictions = []
    
    for class_idx in range(10):
        # Find samples of this class
        class_indices = np.where(y_test.flatten() == class_idx)[0]
        selected = np.random.choice(class_indices, min(samples_per_class, len(class_indices)), replace=False)
        
        correct = 0
        for idx in selected:
            image = x_test[idx]
            true_label = y_test[idx]
            
            predicted_class, confidence, probabilities = predict_single_image(model, image, true_label)
            
            if predicted_class == class_idx:
                correct += 1
            
            all_predictions.append({
                'image': image,
                'true_class': class_idx,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'is_correct': (predicted_class == class_idx)
            })
        
        accuracy = (correct / len(selected)) * 100
        class_accuracy[CLASS_NAMES[class_idx]] = accuracy
        
        print(f"{CLASS_NAMES[class_idx]:12s}: {accuracy:5.1f}% ({correct}/{len(selected)})")
    
    # Save visualization by class
    if save_images and all_predictions:
        results_dir = Path('../../results/plots')
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Create grid showing 1 example per class
        fig, axes = plt.subplots(2, 5, figsize=(20, 8))
        axes = axes.flatten()
        
        for class_idx in range(10):
            # Get first sample of this class
            class_samples = [p for p in all_predictions if p['true_class'] == class_idx]
            if class_samples:
                sample = class_samples[0]
                
                axes[class_idx].imshow(sample['image'])
                axes[class_idx].axis('off')
                
                color = 'green' if sample['is_correct'] else 'red'
                title = f"{CLASS_NAMES[class_idx]}\n→ {CLASS_NAMES[sample['predicted_class']]}\n{sample['confidence']*100:.1f}%"
                axes[class_idx].set_title(title, color=color, fontsize=12, fontweight='bold')
        
        plt.suptitle('One Example per Class', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = results_dir / f'by_class_{timestamp}.png'
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\n✓ Class examples saved: {save_path}")
        plt.close(fig)
    
    return class_accuracy

def interactive_test(model, x_test, y_test):
    """Interactive testing mode"""
    print(f"\n{'='*60}")
    print(f"  Interactive Testing Mode")
    print(f"{'='*60}\n")
    
    while True:
        try:
            choice = input("\nEnter image index (0-9999) or 'r' for random, 'q' to quit: ").strip().lower()
            
            if choice == 'q':
                print("Exiting interactive mode.")
                break
            
            if choice == 'r':
                idx = np.random.randint(0, len(x_test))
            else:
                idx = int(choice)
                if idx < 0 or idx >= len(x_test):
                    print(f"Invalid index. Please enter 0-{len(x_test)-1}")
                    continue
            
            image = x_test[idx]
            true_label = y_test[idx]
            
            predicted_class, confidence, probabilities = predict_single_image(model, image, true_label)
            
            fig = visualize_prediction(image, true_label, predicted_class, confidence, probabilities)
            plt.show()
            
        except ValueError:
            print("Invalid input. Please enter a number, 'r', or 'q'.")
        except KeyboardInterrupt:
            print("\nExiting interactive mode.")
            break

def main():
    """Main testing function"""
    print("="*60)
    print("  Model Testing - Subsystem 5")
    print("="*60)
    
    # Create results directory
    results_dir = Path('../../results/plots')
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Load model
    try:
        model, model_name = load_latest_model()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Please train a model first using: python simple_cnn.py")
        return
    
    # Show model summary
    print(f"\nModel Summary:")
    model.summary()
    
    # Load test data
    x_test, y_test = load_test_data()
    
    # Menu
    while True:
        print(f"\n{'='*60}")
        print("  Testing Options")
        print(f"{'='*60}")
        print("1. Test random samples (10 images)")
        print("2. Evaluate on full test dataset (10,000 images)")
        print("3. Test by class")
        print("4. Show prediction grid (9 images)")
        print("5. Interactive testing mode")
        print("6. Exit")
        print(f"{'='*60}")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            test_random_samples(model, x_test, y_test, num_samples=10)
        
        elif choice == '2':
            test_full_dataset(model, x_test, y_test)
        
        elif choice == '3':
            test_by_class(model, x_test, y_test, samples_per_class=5)
        
        elif choice == '4':
            fig = visualize_predictions_grid(model, x_test, y_test, num_samples=9)
            save_path = results_dir / f'predictions_grid_{model_name.replace(".h5", "")}.png'
            fig.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"\n✓ Grid saved: {save_path}")
            plt.show()
        
        elif choice == '5':
            interactive_test(model, x_test, y_test)
        
        elif choice == '6':
            print("\n✓ Testing completed!")
            break
        
        else:
            print("\n❌ Invalid option. Please select 1-6.")

if __name__ == "__main__":
    main()
