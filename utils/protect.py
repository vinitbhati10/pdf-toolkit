from pypdf import PdfReader, PdfWriter


def protect_pdf(input_path, output_path, password):

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open(output_path, "wb") as output:
        writer.write(output)

    return output_path