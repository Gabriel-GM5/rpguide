from pathlib import Path
from modules.configs import config

from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredRTFLoader,
)

from langchain_unstructured import UnstructuredLoader


class DocsManager:
    def __init__(self, config):
        self.local_knowledge_path = config.LOCAL_KNOWLEDGE_PATH
        self.config = config

        self.specialized_loaders = {
            ".pdf": PyMuPDFLoader,
            ".txt": TextLoader,
            ".csv": CSVLoader,
            ".md": UnstructuredMarkdownLoader,
            ".html": UnstructuredHTMLLoader,
            ".htm": UnstructuredHTMLLoader,

            # Word / Rich text
            ".docx": UnstructuredWordDocumentLoader,
            ".doc": UnstructuredWordDocumentLoader,
            ".rtf": UnstructuredRTFLoader,

            # PowerPoint
            ".pptx": UnstructuredPowerPointLoader,
            ".ppt": UnstructuredPowerPointLoader,
        }

    def _load(self, loader_cls, file_path):
        loader = loader_cls(str(file_path))
        return loader.load()

    def getDocs(self):
        docs = []
        base_dir = Path(__file__).resolve().parent.parent
        knowledge_dir = base_dir / self.local_knowledge_path

        for file in knowledge_dir.glob("**/*"):
            if not file.is_file():
                continue

            # 🚫 Skip dotfiles with no extension (.gitkeep, .env, etc.)
            if file.name.startswith(".") and file.suffix == "":
                continue

            ext = file.suffix.lower()

            # 1️⃣ Specialized loader first
            loader_cls = self.specialized_loaders.get(ext)
            if loader_cls:
                try:
                    docs.extend(self._load(loader_cls, file))
                    if config.DEBUG:
                        print(
                            f"{self.config.texts['file']} {file.name} "
                            f"{self.config.texts['loaded.successfully']} (specialized)"
                        )
                    continue
                except Exception as e:
                    if config.DEBUG:
                        print(
                            f"{self.config.texts['file.loading.error']} "
                            f"{file.name} (specialized): {e}"
                        )

            # 2️⃣ Generic unstructured fallback
            try:
                loader = UnstructuredLoader(str(file))
                docs.extend(loader.load())
                if config.DEBUG:
                    print(
                        f"{self.config.texts['file']} {file.name} "
                        f"{self.config.texts['loaded.successfully']} (unstructured fallback)"
                    )
            except Exception as e:
                if config.DEBUG:
                    print(
                        f"{self.config.texts['file.loading.error']} "
                        f"{file.name} (unstructured): {e}"
                    )

        return docs