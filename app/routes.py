from flask import Flask, request, send_file, jsonify
import fitz
import zipfile
import uuid
import base64

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
        origin_name = file.filename
        notype_name = os.path.splitext(origin_name)[0]
        uid_filename = str(uuid_v4) + "_" + origin_name
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], uid_filename)
        file.save(filepath)

        if ctype == "word2jpg":
            # word2jpgAspose(filepath, filename)
            return {"code": 200}
        if ctype == "pdf2jpg":
            pdf2jpg(filepath, uid_filename)
            to_zip(notype_name, uuid_v4=str(uuid_v4))
            return {"code": 200}
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


def pdf2jpg(filepath, uid_filename):
    doc = fitz.open(filepath)
    temppath = os.path.join(app.config["UPLOAD_FOLDER"])
    tempname = os.path.splitext(uid_filename)[0]
    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        image_bytes = page.get_pixmap(dpi=300).tobytes("png")
        image_filename = f"{tempname}{page_index}.png"
        image_path = os.path.join(temppath, image_filename)
        with open(image_path, "wb") as f:
            f.write(image_bytes)


def to_zip(notype_name, uuid_v4):
    temppath = os.path.join(app.config["UPLOAD_FOLDER"])
    with zipfile.ZipFile(
        f"{os.path.join(temppath, notype_name)}.zip", "w", zipfile.ZIP_DEFLATED
    ) as zipf:
        for root, _, files in os.walk(temppath):
            for file in files:
                if file.startswith(uuid_v4) and file.endswith((".png", ".jpg")):
                    abs_file_path = os.path.join(root, file)
                    zipf.write(
                        abs_file_path,
                        os.path.basename(file.replace(uuid_v4 + "_", "")),
                    )


# def word2jpgAspose(filepath, filename):
#     doc = aw.Document(filepath)
#     options = aw.saving.ImageSaveOptions(aw.SaveFormat.JPEG)

#     for pageNumber in range(doc.page_count):
#         options.page_set = aw.saving.PageSet(pageNumber)
#         img_name = os.path.splitext(filename)[0] + str(pageNumber) + ".jpg"
#         doc.save(img_name, options)
