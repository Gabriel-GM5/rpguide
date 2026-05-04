import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from modules.configs import load_user_config, save_user_config, _resource_base

_PROVIDERS = ["gemini", "openai", "lmstudio", "ollama", "anthropic"]
_NEEDS_API_KEY = {"gemini", "openai", "anthropic"}
_NEEDS_BASE_URL = {"lmstudio", "ollama"}
_OPTIONAL_BASE_URL = {"openai"}
_NO_EMBEDDINGS = {"anthropic"}
_COMMON_DOC_TYPES = ["pdf", "txt", "md", "docx", "doc", "html", "csv", "rtf", "pptx"]


def _set_icon(window: tk.BaseWidget) -> None:
    icon_path = os.path.join(_resource_base(), "icon.ico")
    if os.path.exists(icon_path):
        try:
            window.iconbitmap(icon_path)
        except Exception:
            pass


class SetupApp:
    def __init__(self, root: tk.BaseWidget):
        self.root = root
        self.root.title("rpguide — Setup")
        self.root.geometry("540x620")
        self.root.resizable(False, False)
        _set_icon(self.root)
        self._existing = load_user_config()
        self._build_form()

    def _build_form(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="rpguide Configuration", font=("Arial", 13, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 16), sticky="w"
        )

        # Provider
        self._provider_var = tk.StringVar(value=self._existing.get("LLM_TYPE", "gemini"))
        self._add_label(frame, "LLM Provider *", 1)
        provider_cb = ttk.Combobox(frame, textvariable=self._provider_var, values=_PROVIDERS, state="readonly")
        provider_cb.grid(row=1, column=1, sticky="ew", pady=4)
        self._provider_var.trace_add("write", lambda *_: self._refresh())

        # API Key
        self._api_key_lbl = ttk.Label(frame, text="API Key *", anchor="e")
        self._api_key_var = tk.StringVar(value=self._existing.get("LLM_AI_API_KEY", ""))
        self._api_key_entry = ttk.Entry(frame, textvariable=self._api_key_var, show="*")

        # Base URL
        self._base_url_lbl = ttk.Label(frame, text="Base URL *", anchor="e")
        self._base_url_var = tk.StringVar(value=self._existing.get("LLM_AI_BASE_URL", ""))
        self._base_url_entry = ttk.Entry(frame, textvariable=self._base_url_var)

        # LLM Model
        self._model_var = tk.StringVar(value=self._existing.get("LLM_AI_MODEL", ""))
        self._add_label(frame, "LLM Model *", 4)
        ttk.Entry(frame, textvariable=self._model_var).grid(row=4, column=1, sticky="ew", pady=4)

        # Embeddings Model
        self._emb_lbl = ttk.Label(frame, text="Embeddings Model", anchor="e")
        self._emb_var = tk.StringVar(value=self._existing.get("EMBEDDINGS_AI_MODEL", ""))
        self._emb_entry = ttk.Entry(frame, textvariable=self._emb_var)

        # Temperature
        self._temp_var = tk.StringVar(value=self._existing.get("LLM_AI_TEMPERATURE", "0.0"))
        self._add_label(frame, "Temperature", 6)
        ttk.Entry(frame, textvariable=self._temp_var).grid(row=6, column=1, sticky="ew", pady=4)

        # Language
        self._lang_var = tk.StringVar(value=self._existing.get("LANGUAGE", "en_us"))
        self._add_label(frame, "Language", 7)
        ttk.Combobox(frame, textvariable=self._lang_var, values=["en_us", "pt_br"], state="readonly").grid(
            row=7, column=1, sticky="ew", pady=4
        )

        # AI Persona
        self._persona_var = tk.StringVar(value=self._existing.get("AI_PERSONA", ""))
        self._add_label(frame, "AI Persona", 8)
        ttk.Entry(frame, textvariable=self._persona_var).grid(row=8, column=1, sticky="ew", pady=4)

        # Knowledge Path
        self._knowledge_var = tk.StringVar(value=self._existing.get("LOCAL_KNOWLEDGE_PATH", ""))
        self._add_label(frame, "Knowledge Path", 9)
        path_frame = ttk.Frame(frame)
        path_frame.grid(row=9, column=1, sticky="ew", pady=4)
        path_frame.columnconfigure(0, weight=1)
        ttk.Entry(path_frame, textvariable=self._knowledge_var).grid(row=0, column=0, sticky="ew")
        ttk.Button(path_frame, text="Browse", command=self._browse, bootstyle="secondary", width=8).grid(
            row=0, column=1, padx=(4, 0)
        )

        # Doc Types — checkboxes for common types + free-text for others
        existing_types = {
            t.strip()
            for t in self._existing.get("LOCAL_KNOWLEDGE_DOC_TYPES", "").split(",")
            if t.strip()
        }
        self._doc_type_vars: dict[str, tk.BooleanVar] = {
            dt: tk.BooleanVar(value=dt in existing_types) for dt in _COMMON_DOC_TYPES
        }
        other_types = existing_types - set(_COMMON_DOC_TYPES)
        self._doc_types_other_var = tk.StringVar(value=",".join(sorted(other_types)))

        self._add_label(frame, "Doc Types", 10)
        dt_frame = ttk.Frame(frame)
        dt_frame.grid(row=10, column=1, sticky="ew", pady=(4, 0))
        for i, dt in enumerate(_COMMON_DOC_TYPES):
            ttk.Checkbutton(dt_frame, text=dt, variable=self._doc_type_vars[dt]).grid(
                row=i // 3, column=i % 3, sticky="w", padx=(0, 10), pady=1
            )
        other_row = ttk.Frame(dt_frame)
        other_row.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(4, 0))
        other_row.columnconfigure(1, weight=1)
        ttk.Label(other_row, text="Other:", font=("Arial", 9), foreground="gray").grid(row=0, column=0, sticky="w", padx=(0, 4))
        ttk.Entry(other_row, textvariable=self._doc_types_other_var, font=("Arial", 9)).grid(row=0, column=1, sticky="ew")

        # Debug
        raw_debug = self._existing.get("DEBUG", "false")
        self._debug_var = tk.BooleanVar(value=str(raw_debug).lower() in ("true", "1", "yes", "y"))
        self._add_label(frame, "Debug Mode", 11)
        ttk.Checkbutton(frame, variable=self._debug_var, bootstyle="round-toggle").grid(
            row=11, column=1, sticky="w", pady=4
        )

        # Save button
        ttk.Button(frame, text="Save & Start", command=self._save, bootstyle="success", width=20).grid(
            row=12, column=0, columnspan=2, pady=(20, 0)
        )

        self._frame = frame
        self._refresh()

    def _add_label(self, frame: ttk.Frame, text: str, row: int):
        ttk.Label(frame, text=text, anchor="e").grid(row=row, column=0, sticky="e", padx=(0, 10), pady=4)

    def _refresh(self):
        provider = self._provider_var.get()

        if provider in _NEEDS_API_KEY:
            self._api_key_lbl.config(text="API Key *")
            self._api_key_lbl.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=4)
            self._api_key_entry.grid(row=2, column=1, sticky="ew", pady=4)
        else:
            self._api_key_lbl.grid_remove()
            self._api_key_entry.grid_remove()

        if provider in _NEEDS_BASE_URL:
            self._base_url_lbl.config(text="Base URL *")
            self._base_url_lbl.grid(row=3, column=0, sticky="e", padx=(0, 10), pady=4)
            self._base_url_entry.grid(row=3, column=1, sticky="ew", pady=4)
        elif provider in _OPTIONAL_BASE_URL:
            self._base_url_lbl.config(text="Base URL")
            self._base_url_lbl.grid(row=3, column=0, sticky="e", padx=(0, 10), pady=4)
            self._base_url_entry.grid(row=3, column=1, sticky="ew", pady=4)
        else:
            self._base_url_lbl.grid_remove()
            self._base_url_entry.grid_remove()

        if provider not in _NO_EMBEDDINGS:
            self._emb_lbl.grid(row=5, column=0, sticky="e", padx=(0, 10), pady=4)
            self._emb_entry.grid(row=5, column=1, sticky="ew", pady=4)
        else:
            self._emb_lbl.grid_remove()
            self._emb_entry.grid_remove()

    def _browse(self):
        path = filedialog.askdirectory(title="Select knowledge base directory")
        if path:
            self._knowledge_var.set(path)

    def _collect_doc_types(self) -> str:
        checked = [dt for dt in _COMMON_DOC_TYPES if self._doc_type_vars[dt].get()]
        other = [t.strip() for t in self._doc_types_other_var.get().split(",") if t.strip()]
        return ",".join(checked + other)

    def _save(self):
        provider = self._provider_var.get()

        if provider in _NEEDS_API_KEY and not self._api_key_var.get().strip():
            messagebox.showerror("Validation", "API Key is required for this provider.")
            return
        if provider in _NEEDS_BASE_URL and not self._base_url_var.get().strip():
            messagebox.showerror("Validation", "Base URL is required for this provider.")
            return
        if not self._model_var.get().strip():
            messagebox.showerror("Validation", "LLM Model is required.")
            return
        try:
            float(self._temp_var.get())
        except ValueError:
            messagebox.showerror("Validation", "Temperature must be a number (e.g. 0.7).")
            return

        save_user_config({
            "LLM_TYPE": provider,
            "LLM_AI_API_KEY": self._api_key_var.get().strip(),
            "LLM_AI_BASE_URL": self._base_url_var.get().strip(),
            "LLM_AI_MODEL": self._model_var.get().strip(),
            "EMBEDDINGS_AI_MODEL": self._emb_var.get().strip(),
            "LLM_AI_TEMPERATURE": self._temp_var.get().strip(),
            "LANGUAGE": self._lang_var.get(),
            "AI_PERSONA": self._persona_var.get().strip(),
            "LOCAL_KNOWLEDGE_PATH": self._knowledge_var.get().strip(),
            "LOCAL_KNOWLEDGE_DOC_TYPES": self._collect_doc_types(),
            "DEBUG": "true" if self._debug_var.get() else "false",
        })
        self.root.destroy()


def run_setup() -> None:
    """Launch the setup wizard and block until it closes."""
    root = ttk.Window(themename="darkly")
    SetupApp(root)
    root.mainloop()


def run_setup_dialog(parent: tk.Widget) -> bool:
    """Open the setup wizard as a modal dialog attached to parent.

    Returns True if the configuration was saved (i.e. it changed).
    """
    before = load_user_config()

    dialog = tk.Toplevel(parent)
    dialog.transient(parent)
    dialog.grab_set()

    SetupApp(dialog)
    parent.wait_window(dialog)

    after = load_user_config()
    return before != after
