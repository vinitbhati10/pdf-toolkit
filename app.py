from flask import Flask, render_template, request, jsonify, send_file
import os
import zipfile
from utils.merge import merge_pdfs
from utils.split import split_pdf
from utils.compress import compress_pdf
from utils.rotate import rotate_pdf
from utils.convert import pdf_to_images, images_to_pdf
from utils.watermark import add_watermark
from utils.protect import protect_pdf
from utils.organize import organize_pdf
from pypdf import PdfReader


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file selected"
        })

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected"
        })

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "success": False,
            "message": "Only PDF files are allowed"
        })

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(file_path)

    return jsonify({
        "success": True,
        "message": "PDF uploaded successfully",
        "filename": file.filename
    })

@app.route("/merge", methods=["POST"])
def merge_files():

    try:

        files = request.files.getlist("files")

        if len(files) < 2:
            return jsonify({
                "success": False,
                "message": "Please select at least 2 PDF files"
            }), 400

        pdf_paths = []

        for file in files:

            if file.filename == "":
                continue

            if not file.filename.lower().endswith(".pdf"):
                return jsonify({
                    "success": False,
                    "message": "Only PDF files are allowed"
                }), 400

            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(file_path)

            pdf_paths.append(file_path)

        if len(pdf_paths) < 2:
            return jsonify({
                "success": False,
                "message": "Please select at least 2 PDF files"
            }), 400

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "merged.pdf"
        )

        merge_pdfs(pdf_paths, output_path)

        return jsonify({
            "success": True,
            "message": "PDFs merged successfully",
            "download_url": "/download/merged.pdf"
        })

    except Exception as e:

        print("MERGE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
@app.route("/download/<filename>")
def download_file(filename):

    file_path = os.path.join(
        app.config["OUTPUT_FOLDER"],
        filename
    )

    return send_file(
        file_path,
        as_attachment=True
    )
@app.route("/split", methods=["POST"])
def split_file():

    try:

        file = request.files.get("file")

        if file is None or file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a PDF file."
            }), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({
                "success": False,
                "message": "Only PDF files are allowed."
            }), 400

        start_page = request.form.get("start_page")
        end_page = request.form.get("end_page")

        if not start_page or not end_page:
            return jsonify({
                "success": False,
                "message": "Please enter both start and end pages."
            }), 400

        start_page = int(start_page)
        end_page = int(end_page)

        # Save uploaded PDF
        input_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(input_path)

        # Output file
        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "split.pdf"
        )

        # Split PDF
        split_pdf(
            input_path,
            output_path,
            start_page,
            end_page
        )

        return jsonify({
            "success": True,
            "message": "PDF split successfully!",
            "download_url": "/download/split.pdf"
        })

    except ValueError as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    except Exception as e:

        print("SPLIT ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/compress", methods=["POST"])
def compress_file():

    try:

        file = request.files.get("file")

        if file is None or file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a PDF file."
            }), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({
                "success": False,
                "message": "Only PDF files are allowed."
            }), 400

        input_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(input_path)

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "compressed.pdf"
        )

        compress_pdf(
            input_path,
            output_path
        )

        return jsonify({
            "success": True,
            "message": "PDF compressed successfully!",
            "download_url": "/download/compressed.pdf"
        })

    except Exception as e:

        print("COMPRESS ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/rotate", methods=["POST"])
def rotate_file():

    try:

        file = request.files.get("file")

        if file is None or file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a PDF file."
            }), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({
                "success": False,
                "message": "Only PDF files are allowed."
            }), 400

        angle = request.form.get("angle")

        if not angle:
            return jsonify({
                "success": False,
                "message": "Please select a rotation angle."
            }), 400

        angle = int(angle)

        if angle not in [90, 180, 270]:
            return jsonify({
                "success": False,
                "message": "Rotation must be 90, 180, or 270 degrees."
            }), 400

        input_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(input_path)

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "rotated.pdf"
        )

        rotate_pdf(
            input_path,
            output_path,
            angle
        )

        return jsonify({
            "success": True,
            "message": f"PDF rotated by {angle} degrees!",
            "download_url": "/download/rotated.pdf"
        })

    except Exception as e:

        print("ROTATE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/pdf-to-images", methods=["POST"])
