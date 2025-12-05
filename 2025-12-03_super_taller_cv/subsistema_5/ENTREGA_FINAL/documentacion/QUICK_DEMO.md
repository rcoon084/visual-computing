# Quick Demo Script - Subsistema 5

## 1. Configuración rápida

```powershell
cd python/training
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Ejecución completa (recomendado)

```powershell
python run_complete_automation.py
```

El script ejecuta automáticamente:
1. Verificación del entorno y del modelo.
2. Generación de evidencias (GIFs + capturas + métricas).
3. Actualización de documentación.
4. Ejecución de pruebas rápidas.
5. Empaquetado en `ENTREGA_FINAL/`.

## 3. Ejecución manual por etapas (avanzado)

```powershell
# Entrenar modelo rápido
python simple_cnn.py

# Probar modelo
python test_model.py

# Generar evidencias visuales
python generate_evidence.py

# Actualizar documentación
python update_documentation.py
```

## 4. Visualización de resultados

- Evidencias: `results/evidencias/`
- Modelos: `results/models/`
- Dashboard (opcional): `streamlit run dashboard.py`
- Entrega final consolidada: `ENTREGA_FINAL/`
