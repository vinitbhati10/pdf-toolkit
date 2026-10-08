import fitz


def pdf_to_images(input_path, output_folder):

    pdf = fitz.open(input_path)

    image_paths = []

    for page_number, page in enumerate(pdf):

        pix = page.get_pixmap()

        image_path = (
            f"{output_folder}/page_{page_number + 1}.png"
        )

        pix.save(image_path)

        image_paths.append(image_path)

    pdf.close()

    return image_paths

from PIL import Image


def images_to_pdf(image_paths, output_path):

    images = []

    for image_path in image_paths:

        image = Image.open(image_path)

        # Convert image to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        images.append(image)

    if not images:
        raise ValueError("No images were provided.")

    # Save all images as one PDF
    first_image = images[0]

    first_image.save(
        output_path,
        save_all=True,
        append_images=images[1:]
    )

    # Close images
    for image in images:
        image.close()

    return output_path