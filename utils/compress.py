from pypdf import PdfReader, PdfWriter


def compress_pdf(input_path, output_path):

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:

        # First add the page to the writer
        writer.add_page(page)

        # Then compress the page
        writer.pages[-1].compress_content_streams()

    with open(output_path, "wb") as output:
        writer.write(output)

    return output_path