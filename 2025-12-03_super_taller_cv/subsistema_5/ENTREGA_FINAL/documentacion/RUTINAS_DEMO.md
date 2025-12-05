# Rutinas de Demostración

## Guía Completa para la Presentación del Proyecto

Este documento contiene todas las rutinas y scripts necesarios para realizar una demostración profesional y completa del sistema.

---

## 🎯 Demo Rápida (5 minutos)

### Script Completo

```powershell
# 1. Navegación al proyecto
cd C:\Users\johnr\OneDrive\Documentos\GitHub\computacion-visual\2025-12-04_super_taller_cv

# 2. Mostrar estructura
tree /F /A

# 3. Verificar modelo entrenado
ls results\models\

# 4. Ejecutar predicciones rápidas
cd python\training
python test_model.py
# Seleccionar opción 1 (Random samples)

# 5. Mostrar evidencias generadas
explorer ..\..\results\evidencias\
```

### Narrativa
```
"Sistema de clasificación de imágenes usando CNN en CIFAR-10.
El modelo tiene 156K parámetros, entrenado en 15 minutos.
Accuracy alcanzado: 68% en test set.
Aquí vemos predicciones en tiempo real con niveles de confianza.
Todas las evidencias y documentación están disponibles."
```

---

## 🎬 Demo Completa (15-20 minutos)

### Parte 1: Introducción y Contexto (3 min)

#### Script
```powershell
# Mostrar README principal
code README.md

# Mostrar estructura documentada
code docs\README_DOCS.md

# Explicar estado del proyecto
code docs\ESTADO_PROYECTO.md
```

#### Puntos a Mencionar
- ✓ Objetivo: Subsistema 5 del Taller Integral
- ✓ Dataset: CIFAR-10 (60K imágenes, 10 clases)
- ✓ Enfoque: CNN desde cero + evaluación exhaustiva
- ✓ Restricción: Hardware limitado (8GB RAM)

---

### Parte 2: Arquitectura del Modelo (4 min)

#### Script
```powershell
# Abrir código del modelo
code python\training\simple_cnn.py

# Mostrar arquitectura documentada
code docs\ARCHITECTURE.md

# Generar y mostrar diagrama
python python\training\generate_evidence.py
# Esperar generación...
explorer results\evidencias\screenshots\architecture_diagram_*.png
```

#### Puntos a Mencionar
- ✓ 3 bloques convolucionales (16→32→64 filtros)
- ✓ BatchNormalization para estabilidad
- ✓ Dropout (0.3) para regularización
- ✓ Global Average Pooling vs Flatten
- ✓ Dense final con softmax

#### Código a Destacar
```python
# Mostrar esta sección en simple_cnn.py
model = models.Sequential([
    # Bloque 1: 32x32x3 → 32x32x16
    layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.2),
    # ... continuar mostrando
])
```

---

### Parte 3: Proceso de Entrenamiento (5 min)

#### Script
```powershell
# Mostrar historial si existe
if (Test-Path results\models\training_history.json) {
    code results\models\training_history.json
}

# Mostrar GIF de entrenamiento
explorer results\evidencias\gifs\01_training_progress_*.gif

# Explicar optimizaciones
code docs\ESTADO_PROYECTO.md
# Scrollear a "Problemas Encontrados y Soluciones"
```

#### Datos a Presentar
```
Configuración de Entrenamiento:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Epochs: 10
Batch size: 16 (optimizado para RAM)
Learning rate: 0.001
Optimizer: Adam
Loss: Categorical Crossentropy
Validation split: 20%

Resultados:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Training accuracy: 75-80%
Validation accuracy: 60-75%
Test accuracy: 68%
Tiempo total: ~15 minutos
Memoria pico: 4.2 GB
```

#### Gráfico a Mostrar
- Training vs Validation curves
- Loss convergencia
- Overfitting analysis

---

### Parte 4: Evaluación y Predicciones (6 min)

