from pathlib import Path

from annotated_types import doc
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import EMBEDDING_MODEL, VECTOR_DB_PATH
import os
import fitz
from pathlib import Path

def extract_pdf_images(pdf_path, output_folder):

    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    pdf = fitz.open(pdf_path)

    image_paths = []

    for page_number, page in enumerate(pdf):

        images = page.get_images(full=True)

        for image_number, image in enumerate(images):

            xref = image[0]

            base_image = pdf.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_name = (
                f"{Path(pdf_path).stem}"
                f"_page_{page_number + 1}"
                f"_image_{image_number + 1}."
                f"{image_ext}"
            )

            image_path = output_folder / image_name

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_paths.append({
                "page": page_number + 1,
                "path": str(image_path)
            })

    pdf.close()

    return image_paths

def build_vectorstore():

    documents_path = Path("documents")

    pdf_files = list(documents_path.glob("*.pdf"))

    print(f"PDFs found: {len(pdf_files)}")

    all_docs = []

    for pdf_file in pdf_files:

        print(f"Loading: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()

        # Extract images from this PDF
        images = extract_pdf_images(
            pdf_file,
            "extracted_images"
        )

        for doc in docs:

            page_number = doc.metadata.get("page", 0) + 1

            doc.metadata["source"] = pdf_file.name
            doc.metadata["page"] = page_number

            # Images belonging to this page
            page_images = [
                image["path"]
                for image in images
                if image["page"] == page_number
            ]

            doc.metadata["images"] = page_images

        print(f"Pages loaded: {len(docs)}")

        all_docs.extend(docs)

    print(f"Total pages: {len(all_docs)}")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile"
    )

    chunks = splitter.split_documents(all_docs)

    print(f"Total semantic chunks: {len(chunks)}")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(VECTOR_DB_PATH)

    print(f"FAISS database saved to: {VECTOR_DB_PATH}")

    return vectorstore


def load_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    index_file = os.path.join(
        VECTOR_DB_PATH,
        "index.faiss"
    )

    if os.path.exists(index_file):

        return FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    return build_vectorstore()