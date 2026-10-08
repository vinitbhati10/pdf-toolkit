from pypdf import PdfReader, PdfWriter


def rotate_pdf(input_path, output_path, angle):

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(angle)
        writer.add_page(page)

    with open(output_path, "wb") as output:
        writer.write(output)

    return output_path