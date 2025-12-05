# Métricas del Modelo - Subsistema 5

**Última actualización:** 2025-12-04 23:29:58
**Muestras evaluadas:** 10000

---

## Resumen ejecutivo

- Accuracy (evaluación): 62.79%
- Loss (evaluación): 1.0686
- Macro Precision: 64.49%
- Macro Recall: 62.79%
- Macro F1-Score: 62.32%
- ROC AUC (OvR): 0.9365
- Errores totales detectados: 3721

---

## Precisión por clase

| Clase | Accuracy | Soporte |
| --- | --- | --- |
| Avión | 64.60% | 1000.0 |
| Auto | 61.50% | 1000.0 |
| Pájaro | 33.00% | 1000.0 |
| Gato | 44.50% | 1000.0 |
| Ciervo | 76.80% | 1000.0 |
| Perro | 46.10% | 1000.0 |
| Rana | 81.70% | 1000.0 |
| Caballo | 63.40% | 1000.0 |
| Barco | 83.10% | 1000.0 |
| Camión | 73.20% | 1000.0 |

---

## Confusiones principales

- Avión → Barco (143 casos)
- Auto → Camión (188 casos)
- Pájaro → Ciervo (281 casos)
- Gato → Ciervo (153 casos)
- Ciervo → Rana (71 casos)
- Perro → Gato (226 casos)
- Rana → Ciervo (77 casos)
- Caballo → Ciervo (171 casos)
- Barco → Avión (62 casos)
- Camión → Barco (85 casos)

---

## Referencia de métricas

- **Accuracy:** Porcentaje de predicciones correctas sobre el total.
- **Precision:** Proporción de verdaderos positivos sobre todas las predicciones positivas.
- **Recall:** Proporción de verdaderos positivos sobre todas las muestras positivas reales.
- **F1-Score:** Media armónica entre precision y recall.
- **ROC AUC:** Área bajo la curva ROC para clasificación multiclase (One-vs-Rest).