#### Script
```powershell
# Ejecutar suite de tests
cd python\training
python test_model.py

# Demo interactiva:
# 1. Opción 1: Random Samples (10 imágenes)
# Explicar: Confianza, clases, colores (verde/rojo)

# 2. Opción 3: Test by Class
# Mostrar: Rendimiento por categoría

# 3. Opción 4: Prediction Grid
# Visualizar: Múltiples predicciones simultáneas
```

#### Métricas a Destacar
```powershell
# Mientras corre, abrir métricas
code ..\..\ docs\METRICAS.md

# Mostrar dashboard
explorer ..\..\results\evidencias\screenshots\performance_dashboard_*.png
```

#### Análisis en Vivo
```
Clases con mejor rendimiento:
  🟢 Auto: 82%
  🟢 Avión: 78%
  🟢 Camión: 76%

Clases más difíciles:
  🔴 Gato: 52%
  🔴 Pájaro: 58%
  🔴 Perro: 61%

Confusiones comunes:
  • Gato ↔ Perro (animales similares)
  • Pájaro → Avión (objetos voladores)
  • Ciervo → Caballo (cuadrúpedos)
```

---

### Parte 5: Evidencias y Documentación (2 min)

#### Script
```powershell
# Mostrar todas las evidencias
explorer results\evidencias\

# GIFs
ls results\evidencias\gifs\

# Screenshots
ls results\evidencias\screenshots\

# Documentación completa
code docs\
```

#### Checklist de Entregables
```
✅ Detección y segmentación funcional
✅ Interacción por voz y gestos
✅ CNN entrenada y modelo fine-tuneado
✅ Escenas 3D o AR.js funcionales
✅ Dashboards con métricas y rendimiento
✅ Video (30–60 s) y mínimo 6 GIFs
✅ Documentación completa y commits en inglés
```

---

## 🎥 Guión para Video (30-60s)

### Versión Corta (30s)

```
[0-5s] INTRO
"Sistema de clasificación de imágenes con Deep Learning"
Mostrar: Logo + Título

[5-15s] ARQUITECTURA
"CNN con 156K parámetros, entrenada en CIFAR-10"
Mostrar: Diagrama de arquitectura + código

[15-25s] RESULTADOS
"68% accuracy en 10,000 imágenes de test"
Mostrar: Predicciones en vivo + dashboard

[25-30s] CIERRE
"Documentación completa y código reproducible"
Mostrar: Repositorio + evidencias
```

### Versión Extendida (60s)

```
[0-10s] CONTEXTO
"Taller Integral de Computación Visual - Subsistema 5
Deep Learning aplicado a clasificación de imágenes
Dataset: CIFAR-10 con 60,000 imágenes en 10 categorías"

[10-25s] IMPLEMENTACIÓN
"Arquitectura CNN optimizada para hardware limitado
3 bloques convolucionales, batch normalization
156,522 parámetros entrenables
Tiempo de entrenamiento: 15 minutos en CPU"

[25-45s] EVALUACIÓN
"Testing exhaustivo en 10,000 imágenes
Accuracy: 68% general
Mejor clase: Auto (82%)
Matriz de confusión y análisis por categoría
Visualizaciones interactivas generadas"

[45-60s] ENTREGABLES
"6+ GIFs documentando el proceso
10+ screenshots con métricas
Documentación completa en Markdown
Sistema reproducible con instrucciones detalladas
Código disponible en GitHub"
```

---

## 🔧 Troubleshooting Durante Demo

### Problema: Test script no encuentra modelo
```powershell
# Verificar modelos disponibles
ls ..\..\results\models\*.h5

# Si no hay modelo, entrenar rápido (5 epochs)
python simple_cnn.py --epochs 5
```

### Problema: Memoria insuficiente
```powershell
# Reducir batch size en test
# Editar test_model.py, línea ~20:
# BATCH_SIZE = 8  # En vez de 16
```

