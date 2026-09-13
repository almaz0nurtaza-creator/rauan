"""
Заменяет все упоминания "Rauan" / "RAUAN" / "Rauan" на "Rauan" / "RAUAN"
во всех текстовых файлах проекта (код, README, LICENSE, .gitignore).

Использование:
    1. Положите этот файл в корень папки проекта (рядом с main.py)
    2. Запустите: python rename_to_rauan.py
"""

import os
import re

# Папки, которые не нужно трогать
SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules"}

# Расширения файлов, которые точно текстовые — остальные (иконки, картинки) не трогаем
TEXT_EXTENSIONS = {".py", ".md", ".txt", ".json", ".html", ".js", ".css", ".gitignore", ""}

# Паттерны для замены (порядок важен — сначала более длинные/специфичные)
REPLACEMENTS = [
    (re.compile(r"\bMARK LIII\b"), "RAUAN"),
    (re.compile(r"\bMark LIII\b"), "Rauan"),
    (re.compile(r"\bmark liii\b", re.IGNORECASE), "rauan"),
    (re.compile(r"\bMARK 53\b"), "RAUAN"),
    (re.compile(r"\bMark 53\b"), "Rauan"),
    (re.compile(r"\bMark-LIII\b"), "Rauan"),
]

changed_files = []

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for filename in files:
        path = os.path.join(root, filename)
        ext = os.path.splitext(filename)[1]
        if ext not in TEXT_EXTENSIONS and filename != ".gitignore":
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            continue

        original = content
        for pattern, replacement in REPLACEMENTS:
            content = pattern.sub(replacement, content)

        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            changed_files.append(path)

print(f"Изменено файлов: {len(changed_files)}")
for f in changed_files:
    print(" -", f)
