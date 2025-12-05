# Documentation - Subsystem 5

**Project:** Advanced Visual Computing Workshop
**Subsystem:** 5 - CNN Model Training and Comparison
**Date:** December 2025

---

## Documentation Index

### Available Documents

1. **[README.md](README.md)** - READ FIRST
   - System overview
   - Quick start guide
   - Features and results

2. **[ESTADO_PROYECTO.md](ESTADO_PROYECTO.md)**
   - Current project status (100% completed)
   - Implemented components
   - Obtained results

3. **[EVIDENCIAS.md](EVIDENCIAS.md)**
   - Generated visual evidence
   - GIFs and plots
   - Metrics files

4. **[ARCHITECTURE.md](ARCHITECTURE.md)**
   - Detailed technical architecture
   - Data flow diagrams
   - Components and modules
   - Applied design patterns

5. **[METRICAS.md](METRICAS.md)**
   - Metrics explanation
   - Accuracy, Precision, Recall, F1-Score, AUC
   - Formulas and examples
   - Results interpretation

6. **[QUICK_DEMO.md](QUICK_DEMO.md)**
   - Quick setup guide
   - Execution commands
   - Results visualization

7. **[RUTINAS_DEMO.md](RUTINAS_DEMO.md)**
   - Complete presentation guide
   - Demo scripts
   - Video guide
   - Troubleshooting

---

## Quick Reading Guide

### If you are new to the project:
```
1. Read README.md (10 min)
   → Understand what the system does

2. Review ESTADO_PROYECTO.md (5 min)
   → See what's done and what's achieved

3. Consult EVIDENCIAS.md (5 min)
   → See generated evidence
```

### If you need to understand the architecture:
```
1. ARCHITECTURE.md (15 min)
   → Complete technical design

2. METRICAS.md (10 min)
   → How models are evaluated
```

### If you will present the project:
```
1. ESTADO_PROYECTO.md - Obtained results
2. RUTINAS_DEMO.md - Presentation guide
3. README.md - How to execute
```---

## 📊 Resumen Ejecutivo

### ¿Qué es el Subsistema 5?

Módulo especializado en **Deep Learning** que implementa:
- Entrenamiento de CNN desde cero
- Transfer learning con modelos preentrenados
- Comparación de arquitecturas
- Visualización de resultados

### Estado Actual (Diciembre 4, 2025)

| Componente | Estado | Completado |
|------------|--------|------------|
| Simple CNN | ✅ Funcional | 100% |
| CNN Scratch | 🔧 Optimización | 77% |
| Fine-Tuning | 📋 Preparado | 60% |
| Comparación | 📋 Preparado | 60% |
| Dashboard | 📋 Preparado | 60% |
| **TOTAL** | | **73%** |

### Resultado Principal

✅ **Modelo Simple CNN entrenado exitosamente**
- Archivo: `results/models/simple_cnn_20251204_202143.h5`
- Parámetros: 156,522 (611 KB)
- Dataset: CIFAR-10
- Accuracy esperada: 60-70%

---

## 🗂️ Estructura de Carpetas

```
docs/
├── README.md                 # Este archivo (índice)
├── ESTADO_PROYECTO.md        # ⭐ Estado actual detallado
├── EVIDENCIAS.md             # Plan de screenshots/GIFs/video
├── ARCHITECTURE.md           # Arquitectura técnica
└── METRICAS.md               # Métricas y evaluación

../python/training/           # Código fuente
├── simple_cnn.py            # ✅ CNN optimizada (funcional)
├── cnn_from_scratch.py      # 🔧 CNN completa (optimización)
├── fine_tuning.py           # 📋 Transfer learning
├── compare_models.py        # 📋 Comparación
├── dashboard.py             # 📋 Streamlit dashboard
├── run_all.py               # 🚀 Pipeline automatizado
└── requirements.txt         # Dependencias

../results/                   # Resultados generados
├── models/                  # Modelos entrenados (.h5)
├── plots/                   # Gráficas y visualizaciones
└── evidencias/              # Screenshots, GIFs, videos
    ├── screenshots/
    ├── gifs/
    └── video/

../data/                      # Datasets
├── raw/                     # CIFAR-10 original
└── processed/               # Datos preprocesados
```

