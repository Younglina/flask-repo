from flask import Flask, request, send_file, jsonify
import fitz
import zipfile
import base64

from PIL import Image

# import aspose.words as aw
import io
import os
from app import app

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/api/downloadAll/<ctype>", methods=["GET"])
def download_zip(ctype):
    uuid = str(request.args.get("uuid"))
    zip_path = os.path.join(app.config["UPLOAD_FOLDER"], uuid)
    to_zip(zip_path, ctype)
    if os.path.exists(zip_path):
        return send_file(os.path.join(zip_path, f'{ctype}.zip'), as_attachment=True, download_name=f'{ctype}.zip')
    else:
        return 'File not found', 404

@app.route("/api/convert/<ctype>", methods=["POST"])
def conver_image(ctype):
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No file selected for uploading"}), 400

    if file:
        uuid_v4 = str(request.form.get("uuid"))
        notype_name = os.path.splitext(file.filename)[0]
        directory = os.path.join(app.config["UPLOAD_FOLDER"], uuid_v4)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], uuid_v4, file.filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file.save(filepath)
        pass
        if ctype == "word2jpg":
            # word2jpgAspose(filepath, filename)
            return {"code": 200}
        if ctype == "pdf2png":
            pdf2png(filepath, directory, notype_name)
            to_zip(directory, notype_name, uuid_v4)
            with open(
                os.path.join(directory, f"{notype_name}0.png"), "rb"
            ) as image_file:
                image_data = image_file.read()
                base64_data = base64.b64encode(image_data).decode("utf-8")
                return {"code": 200, "data": base64_data}
        else:
            img = Image.open(filepath)
            img_io = io.BytesIO()
            types = {
                "jpg2png": {"format": "PNG", "nfix": "png"},
                "png2jpg": {"format": "JPEG", "nfix": "jpg"},
            }
            # 如果图像模式为RGBA，则转换为RGB
            if img.mode == "RGBA":
                img = img.convert("RGB")
            img.save(img_io, types[ctype]["format"])
            img_io.seek(0)
            # 将图像转换为base64字符串
            base64_img = base64.b64encode(img_io.getvalue()).decode("utf-8")
            return {"code": 200, "data": base64_img}
            # os.remove(filepath)
            # return send_file(
            #     img_io,
            #     as_attachment=True,
            #     mimetype="image/png",
            #     download_name=f"{notype_name}.{types[ctype]['nfix']}",
            # )


def pdf2png(filepath, directory, notype_name):
    doc = fitz.open(filepath)
    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        image_bytes = page.get_pixmap(dpi=300).tobytes("png")
        image_filename = f"{notype_name}{page_index}.png"
        image_path = os.path.join(directory, image_filename)
        with open(image_path, "wb") as f:
            f.write(image_bytes)


def to_zip(directory, notype_name):
    with zipfile.ZipFile(
        f"{os.path.join(directory, notype_name)}.zip", "w", zipfile.ZIP_DEFLATED
    ) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith((".png", ".jpg", "jpeg")):
                    abs_file_path = os.path.join(root, file)
                    zipf.write(
                        abs_file_path,
                        os.path.basename(file),
                    )


# def word2jpgAspose(filepath, filename):
#     doc = aw.Document(filepath)
#     options = aw.saving.ImageSaveOptions(aw.SaveFormat.JPEG)

#     for pageNumber in range(doc.page_count):
#         options.page_set = aw.saving.PageSet(pageNumber)
#         img_name = os.path.splitext(filename)[0] + str(pageNumber) + ".jpg"
#         doc.save(img_name, options)
