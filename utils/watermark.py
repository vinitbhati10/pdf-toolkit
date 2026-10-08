from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
import io


def add_watermark(input_path, output_path, text):

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:

        # Get page size
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # Create temporary watermark PDF in memory
        packet = io.BytesIO()

        canvas_obj = canvas.Canvas(
            packet,
            pagesize=(width, height)
        )

        # Watermark appearance
        canvas_obj.setFillColor(
            Color(0.4, 0.4, 0.4, alpha=0.60)
        )

        canvas_obj.setFont(
            "Helvetica-Bold",
            50
        )

        # Rotate watermark
        canvas_obj.saveState()

        canvas_obj.translate(
            width / 2,
            height / 2
        )

        canvas_obj.rotate(45)

        canvas_obj.drawCentredString(
            0,
            0,
            text
        )

        canvas_obj.restoreState()

        canvas_obj.save()

        packet.seek(0)

        watermark_reader = PdfReader(packet)

        watermark_page = watermark_reader.pages[0]

        # Put watermark over the original page
        page.merge_page(watermark_page)

        writer.add_page(page)

    with open(output_path, "wb") as output:
        writer.write(output)

    return output_path