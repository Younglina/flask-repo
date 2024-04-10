"""
Author: Younglina younglina0409@outlook.com
Date: 2024-04-10 16:24:25
Description: 
"""

from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import io
import os

from app import app

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/convert/<ctype>", methods=["POST"])
def conver_image(ctype):
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No file selected for uploading"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        img = Image.open(filepath)
        img_io = io.BytesIO()
        types = {
            "jpg2png": {"format": "PNG", "nfix": "png"},
            "png2jpg": {"format": "JPEG", "nfix": "jpg"},
        }
        img.save(img_io, types[ctype]["format"])
        img_io.seek(0)

        # os.remove(filepath)
        return send_file(
            img_io,
            as_attachment=True,
            mimetype="image/png",
            download_name=f"{os.path.splitext(filename)[0]}.{types[ctype]['nfix']}",
        )
