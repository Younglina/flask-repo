from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import fitz
import zipfile
import uuid

from PIL import Image

# import aspose.words as aw
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
        uuid_v4 = uuid.uuid4()
        filename = str(uuid_v4) + "_" + secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        if ctype == "word2jpg":
            # word2jpgAspose(filepath, filename)
            # word_to_pdf(filepath, filename)
            return {"code": 200}
        if ctype == "pdf2jpg":
            pdf2jpg(filepath, filename)
            to_zip(filename)
            return {"code": 200}
        else:
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


def pdf2jpg(filepath, filename):
    doc = fitz.open(filepath)
    temppath = os.path.join(app.config["UPLOAD_FOLDER"])
    tempname = os.path.splitext(filename)[0]
    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        image_bytes = page.get_pixmap(dpi=300).tobytes("png")
        with open(f"{temppath}/{tempname+str(page_index)}.png", "wb") as f:
            f.write(image_bytes)


def to_zip(filename):
    temppath = os.path.join(app.config["UPLOAD_FOLDER"])
    tempname = os.path.splitext(filename)[0]
    with zipfile.ZipFile(f"{tempname}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temppath):
            for file in files:
                if file.startswith(filename) and file.endswith((".png", ".jpg")):
                    abs_file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(abs_file_path, os.path.dirname(temppath))
                    zipf.write(abs_file_path, arc_name)


# def word2jpgAspose(filepath, filename):
#     doc = aw.Document(filepath)
#     options = aw.saving.ImageSaveOptions(aw.SaveFormat.JPEG)

#     for pageNumber in range(doc.page_count):
#         options.page_set = aw.saving.PageSet(pageNumber)
#         img_name = os.path.splitext(filename)[0] + str(pageNumber) + ".jpg"
#         doc.save(img_name, options)
