from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

from .embedding import get_embeddings


COLLECTION_NAME = "ecommerce_products"
QDRANT_PATH = "qdrant_storage"


def get_vector_store():

    client = QdrantClient(path=QDRANT_PATH)

    embeddings = get_embeddings()

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )

    return vector_store