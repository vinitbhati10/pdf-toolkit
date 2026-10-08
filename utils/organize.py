from pypdf import PdfReader, PdfWriter


def organize_pdf(input_path, output_path, page_order):

    reader = PdfReader(input_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    for page_number in page_order:

        if page_number < 0 or page_number >= total_pages:
            raise ValueError("Invalid page number.")

        writer.add_page(
            reader.pages[page_number]
        )

    with open(output_path, "wb") as output:
        writer.write(output)

    return output_path