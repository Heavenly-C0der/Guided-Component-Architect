from flask import Flask, request, jsonify
from pathlib import Path
import os

from generator import ComponentGenerator
from validator import ComponentValidator
from architect import GuidedComponentArchitect
from llm_client import LLMClient
from preview import wrap_preview

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
design_system_path = BASE_DIR / "system_design.json"

llm_client = LLMClient(api_key=os.getenv("HF_TOKEN"))
generator = ComponentGenerator(llm_client, design_system_path)
validator = ComponentValidator(design_system_path)
architect = GuidedComponentArchitect(generator, validator, llm_client)


@app.route("/", methods=["GET"])
def health():
    return {"status": "ok"}


@app.route("/generate", methods=["POST"])
def generate():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        structured = architect.run(prompt, max_retries=5)

        preview_html = wrap_preview(
            structured["preview_markup"],
            generator.design_system["tokens"]
        )

        return jsonify({
            "angular_code": structured["angular_code"],
            "preview_html": preview_html
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


