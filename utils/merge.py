from pypdf import PdfWriter


def merge_pdfs(pdf_files, output_path):
    writer = PdfWriter()

    for pdf_file in pdf_files:
        writer.append(pdf_file)

    with open(output_path, "wb") as output:
        writer.write(output)

    return output_path