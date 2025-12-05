#!/usr/bin/env python
"""Automatic documentation generator for Subsystem 5."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path


class DocumentationUpdater:
    """Regenerates Markdown documentation based on latest metrics and evidences."""

    def __init__(self) -> None:
        self.training_path = Path(__file__).parent
        self.base_path = self.training_path.parent.parent
        self.docs_path = self.base_path / "docs"
        self.results_path = self.base_path / "results"
        self.metrics_path = self.results_path / "metrics"
        self.evidence_path = self.results_path / "evidencias"
        self.timestamp = datetime.now()

        self.metrics = self._load_json(self.metrics_path / "latest_metrics.json")
        self.manifest = self._load_json(self.metrics_path / "latest_evidence_manifest.json")

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def _load_json(self, path: Path) -> dict:
        if path.exists():
            with open(path, "r", encoding="utf-8") as descriptor:
                try:
                    return json.load(descriptor)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _write_file(self, relative_path: str, content: str) -> None:
        output_path = self.docs_path / relative_path
        output_path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"✓ Documentación actualizada: {output_path.relative_to(self.base_path)}")

    @staticmethod
    def _format_percent(value: float | None) -> str:
        if value is None:
            return "N/A"
        return f"{value * 100:.2f}%"

    # ------------------------------------------------------------------
    # Document builders
    # ------------------------------------------------------------------
    def build_evidencias(self) -> None:
        items = self.manifest.get("items", [])
        counts = Counter(item.get("kind", "otros") for item in items)

        gifs = [item for item in items if item.get("kind") == "gif"]
        screenshots = [item for item in items if item.get("kind") == "screenshot"]
        videos = [item for item in items if item.get("kind") == "video"]

        resumen_table = "\n".join([
            "| Tipo | Cantidad | Carpeta |",
            "| --- | --- | --- |",
            f"| GIFs | {counts.get('gif', 0)} | results/evidencias/gifs |",
            f"| Screenshots | {counts.get('screenshot', 0)} | results/evidencias/screenshots |",
            f"| Videos | {counts.get('video', 0)} | results/evidencias/videos |",
        ])

        gifs_section = "\n".join(
            f"{idx}. {item.get('description')} (`{item.get('path')}`)"
            for idx, item in enumerate(sorted(gifs, key=lambda entry: entry.get("path", "")), start=1)
        ) or "- (Sin GIFs registrados)"

        screenshots_section = "\n".join(
            f"{idx}. {item.get('description')} (`{item.get('path')}`)"
            for idx, item in enumerate(sorted(screenshots, key=lambda entry: entry.get("path", "")), start=1)
        ) or "- (Sin capturas registradas)"

        videos_section = "\n".join(
            f"{idx}. {item.get('description')} (`{item.get('path')}`)"
            for idx, item in enumerate(sorted(videos, key=lambda entry: entry.get("path", "")), start=1)
        ) if videos else "- (Pendiente). Generar con `python record_demo_video.py`."

        lines = [
            "# Evidencias Visuales - Subsistema 5",
            "",
            f"**Fecha de actualización:** {self.timestamp:%Y-%m-%d %H:%M:%S}",
            "**Subsistema:** 5 - Entrenamiento y Comparación de Modelos CNN",
            "",
            "---",
            "",
            "## Resumen rápido",
            "",
            resumen_table,
            "",
            "---",
            "",
            "## GIFs generados",
            "",
            gifs_section,
            "",
            "## Capturas de pantalla",
            "",
            screenshots_section,
            "",
            "## Videos",
            "",
            videos_section,
            "",
            "---",
            "",
            "## Cómo regenerar automáticamente",
            "",
            "```powershell",
            "cd python/training",
            "python run_complete_automation.py",
            "```",
            "",
            "El script anterior entrena (si es necesario), ejecuta pruebas, genera evidencias visuales,",
            "actualiza la documentación y empaqueta la entrega final en `ENTREGA_FINAL/`.",
        ]

        self._write_file("EVIDENCIAS.md", "\n".join(lines))

    def build_metricas(self) -> None:
        if not self.metrics:
            lines = [
                "# Métricas del Modelo - Subsistema 5",
                "",
                "No se encontraron métricas guardadas. Ejecuta `python run_complete_automation.py`",
                "para generar el modelo, las métricas y la documentación actualizada.",
            ]
            self._write_file("METRICAS.md", "\n".join(lines))
            return

        per_class_accuracy = self.metrics.get("per_class_accuracy", {})
        report = self.metrics.get("report", {})
        support = {label: data.get("support", 0) for label, data in report.items() if isinstance(data, dict)}

        per_class_rows = "\n".join(
            f"| {label} | {accuracy * 100:.2f}% | {support.get(label, 0)} |"
            for label, accuracy in per_class_accuracy.items()
        ) if per_class_accuracy else "| - | - | - |"

        top_confusions = self.metrics.get("top_confusions", [])
        confusions_section = "\n".join(
            f"- {item['actual']} → {item['predicted']} ({item['count']} casos)"
            for item in top_confusions
        ) if top_confusions else "- Sin confusiones destacadas"

        lines = [
            "# Métricas del Modelo - Subsistema 5",
            "",
            f"**Última actualización:** {self.timestamp:%Y-%m-%d %H:%M:%S}",
            f"**Muestras evaluadas:** {self.metrics.get('sample_count', 0)}",
            "",
            "---",
            "",
            "## Resumen ejecutivo",
            "",
            f"- Accuracy (evaluación): {self._format_percent(self.metrics.get('eval_accuracy'))}",
            f"- Loss (evaluación): {self.metrics.get('test_loss', 0.0):.4f}",
            f"- Macro Precision: {self._format_percent(self.metrics.get('macro_precision'))}",
            f"- Macro Recall: {self._format_percent(self.metrics.get('macro_recall'))}",
            f"- Macro F1-Score: {self._format_percent(self.metrics.get('macro_f1'))}",
            f"- ROC AUC (OvR): {self.metrics.get('roc_auc_ovr', 0.0):.4f}",
            f"- Errores totales detectados: {self.metrics.get('misclassified', 0)}",
            "",
            "---",
            "",
            "## Precisión por clase",
            "",
            "| Clase | Accuracy | Soporte |",
            "| --- | --- | --- |",
            per_class_rows,
            "",
            "---",
            "",
            "## Confusiones principales",
            "",
            confusions_section,
            "",
            "---",
            "",
            "## Referencia de métricas",
            "",
            "- **Accuracy:** Porcentaje de predicciones correctas sobre el total.",
            "- **Precision:** Proporción de verdaderos positivos sobre todas las predicciones positivas.",
            "- **Recall:** Proporción de verdaderos positivos sobre todas las muestras positivas reales.",
            "- **F1-Score:** Media armónica entre precision y recall.",
            "- **ROC AUC:** Área bajo la curva ROC para clasificación multiclase (One-vs-Rest).",
        ]

        self._write_file("METRICAS.md", "\n".join(lines))

    def build_estado_proyecto(self) -> None:
        evidencias = Counter(item.get("kind", "otros") for item in self.manifest.get("items", []))
        progreso = 100 if self.metrics and evidencias.get("gif", 0) >= 6 and evidencias.get("screenshot", 0) >= 10 else 80

        lines = [
            "# Estado del Proyecto - Subsistema 5",
            "",
            f"**Fecha:** {self.timestamp:%d de %B de %Y}",
            "**Subsistema:** 5 - Entrenamiento y Comparación de Modelos CNN",
            f"**Progreso estimado:** {progreso}%",
            "",
            "---",
            "",
            "## Resumen ejecutivo",
            "",
            f"- ✅ Modelo entrenado y guardado (`results/models/`).",
            f"- ✅ Evidencias visuales generadas ({evidencias.get('gif', 0)} GIFs, {evidencias.get('screenshot', 0)} capturas).",
            "- ✅ Documentación actualizada automáticamente.",
            "- ⚠ Video demo pendiente (opcional, `record_demo_video.py`).",
            "",
            "---",
            "",
            "## Checklist rápido",
            "",
            "- [x] Entrenamiento CNN (`simple_cnn.py`).",
            "- [x] Pruebas de validación (`test_model.py`).",
            "- [x] Generación de evidencias (`generate_evidence.py`).",
            "- [x] Actualización de documentación (`update_documentation.py`).",
            "- [ ] Video showcase (opcional, por grabar).",
            "",
            "---",
            "",
            "## Próximos pasos sugeridos",
            "",
            "1. Grabar y publicar un video corto (30-60 s) con `record_demo_video.py`.",
            "2. Revalidar métricas si se entrena un nuevo modelo.",
            "3. Compartir la carpeta `ENTREGA_FINAL/` como entregable final.",
        ]

        self._write_file("ESTADO_PROYECTO.md", "\n".join(lines))
    def build_quick_demo(self) -> None:
        lines = [
            "# Quick Demo Script - Subsistema 5",
            "",
            "## 1. Configuración rápida",
            "",
            "```powershell",
            "cd python/training",
            "python -m venv .venv",
            ".venv\\Scripts\\activate",
            "pip install -r requirements.txt",
            "```",
            "",
            "## 2. Ejecución completa (recomendado)",
            "",
            "```powershell",
            "python run_complete_automation.py",
            "```",
            "",
            "El script ejecuta automáticamente:",
            "1. Verificación del entorno y del modelo.",
            "2. Generación de evidencias (GIFs + capturas + métricas).",
            "3. Actualización de documentación.",
            "4. Ejecución de pruebas rápidas.",
            "5. Empaquetado en `ENTREGA_FINAL/`.",
            "",
            "## 3. Ejecución manual por etapas (avanzado)",
            "",
            "```powershell",
            "# Entrenar modelo rápido",
            "python simple_cnn.py",
            "",
            "# Probar modelo",
            "python test_model.py",
            "",
            "# Generar evidencias visuales",
            "python generate_evidence.py",
            "",
            "# Actualizar documentación",
            "python update_documentation.py",
            "```",
            "",
            "## 4. Visualización de resultados",
            "",
            "- Evidencias: `results/evidencias/`",
            "- Modelos: `results/models/`",
            "- Dashboard (opcional): `streamlit run dashboard.py`",
            "- Entrega final consolidada: `ENTREGA_FINAL/`",
        ]

        self._write_file("QUICK_DEMO.md", "\n".join(lines))

    # ------------------------------------------------------------------
    # Runner
    # ------------------------------------------------------------------
    def run(self) -> None:
        if not self.docs_path.exists():
            raise FileNotFoundError(f"Directorio de documentación inexistente: {self.docs_path}")

        self.build_evidencias()
        self.build_metricas()
        self.build_estado_proyecto()
        self.build_quick_demo()


if __name__ == "__main__":
    updater = DocumentationUpdater()
    updater.run()
