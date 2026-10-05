import os
import django

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

from langchain_core.documents import Document

from backend.models import product
from .embedding import get_embeddings
from .vector_store import (
    QdrantVectorStore,
    COLLECTION_NAME,
    QDRANT_PATH,
)


def create_product_documents():

    products = product.objects.filter(status=0)

    documents = []

    for item in products:

        category_name = item.category_name.name if item.category_name else "Unknown"

        content = f"""
Product Name: {item.name}
Category: {category_name}
Vendor: {item.vendor_name}
Description: {item.description}
Original Price: ₹{item.original_price}
Selling Price: ₹{item.selling_price}
Stock: {item.quantity}
Trending: {"Yes" if item.trending else "No"}
""".strip()

        metadata = {
            "product_id": item.id,
            "name": item.name,
            "category": category_name,
            "vendor": item.vendor_name,
            "selling_price": float(item.selling_price),
            "quantity": item.quantity,
            "trending": bool(item.trending),
        }

        documents.append(
            Document(
                page_content=content,
                metadata=metadata,
            )
        )

    return documents


def ingest_products():

    print("Fetching products from MySQL...")

    documents = create_product_documents()

    print(f"Products found: {len(documents)}")

    if not documents:
        print("No active products found.")
        return

    print("Loading embedding model...")

    embeddings = get_embeddings()

    print("Connecting to Qdrant...")

    print("Creating vector store...")

    vector_store = QdrantVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
    )

    print("================================")
    print("Product ingestion completed!")
    print(f"Products stored: {len(documents)}")
    print(f"Collection: {COLLECTION_NAME}")
    print("================================")


if __name__ == "__main__":
    ingest_products()