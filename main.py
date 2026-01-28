from rag.pipeline import RAGPipeline

rag = RAGPipeline()

rag.index_folder("books")

while True:
    q = input("\nAsk Question (or type exit): ")
    if q.lower() == "exit":
        break

    answer = rag.ask(q)
    print("\n Answer:\n", answer)
