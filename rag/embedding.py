from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

if __name__ == "__main__":
    embeddings = get_embeddings()
    text = "Ribbed Knit Top premium casual fashion"
    vector = embeddings.embed_query(text)
    print("Embedding created successfully!")
    print("Vector dimension:", len(vector))
    print("First 5 values:", vector[:5])