from src.config.settings import CORPUS_PATH
from src.ingest.loader import load_corpus
def main():
    docs = load_corpus(CORPUS_PATH)
    for doc in docs:
        print(doc)
        break
    print(f"Loaded {len(docs)} documents from {CORPUS_PATH}")


if __name__ == "__main__":
    main()
