from pypdf import PdfReader, PdfWriter


def split_pdf(input_path, output_path, start_page, end_page):

    reader = PdfReader(input_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    # Validate page numbers
    if start_page < 1 or end_page > total_pages:
        raise ValueError(
            f"PDF has {total_pages} pages. "
            f"Please enter a range between 1 and {total_pages}."
        )

    if start_page > end_page:
        raise ValueError(
            "Starting page cannot be greater than ending page."
        )

    # Convert to Python's 0-based index
    for page_number in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_number])

    with open(output_path, "wb") as output:
        writer.write(output)

    return output_path