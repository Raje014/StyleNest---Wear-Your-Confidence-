from .vector_store import get_vector_store

def search_products(query, k=5):
    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query,
        k=k
    )
    return results

if __name__ == "__main__":

    query = "casual top for women"
    results = search_products(query, k=5)

    print("\n==============================")
    print("SEARCH RESULTS")
    print("==============================")

    for i, doc in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("------------------------------")
        print(doc.page_content)
        print("Metadata:", doc.metadata)