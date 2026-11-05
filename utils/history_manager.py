"""
EvidenceBot - Search History Manager
====================================
Provides persistent storage and retrieval of user search queries.
Preserves history across browser refreshes and session restarts using JSON storage.
Prevents duplicate entries and ensures the most recent queries appear first.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Resolve the data directory relative to project root
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
HISTORY_FILE = DATA_DIR / "search_history.json"


def _ensure_data_dir() -> None:
    """Ensures that the data storage directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_search_history() -> List[Dict[str, Any]]:
    """
    Loads persistent search history from disk.
    
    Returns:
        List[Dict[str, Any]]: List of search history items, latest first.
        Each item is a dictionary: {"query": str, "timestamp": str, "year_range": Optional[str]}
    """
    _ensure_data_dir()
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                # Ensure each element has at least a 'query' key
                valid_items = []
                for item in data:
                    if isinstance(item, str) and item.strip():
                        valid_items.append({
                            "query": item.strip(),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "year_range": None
                        })
                    elif isinstance(item, dict) and item.get("query", "").strip():
                        valid_items.append(item)
                return valid_items
            return []
    except Exception:
        # Fallback to empty list if file is corrupt
        return []


def save_search_history(history: List[Dict[str, Any]]) -> None:
    """Writes the search history list to disk."""
    _ensure_data_dir()
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def add_to_history(query: str, year_range: Optional[str] = None, max_items: int = 20) -> List[Dict[str, Any]]:
    """
    Appends a new query to the search history, moving it to the top if it already existed.
    Prevents duplicate queries.
    
    Parameters:
        query: Search query text.
        year_range: Optional publication year range string (e.g. "2015-2026").
        max_items: Maximum number of history items to retain.
        
    Returns:
        List[Dict[str, Any]]: The updated history list.
    """
    clean_q = query.strip()
    if not clean_q:
        return load_search_history()

    history = load_search_history()

    # Remove existing duplicate(s) case-insensitively
    new_history = [
        item for item in history
        if item.get("query", "").strip().lower() != clean_q.lower()
    ]

    # Prepend the new query so latest searches always appear first
    new_entry = {
        "query": clean_q,
        "timestamp": datetime.now().strftime("%b %d, %H:%M"),
        "year_range": year_range
    }
    new_history.insert(0, new_entry)

    # Trim to max_items
    new_history = new_history[:max_items]

    # Save to disk
    save_search_history(new_history)
    return new_history


def clear_search_history() -> None:
    """Clears all stored search history."""
    save_search_history([])


# Convenient alias
clear_history = clear_search_history