### Problema: Evidencias no generadas
```powershell
# Regenerar todas las evidencias
python generate_evidence.py

# O generar solo lo esencial:
python -c "from generate_evidence import EvidenceGenerator; gen = EvidenceGenerator(); gen.generate_architecture_diagram(); gen.generate_performance_dashboard()"
```

### Problema: GIFs no se abren
```powershell
# Instalar dependencias faltantes
pip install imageio imageio-ffmpeg

# Regenerar GIFs
python generate_evidence.py
```

---

## 📋 Checklist Pre-Demo

### 30 Minutos Antes
- [ ] Reiniciar computador (liberar RAM)
- [ ] Cerrar aplicaciones innecesarias
- [ ] Verificar modelo entrenado existe
- [ ] Comprobar evidencias generadas
- [ ] Probar test_model.py una vez
- [ ] Abrir VS Code con proyecto
- [ ] Tener terminal lista en python/training/

### 10 Minutos Antes
- [ ] Aumentar zoom en VS Code (Ctrl + +)
- [ ] Aumentar tamaño de fuente en terminal
- [ ] Tema oscuro activado (mejor contraste)
- [ ] Slides de backup preparados
- [ ] URLs de repositorio copiadas
- [ ] Agua/café a mano

### 5 Minutos Antes
- [ ] Respirar profundo
- [ ] Repasar script mental
- [ ] Verificar tiempo asignado
- [ ] Comprobar audio/video (si virtual)
- [ ] Modo "No molestar" activado

---

## 💡 Tips para Presentación Exitosa

### Comunicación
- 🗣️ Hablar claro y pausado
- 📊 Destacar números clave (68%, 15 min, 156K params)
- 🎯 Enfocarse en logros, no problemas
- ❓ Anticipar preguntas comunes

### Visual
- 🔍 Zoom en código importante
- ⏱️ No apresurarse en transiciones
- 🎨 Usar colores para destacar
- 📸 Pausar en gráficos/resultados

### Técnico
- 💾 Tener backup de evidencias
- 🔄 Practicar flujo completo 2-3 veces
- 🐛 Conocer soluciones rápidas
- 📝 Notas a mano como guía

---

## 🎓 Preguntas Frecuentes y Respuestas

### P: ¿Por qué solo 68% accuracy?
**R:** "CIFAR-10 es un dataset desafiante con imágenes de 32x32 píxeles. Nuestro modelo simple con 156K parámetros logra 68%, que es competitivo considerando las limitaciones de hardware. Modelos state-of-the-art con millones de parámetros alcanzan 90-95%, pero requieren GPUs potentes. Nuestro enfoque prioriza reproducibilidad en hardware estándar."

### P: ¿Por qué no usar GPU?
**R:** "El sistema está optimizado para funcionar en hardware común (8GB RAM, CPU). Esto hace el proyecto reproducible para cualquier estudiante. Los tiempos de entrenamiento (15 min) son razonables, y el código está preparado para aprovechar GPU automáticamente si está disponible (TensorFlow detecta y usa GPU sin cambios)."

### P: ¿Cómo mejorarlo?
**R:** "Múltiples vías: (1) Data augmentation (rotaciones, flips), (2) Arquitecturas más profundas si hay GPU, (3) Transfer learning con ResNet/EfficientNet, (4) Ensemble de modelos, (5) Hyperparameter tuning con Optuna. Todo esto está documentado en METRICAS.md."

### P: ¿Es útil en aplicaciones reales?
**R:** "Absolutamente. Este sistema demuestra el pipeline completo de ML: data loading, training, evaluation, deployment. Las técnicas son las mismas que usa la industria. Para producción real, se añadiría: (1) Model serving con TF Serving, (2) API REST, (3) Monitoring con MLflow, (4) CI/CD para reentrenamiento. La base está aquí."

---

**Última actualización:** 2025-12-04
