import fitz, io, uuid, imagehash
from pathlib import Path
from PIL import Image

class PDFExtractor:

    def __init__(self, root_folder: str, image_output_folder: str):

        # Declare the folder containing the tender documents
        self.root_folder = Path(root_folder)
        # Declare the folder holding the extracted images
        self.image_output_folder = Path(image_output_folder)
        # Create the extracted images folder if it doesn't exist
        self.image_output_folder.mkdir(parents=True, exist_ok=True)

    ####################################################################
    # Discover all PDFs
    ####################################################################

    def discover_documents(self):
        """
        Returns a list of PDF document metadata.
        """

        documents = []

        for folder in self.root_folder.iterdir():
            
            # ignore loose documents not in any folder
            if not folder.is_dir():
                continue
            
            # search recursively for pdf documents in each detected folder
            for pdf_path in folder.rglob("*.pdf"):
                documents.append({
                    "doc_id": str(uuid.uuid4()),
                    "doc_name": pdf_path.name,
                    "doc_path": str(pdf_path.resolve()),
                    "doc_type": "pdf",
                    "vendor_name": folder.name.lower() if "tender_spec" not in folder.name.lower() else "tender_spec"
                })
        
        return documents

    ####################################################################
    # Extract text and image from PDF
    ####################################################################

    def extract_pdf(self, document):
        """
        Extract text and images from a PDF.

        Returns:
             text_chunks
             image_records
        """

        pdf = fitz.open(document["doc_path"])

        pages = []
        images = []
        #full_text = ""
        current_offset = 0

        # Iterating through the pages
        for page_number, page in enumerate(pdf, start=1):
            # Extract the text
            text = page.get_text("text").strip()

            if text:
                # get the starting character position for each page
                start_offset = current_offset
                #full_text += text + "\n\n"
                current_offset += len(text)
                # calculate the ending character position for each page
                end_offset = current_offset
                
                pages.append({
                    "doc_id": document["doc_id"],
                    "page_number": page_number,
                    "start_offset": start_offset,
                    "end_offset": end_offset,
                    "page_text": text
                })
            
            # Extract the images
            image_list = page.get_images(full=True)

            if image_list:
                for image_index, image in enumerate(image_list, start=1):
                    # get the image object identifier
                    xref = image[0]
                    # extract the binary data and then the raw bytes
                    image_data = pdf.extract_image(xref)
                    image_bytes = image_data["image"]
                    # extract the image file type
                    extension = image_data["ext"]
                    # load the raw bytes as PIL image
                    image = Image.open(io.BytesIO(image_bytes))
                    # Generate the image hash
                    phash = str(imagehash.phash(image))
                    # define the filepath to save the extracted image and then save the image
                    filename = f'{document["vendor_name"]}_{Path(document["doc_name"]).stem}_page{page_number}_img{image_index}.{extension}'
                    output_path = self.image_output_folder/filename
                    image.save(output_path)
                        #with open(output_path, "wb") as f:
                        #    f.write(image_bytes)
                    
                    images.append({
                        "image_id": str(uuid.uuid4()),
                        "image_path": str(output_path),
                        "doc_id": document["doc_id"],
                        "page_number": page_number,
                        "phash": phash
                        })
        
        pdf.close()

        return pages, images 


# next work on insert into DB, then seperate .py for chunking
https://chatgpt.com/c/6a4fbfb0-2874-83ec-975c-206a5fa91db0



# if __name__ == "__main__":
#     main()