# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for rpguide — one-dir build with GUI icon."""

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

block_cipher = None

# ── LangChain family ──────────────────────────────────────────────────────────
lc_d,   lc_b,   lc_h   = collect_all("langchain")
lcc_d,  lcc_b,  lcc_h  = collect_all("langchain_community")
lck_d,  lck_b,  lck_h  = collect_all("langchain_core")
lcg_d,  lcg_b,  lcg_h  = collect_all("langchain_google_genai")
lcu_d,  lcu_b,  lcu_h  = collect_all("langchain_unstructured")
lcx_d,  lcx_b,  lcx_h  = collect_all("langchain_classic")

# ── UI ────────────────────────────────────────────────────────────────────────
ttk_d,  ttk_b,  ttk_h  = collect_all("ttkbootstrap")

all_datas = (
    lc_d + lcc_d + lck_d + lcg_d + lcu_d + lcx_d + ttk_d
    + [
        ("modules/prompts", "modules/prompts"),
        ("texts",           "texts"),
        (".env.example",    "."),
    ]
)
all_binaries = lc_b + lcc_b + lck_b + lcg_b + lcu_b + lcx_b + ttk_b

all_hidden = (
    lc_h + lcc_h + lck_h + lcg_h + lcu_h + lcx_h + ttk_h
    + collect_submodules("modules.connectors")
    + [
        # provider connectors (loaded dynamically via LLM_TYPE env var)
        "modules.connectors.gemini_connector",
        "modules.connectors.openai_connector",
        "modules.connectors.lmstudio_connector",
        "modules.connectors.ollama_connector",
        "modules.connectors.anthropic_connector",
        # FAISS / ML
        "faiss",
        "faiss.swigfaiss",
        # Document loaders
        "pymupdf",
        "fitz",
        "docx2txt",
        "unstructured",
        # Anthropic
        "anthropic",
        "anthropic._legacy_response",
        # Google
        "google.generativeai",
        "google.auth",
        # Standard-lib / tkinter
        "tkinter",
        "tkinter.ttk",
        "tkinter.filedialog",
        "tkinter.messagebox",
        # Misc langchain internals often missed
        "langchain.chains",
        "langchain.chains.retrieval_qa",
        "langchain.chains.combine_documents",
        "langchain_community.vectorstores.faiss",
        "langchain_community.document_loaders",
        "langchain_community.embeddings",
    ]
)

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "scipy", "numpy.testing", "IPython", "notebook"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="rpguide",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # GUI app — no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="rpguide",
)