---

## 🚀 Inicio Rápido

### 1. Instalación

```powershell
# Navegar al directorio
cd 2025-12-04_super_taller_cv\python\training

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar Entrenamiento

```powershell
# Opción recomendada: CNN Simple (funciona con 8GB RAM)
python simple_cnn.py

# Opción avanzada: Pipeline completo (requiere >16GB RAM)
python run_all.py --all
```

### 3. Ver Resultados

```powershell
# Modelos guardados
ls ..\..\results\models\

# Gráficas generadas
ls ..\..\results\plots\
```

---

## 📖 Información por Documento

### ESTADO_PROYECTO.md

**Contenido:**
- Resumen ejecutivo del progreso
- Estado de cada componente (código, pruebas, docs)
- Problemas encontrados y cómo se resolvieron
- Resultados técnicos obtenidos
- Roadmap de próximos pasos

**Cuándo leer:**
- Antes de empezar a trabajar
- Para reportar progreso
- Para entender qué falta por hacer

**Longitud:** ~15 minutos de lectura

---

### EVIDENCIAS.md

**Contenido:**
- Lista de screenshots requeridos (mínimo 10)
- Plan de GIFs (mínimo 6)
- Guion de video demo (30-60 segundos)
- Herramientas recomendadas (ScreenToGif, OBS)
- Checklist de capturas

**Cuándo leer:**
- Cuando necesites generar evidencias
- Antes de hacer la presentación
- Para organizar capturas

**Longitud:** ~10 minutos de lectura

---

### ARCHITECTURE.md

**Contenido:**
- Diseño del sistema completo
- Diagramas de componentes
- Flujo de datos
- Patrones de diseño
- Decisiones técnicas

**Cuándo leer:**
- Para entender la arquitectura
- Antes de modificar código
- Para documentación técnica

**Longitud:** ~20 minutos de lectura

---

### METRICAS.md

**Contenido:**
- Accuracy: (TP+TN)/(TP+TN+FP+FN)
- Precision: TP/(TP+FP)
- Recall: TP/(TP+FN)
- F1-Score: 2 × (Precision × Recall)/(Precision + Recall)
- AUC: Área bajo curva ROC
- Ejemplos con CIFAR-10

**Cuándo leer:**
- Para entender métricas del modelo
- Al analizar resultados
- Para reportes técnicos

**Longitud:** ~15 minutos de lectura

---

## 🔗 Enlaces Útiles

### Documentación Externa

- **TensorFlow:** https://www.tensorflow.org/api_docs
- **Keras:** https://keras.io/api/
- **CIFAR-10:** https://www.cs.toronto.edu/~kriz/cifar.html
- **Scikit-learn Metrics:** https://scikit-learn.org/stable/modules/model_evaluation.html

### Repositorios Relacionados

- **Proyecto Principal:** [computacion-visual](https://github.com/johnrua17/computacion-visual)
- **Taller 4:** Ver `taller_4.md` para requisitos completos

---

## 📝 Convenciones de Documentación

### Símbolos Utilizados

- ✅ **Completado** - Funcional y probado
- 🔧 **En progreso** - Implementado, requiere ajustes
- 📋 **Preparado** - Código listo, pendiente pruebas
- ⏳ **Pendiente** - Por implementar
- ⭐ **Importante** - Leer primero
- 🚀 **Acción** - Comando ejecutable
- 💡 **Tip** - Sugerencia útil
- ⚠️ **Advertencia** - Precaución necesaria

### Estados de Componentes

| Símbolo | Código | Pruebas | Docs | Significado |
|---------|--------|---------|------|-------------|
| ✅ | 100% | 100% | 100% | Completamente listo |
| 🔧 | 100% | 50% | 80% | Funcional, requiere ajustes |
| 📋 | 100% | 0% | 80% | Listo para probar |
| ⏳ | 0% | 0% | 0% | Por hacer |

---

## 🎓 Para Estudiantes

### Aprendizajes Clave del Subsistema 5

1. **Deep Learning Básico**
   - Construcción de CNN desde cero
   - Capas: Conv2D, BatchNormalization, Dropout
   - Optimizadores: Adam, SGD
   - Funciones de pérdida: categorical_crossentropy

2. **Transfer Learning**
   - Uso de modelos preentrenados
   - Feature extraction vs Fine-tuning
   - Congelamiento de capas

3. **Optimización de Recursos**
   - Gestión de memoria RAM
   - Batch size vs Accuracy trade-off
   - Procesamiento por lotes

4. **Evaluación de Modelos**
   - Métricas: Accuracy, Precision, Recall, F1
   - Matrices de confusión
   - Curvas ROC y AUC

5. **Ingeniería de Software**
   - Modularización de código
   - Gestión de dependencias
   - Documentación técnica
   - Control de versiones (Git)

---

## ❓ Preguntas Frecuentes

### ¿Por qué hay dos versiones de CNN?

**Simple CNN** es optimizada para hardware limitado (8GB RAM), mientras que **CNN Scratch** es más compleja pero requiere más recursos (>16GB RAM).

### ¿Cuál ejecutar primero?

Siempre `simple_cnn.py` para verificar que todo funciona. Es rápida (~15 min) y funcional.

### ¿El entrenamiento es muy lento?

En CPU es normal que tarde 10-20 minutos. Con GPU (NVIDIA) sería 5-10x más rápido.

### ¿Dónde están los resultados?

En `results/models/` están los modelos .h5 y en `results/plots/` las gráficas generadas.

### ¿Cómo sé si funcionó bien?

Si el archivo .h5 se creó y el accuracy es >50%, funcionó. Para CIFAR-10, 60-70% es bueno para un modelo simple.

---

## 📞 Soporte

### Problemas Comunes

1. **Error de memoria (OOM)**
   - Solución: Usar `simple_cnn.py`
   - Ver ESTADO_PROYECTO.md sección "Problemas Encontrados"

2. **Dependencias faltantes**
   - Solución: `pip install -r requirements.txt`

3. **Rutas incorrectas**
   - Solución: Ejecutar desde `python/training/`

4. **Entrenamiento muy lento**
   - Normal en CPU. Reducir epochs o usar GPU.

### Contacto

- **Repositorio:** [github.com/johnrua17/computacion-visual](https://github.com/johnrua17/computacion-visual)
- **Issues:** Usar GitHub Issues para reportar problemas
- **Documentación:** Esta carpeta `docs/`

---

## 📅 Historial de Actualizaciones

| Fecha | Versión | Cambios |
|-------|---------|---------|
| 2025-12-04 | 1.0 | Documentación inicial completa |
| 2025-12-04 | 1.1 | Agregado ESTADO_PROYECTO.md |
| 2025-12-04 | 1.2 | Agregado EVIDENCIAS.md |
| 2025-12-04 | 1.3 | Este README.md de índice |

---

## ✅ Checklist para Lectores

### Antes de Empezar
- [ ] Leí ESTADO_PROYECTO.md
- [ ] Revisé requisitos en requirements.txt
- [ ] Entiendo que Simple CNN es la opción recomendada
- [ ] Tengo al menos 8GB RAM disponibles

### Durante Desarrollo
- [ ] Ejecuté simple_cnn.py exitosamente
- [ ] Generé modelo .h5
- [ ] Tengo gráficas de accuracy/loss
- [ ] Capturé evidencias (screenshots/GIFs)

### Para Entrega
- [ ] Código documentado con comentarios
- [ ] Commits en inglés con mensajes claros
- [ ] Video demo de 30-60 segundos
- [ ] Mínimo 6 GIFs generados
- [ ] README.md actualizado con resultados
- [ ] Todos los documentos revisados

---

**Última actualización:** Diciembre 4, 2025  
**Versión:** 1.3  
**Mantenedor:** Equipo Subsistema 5
