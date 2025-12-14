from flask import Flask, request, jsonify, send_file
from hybrid.generator import generate_qr, generate_barcode
from hybrid.scanner import scan_image
import os

def create_app():
    app = Flask(__name__)

    @app.route("/generate/qr", methods=["POST"])
    def api_generate_qr():
        payload = request.json or {}
        data = payload.get("data")
        if not data:
            return jsonify({"error": "missing data"}), 400
        filename = payload.get("filename", "api_qr.png")
        path = generate_qr(data, filename=filename)
        return send_file(path, mimetype="image/png")

    @app.route("/generate/barcode", methods=["POST"])
    def api_generate_barcode():
        payload = request.json or {}
        data = payload.get("data")
        if not data:
            return jsonify({"error": "missing data"}), 400
        filename = payload.get("filename", "api_barcode.png")
        path = generate_barcode(data, filename=filename)
        return send_file(path, mimetype="image/png")

    @app.route("/scan", methods=["POST"])
    def api_scan():
        if "file" not in request.files:
            return jsonify({"error": "no file provided"}), 400
        f = request.files["file"]
        save_path = f"./assets/uploads/{f.filename}"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        f.save(save_path)
        results = scan_image(save_path)
        return jsonify({"file": f.filename, "results": results})

    return app
