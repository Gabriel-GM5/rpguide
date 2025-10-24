from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path

class DocsManager:
    def __init__(self, config):
        self.local_knowledge_path = config.LOCAL_KNOWLEDGE_PATH
        self.local_knowledge_doc_types = config.LOCAL_KNOWLEDGE_DOC_TYPES
        self.config = config


    def getDocs(self):
        docs = []
        base_dir = Path(__file__).resolve().parent.parent
        for type in self.local_knowledge_doc_types:
            match type:
                case "pdfs":
                    for doc in base_dir.joinpath(self.local_knowledge_path, type).glob("**/*.pdf"):
                        try:
                            loader = PyMuPDFLoader(str(doc))
                            docs.extend(loader.load())
                            print(f"{self.config.texts['file']} {doc.name} {self.config.texts['loaded.successfully']}")
                        except Exception as e:
                            print(f"{self.config.texts['file.loading.error']} {doc.name}: {e}")
                case _:
                    print(f"{self.config.texts['file.type.skipped']}: {type}")
        return docs