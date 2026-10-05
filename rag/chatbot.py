from langchain_groq import ChatGroq
from dotenv import load_dotenv
from .retriever import search_products
load_dotenv()

def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.3,
    )

def handle_small_talk(question):
    text = question.lower().strip()
    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening",
    ]

    thanks = [
        "thanks",
        "thank you",
        "thank u",
        "thanks a lot",
    ]

    goodbye = [
        "bye",
        "goodbye",
        "see you",
        "see ya",
    ]

    if any(word in text for word in goodbye) and any(
        word in text for word in thanks
    ):
        return "You're welcome! 👋 Thanks for shopping with us. Have a great day! 🛍️"

    if any(word in text for word in goodbye):
        return "Bye! 👋 Thanks for shopping with us. Have a great day! 🛍️"

    if any(word in text for word in thanks):
        return "You're welcome! 😊 Happy shopping! 🛍️"

    if text in greetings:
        return "Hi! 👋 How can I help you with your shopping today? 🛍️"

    return None

def answer_question(question):

    # Handle greetings / thanks / goodbye
    small_talk_response = handle_small_talk(question)
    if small_talk_response:
        return small_talk_response

    # Otherwise use RAG
    results = search_products(question, k=5)
    if not results:
        return "Sorry, I couldn't find any relevant products."

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    prompt = f"""
    You are an AI shopping assistant for our fashion e-commerce store.

    Your job is to help customers discover products using ONLY the
    product information provided below.

    Guidelines:
    - Be friendly and conversational.
    - Give concise answers.
    - Use product names, prices, and useful product details.
    - When listing multiple products, use bullet points.
    - Use Markdown formatting for product names.
    - Do not invent products, prices, stock, or features.
    - If no relevant product is available, clearly say so.
    - Do not mention RAG, Qdrant, embeddings, or LLMs.

    PRODUCT CONTEXT:
    {context}

    CUSTOMER QUESTION:
    {question}

    Give the customer a helpful shopping response.
    """
    llm = get_llm()
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    question = "I need a casual top for summer"
    answer = answer_question(question)

    print("\n==============================")
    print("AI SHOPPING ASSISTANT")
    print("==============================")
    print(answer)