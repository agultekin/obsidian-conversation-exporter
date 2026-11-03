#!/usr/bin/env python3
import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path

# Chargement de la configuration
CONFIG_PATH = Path(__file__).parent.parent / "config" / "settings.json"

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "obsidian_vault_path": "~/Obsidian/Vault",
        "default_folder": "historic",
        "default_tags": ["ai/conversation", "historic"]
    }

def slugify(text: str) -> str:
    """Nettoie le titre pour générer un nom de fichier valide."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text)

def export_conversation(title: str, content: str, subfolder: str = None) -> str:
    config = load_config()
    
    # Construction du chemin cible
    base_vault = Path(os.path.expanduser(config.get("obsidian_vault_path")))
    target_folder = base_vault / config.get("default_folder", "historic")
    
    if subfolder:
        target_folder = target_folder / subfolder
        
    target_folder.mkdir(parents=True, exist_ok=True)
    
    # Nommage du fichier
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{slugify(title)}.md"
    file_path = target_folder / filename
    
    # Tags YAML
    tags = set(config.get("default_tags", ["ai/conversation", "historic"]))
    if subfolder:
        tags.add(slugify(subfolder))
        
    yaml_tags = "\n".join([f"  - {tag}" for tag in tags])
    
    md_content = f"""---
date: {date_str}
tags:
{yaml_tags}
title: "{title}"
---

# {title}

{content}
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    return str(file_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python export_to_obsidian.py '<title>' '<content>' [subfolder]")
        sys.exit(1)
        
    title_arg = sys.argv[1]
    content_arg = sys.argv[2]
    subfolder_arg = sys.argv[3] if len(sys.argv) > 3 else None
    
    saved_path = export_conversation(title_arg, content_arg, subfolder_arg)
    print(f"Conversation exported successfully to: {saved_path}")
