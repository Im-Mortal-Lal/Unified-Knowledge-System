from config import *


def retrieve_context(vectorstore, query):

    docs = vectorstore.similarity_search(
        query,
        k=TOP_K
    )

    print("\n========== RETRIEVAL ==========")
    print("QUERY:", query)

    for i, doc in enumerate(docs):

        print(f"\n--- RESULT {i + 1} ---")
        print("SOURCE:", doc.metadata.get("source"))
        print("PAGE:", doc.metadata.get("page"))

        print("IMAGES:", doc.metadata.get("images", []))

        print("CONTENT:")
        print(doc.page_content[:1000])

    print("\n===============================\n")

    context = "\n\n".join(
        f"""
Source: {doc.metadata.get('source', 'Unknown')}
Page: {doc.metadata.get('page', 'Unknown')}

Content:
{doc.page_content}
"""
        for doc in docs
    )

    return context, docs