def convert_pdf_to_images():

    try:

        file = request.files.get("file")

        if file is None or file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a PDF file."
            }), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({
                "success": False,
                "message": "Only PDF files are allowed."
            }), 400

        input_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(input_path)

        image_folder = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "converted_images"
        )

        os.makedirs(image_folder, exist_ok=True)

        image_paths = pdf_to_images(
            input_path,
            image_folder
        )

        # Create ZIP file
        zip_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "converted_images.zip"
        )

        with zipfile.ZipFile(
            zip_path,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            for image_path in image_paths:

                zip_file.write(
                    image_path,
                    os.path.basename(image_path)
                )

        return jsonify({
            "success": True,
            "message": f"PDF converted successfully! {len(image_paths)} images created.",
            "download_url": "/download/converted_images.zip"
        })

    except Exception as e:

        print("PDF TO IMAGES ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500 

@app.route("/download-image/<filename>")
def download_image(filename):

    image_folder = os.path.join(
        app.config["OUTPUT_FOLDER"],
        "converted_images"
    )

    file_path = os.path.join(
        image_folder,
        filename
    )

    return send_file(
        file_path,
        as_attachment=True
    ) 

@app.route("/images-to-pdf", methods=["POST"])
def convert_images_to_pdf():

    try:

        files = request.files.getlist("images")

        if not files:
            return jsonify({
                "success": False,
                "message": "Please select at least one image."
            }), 400

        image_paths = []

        for file in files:

            if file.filename == "":
                continue

            filename = file.filename.lower()

            if not filename.endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            ):
                return jsonify({
                    "success": False,
                    "message": "Only JPG, JPEG, PNG, and WEBP images are allowed."
                }), 400

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(image_path)

            image_paths.append(image_path)

        if not image_paths:
            return jsonify({
                "success": False,
                "message": "No valid images were selected."
            }), 400

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "images_to_pdf.pdf"
        )

        images_to_pdf(
            image_paths,
            output_path
        )

        return jsonify({
            "success": True,
            "message": f"{len(image_paths)} images converted to PDF successfully!",
            "download_url": "/download/images_to_pdf.pdf"
        })

    except Exception as e:

        print("IMAGES TO PDF ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/watermark", methods=["POST"])
def watermark_file():

    try:

        file = request.files.get("file")

        if file is None or file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a PDF file."
            }), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({
                "success": False,
                "message": "Only PDF files are allowed."
            }), 400

        text = request.form.get("text")

        if not text or not text.strip():
            return jsonify({
                "success": False,
                "message": "Please enter watermark text."
            }), 400

        input_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(input_path)

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "watermarked.pdf"
        )

        add_watermark(
            input_path,
            output_path,
            text.strip()
        )

        return jsonify({
            "success": True,
            "message": "Watermark added successfully!",
            "download_url": "/download/watermarked.pdf"
        })

    except Exception as e:

        print("WATERMARK ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/protect", methods=["POST"])
def protect_file():

    try:

        file = request.files.get("file")

        if file is None or file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a PDF file."
            }), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({
                "success": False,
                "message": "Only PDF files are allowed."
            }), 400

        password = request.form.get("password")

        if not password:
            return jsonify({
                "success": False,
                "message": "Please enter a password."
            }), 400

        input_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(input_path)

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "protected.pdf"
        )

        protect_pdf(
            input_path,
            output_path,
            password
        )

        return jsonify({
            "success": True,
            "message": "PDF protected successfully!",
            "download_url": "/download/protected.pdf"
        })

    except Exception as e:

        print("PROTECT ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500 

@app.route("/organize", methods=["POST"])
def organize_file():

    try:

        file = request.files.get("file")
        page_order = request.form.get("page_order")

        if file is None or file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a PDF file."
            }), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({
                "success": False,
                "message": "Only PDF files are allowed."
            }), 400

        if not page_order:
            return jsonify({
                "success": False,
                "message": "No page order was provided."
            }), 400

        page_order = [
            int(page)
            for page in page_order.split(",")
        ]

        input_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(input_path)

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "organized.pdf"
        )

        organize_pdf(
            input_path,
            output_path,
            page_order
        )

        return jsonify({
            "success": True,
            "message": "PDF organized successfully!",
            "download_url": "/download/organized.pdf"
        })

    except ValueError as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    except Exception as e:

        print("ORGANIZE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500       

@app.route("/delete-pages", methods=["POST"])
def delete_pages():

    try:

        file = request.files.get("file")
        pages_to_delete = request.form.get("pages")

        if file is None or file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a PDF file."
            }), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({
                "success": False,
                "message": "Only PDF files are allowed."
            }), 400

        if not pages_to_delete:
            return jsonify({
                "success": False,
                "message": "Please enter pages to delete."
            }), 400

        input_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(input_path)

        # Read PDF to determine total pages
        reader = PdfReader(input_path)

        total_pages = len(reader.pages)

        # Convert user input: "2,4,5"
        delete_pages = set()

        for page in pages_to_delete.split(","):

            page = page.strip()

            if page.isdigit():

                page_number = int(page)

                if page_number < 1 or page_number > total_pages:
                    return jsonify({
                        "success": False,
                        "message": f"Page {page_number} does not exist. PDF has {total_pages} pages."
                    }), 400

                delete_pages.add(page_number)

        if not delete_pages:
            return jsonify({
                "success": False,
                "message": "Please enter valid page numbers."
            }), 400

        # Create remaining page order
        page_order = []

        for page_number in range(1, total_pages + 1):

            if page_number not in delete_pages:

                page_order.append(page_number - 1)

        if not page_order:
            return jsonify({
                "success": False,
                "message": "You cannot delete all pages."
            }), 400

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            "pages_deleted.pdf"
        )

        organize_pdf(
            input_path,
            output_path,
            page_order
        )

        return jsonify({
            "success": True,
            "message": "Selected pages deleted successfully!",
            "download_url": "/download/pages_deleted.pdf"
        })

    except Exception as e:

        print("DELETE PAGES ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500    

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)