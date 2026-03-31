from pathlib import Path

from langchain_community.document_loaders import (
    CSVLoader,
    Docx2txtLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
)

def _build_loader(file_path: Path):
    suffix = file_path.suffix.lower()
    match suffix:
        case ".pdf":
            return PyPDFLoader(str(file_path))
        case ".csv":
            return CSVLoader(str(file_path))
        case ".json":
            return JSONLoader(str(file_path), jq_schema=".", text_content=False)
        case ".jsonl":
            return JSONLoader(
                str(file_path),
                jq_schema=".",
                text_content=False,
                json_lines=True,
            )
        case ".docx":
            return Docx2txtLoader(str(file_path))
        case ".txt" | ".md" | ".html":
            return TextLoader(str(file_path), encoding="utf-8")
        case _:
            return None


def load_corpus(corpus_path: str):
    if not corpus_path:
        raise ValueError("Corpus path is required")

    source_path = Path(corpus_path)
    if not source_path.exists():
        raise FileNotFoundError(f"Corpus path does not exist: {source_path}")
    if not source_path.is_dir():
        raise NotADirectoryError(f"Corpus path is not a directory: {source_path}")

    all_documents = []
    for file_path in source_path.rglob("*"):
        if not file_path.is_file():
            continue

        loader = _build_loader(file_path)
        if loader is None:
            continue

        all_documents.extend(loader.load())

    return all_documents


def main():
    from src.config.settings import CORPUS_PATH
    docs = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(docs)} documents from {CORPUS_PATH}")


if __name__ == "__main__":
    main()