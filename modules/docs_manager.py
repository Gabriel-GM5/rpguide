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

        # Load from local knowledge path (skip when not configured)
        if not self.local_knowledge_path:
            knowledge_dir = None
        else:
            knowledge_dir = base_dir / self.local_knowledge_path

        for file in (knowledge_dir.glob("**/*") if knowledge_dir else []):
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

        # Load uploaded files
        try:
            upload_dir = Path("uploads")
            if upload_dir.exists():
                for file in upload_dir.glob("**/*"):
                    if not file.is_file():
                        continue
                    
                    ext = file.suffix.lower()
                    
                    # Use the same loaders for uploaded files
                    loader_cls = self.specialized_loaders.get(ext)
                    if loader_cls:
                        try:
                            docs.extend(self._load(loader_cls, file))
                            if config.DEBUG:
                                print(
                                    f"{self.config.texts['file']} {file.name} "
                                    f"{self.config.texts['loaded.successfully']} (uploaded)"
                                )
                            continue
                        except Exception as e:
                            if config.DEBUG:
                                print(
                                    f"{self.config.texts['file.loading.error']} "
                                    f"{file.name} (uploaded): {e}"
                                )
                    
                    # Fallback for uploaded files
                    try:
                        loader = UnstructuredLoader(str(file))
                        docs.extend(loader.load())
                        if config.DEBUG:
                            print(
                                f"{self.config.texts['file']} {file.name} "
                                f"{self.config.texts['loaded.successfully']} (uploaded fallback)"
                            )
                    except Exception as e:
                        if config.DEBUG:
                            print(
                                f"{self.config.texts['file.loading.error']} "
                                f"{file.name} (uploaded fallback): {e}"
                            )
        except Exception as e:
            if config.DEBUG:
                print(f"Error loading uploaded files: {e}")

        return docs