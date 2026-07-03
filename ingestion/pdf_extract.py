from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io
import uuid


ROOT_FOLDER = Path("tender_docs")


def discover_pdf_documents(root_folder):
    """
    Returns a list of PDF document metadata.
    """

    documents = []

    for folder in root_folder.iterdir():

        if not folder.is_dir() or folder.name.split('_')[0]!="vendor":
            continue

        for pdf_file in folder.rglob("*.pdf"):

            documents.append({
                "doc_id": str(uuid.uuid4()),     # optional if you use UUID
                "doc_name": pdf_file.name,
                "doc_path": str(pdf_file.resolve()),
                "doc_type": pdf_file.suffix.lower().replace(".", ""),
                "vendor_name": folder.name
            })

    return documents


def extract_pdf(doc_info):
    """
    Extract text and images from a PDF.

    Returns:
        text_chunks
        image_records
    """

    pdf = fitz.open(doc_info["doc_path"])

    text_chunks = []
    image_records = []

    for page_number, page in enumerate(pdf, start=1):

        ###########################################################
        # TEXT
        ###########################################################

        text = page.get_text("text").strip()

        if text:

            text_chunks.append({

                "chunk_id": str(uuid.uuid4()),
                "doc_id": doc_info["doc_id"],
                "vendor_name": doc_info["vendor_name"],
                "page_number": page_number,
                "chunk_text": text

            })

        ###########################################################
        # IMAGES
        ###########################################################

        image_list = page.get_images(full=True)

        for image_index, image in enumerate(image_list):

            xref = image[0]

            base_image = pdf.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            pil_image = Image.open(io.BytesIO(image_bytes))

            image_records.append({

                "image_id": str(uuid.uuid4()),
                "doc_id": doc_info["doc_id"],
                "vendor_name": doc_info["vendor_name"],
                "page_number": page_number,
                "image_index": image_index,
                "image": pil_image,
                "image_extension": image_ext

            })

    pdf.close()

    return text_chunks, image_records


def main():

    documents = discover_pdf_documents(ROOT_FOLDER)

    print(f"Found {len(documents)} PDF(s)\n")

    all_text = []
    all_images = []

    for doc in documents:

        print(f"Processing: {doc['doc_name']}")

        text_chunks, image_records = extract_pdf(doc)

        all_text.extend(text_chunks)
        all_images.extend(image_records)

    print(f"\nDocuments : {len(documents)}")
    print(f"Text chunks : {len(all_text)}")
    print(f"Images : {len(all_images)}")


if __name__ == "__main__":
    main()