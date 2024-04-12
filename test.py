"""
Author: Younglina younglina0409@outlook.com
Date: 2024-04-12 15:54:03
Description: 
"""

import subprocess


def generate_pdf(doc_path, path):

    subprocess.call(
        [
            "soffice",
            # '--headless',
            "--convert-to",
            "pdf",
            "--outdir",
            path,
            doc_path,
        ]
    )
    return doc_path


generate_pdf("soul-ui.docx", "output_path.pdf")
