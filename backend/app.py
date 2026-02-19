from flask import Flask, request, jsonify
from pathlib import Path
import json
import os

from generator import ComponentGenerator
from validator import ComponentValidator
from architect import GuidedComponentArchitect
from llm_client import LLMClient
from preview import wrap_preview   #

app = Flask(__name__)

design_system_path = Path("system_design.json")

llm_client = LLMClient(api_key=os.getenv("HF_API_KEY"))
generator = ComponentGenerator(llm_client, design_system_path)
validator = ComponentValidator(design_system_path)
architect = GuidedComponentArchitect(generator, validator, llm_client)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    prompt = data.get("prompt", "")

    try:
        structured = architect.run(prompt, max_retries=1)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
