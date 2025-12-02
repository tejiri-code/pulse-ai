"""
Deduplication and novelty scoring using simple text similarity
"""
import os
import hashlib
from typing import List, Dict, Tuple


USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "True").lower() == "true"


def generate_embedding(text: str) -> List[float]:
    """
    Generate a simple hash-based embedding for a text
    (Simplified version without sentence-transformers)
    
    Args:
        text: Text to embed
        
    Returns:
        Hash-based embedding vector
    """
    # Use hash to create a simple numeric representation
    text_hash = hashlib.md5(text.encode()).hexdigest()
    # Convert to list of floats (simplified embedding)
    return [float(int(text_hash[i:i+2], 16)) / 255.0 for i in range(0, 32, 2)]


def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute simple similarity between two embeddings
    
    Args:
        embedding1: First embedding
        embedding2: Second embedding
        
    Returns:
        Similarity score (0-1)
    """
    if not embedding1 or not embedding2:
        return 0.0
    
    # Simple dot product similarity
    similarity = sum(a * b for a, b in zip(embedding1, embedding2)) / len(embedding1)
    return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]


def check_duplicate(new_item: Dict, existing_items: List[Dict], threshold: float = 0.85) -> Tuple[bool, float]:
    """
    Check if a news item is a duplicate of existing items
    
    Args:
        new_item: New news item with embedding
        existing_items: List of existing items with embeddings
        threshold: Similarity threshold for duplicate detection
        
    Returns:
        Tuple of (is_duplicate, max_similarity)
    """
    if not existing_items:
        return False, 0.0
    
    new_embedding = new_item.get("embedding", [])
    if not new_embedding:
        return False, 0.0
    
    max_similarity = 0.0
    
    for existing_item in existing_items:
        existing_embedding = existing_item.get("embedding", [])
        if not existing_embedding:
            continue
        
        similarity = compute_similarity(new_embedding, existing_embedding)
        max_similarity = max(max_similarity, similarity)
        
        if similarity >= threshold:
            return True, similarity
    
    return False, max_similarity


def compute_novelty_score(item: Dict, existing_items: List[Dict]) -> float:
    """
    Compute novelty score for a news item
    Higher score = more novel/unique content
    
    Args:
        item: News item with embedding
        existing_items: List of existing items with embeddings
        
    Returns:
        Novelty score (0-1, where 1 is most novel)
    """
    if not existing_items:
        return 1.0  # First item is always novel
    
    item_embedding = item.get("embedding", [])
    if not item_embedding:
        return 0.5  # Default middle score if no embedding
    
    similarities = []
    for existing_item in existing_items:
        existing_embedding = existing_item.get("embedding", [])
        if existing_embedding:
            similarity = compute_similarity(item_embedding, existing_embedding)
            similarities.append(similarity)
    
    if not similarities:
        return 1.0
    
    # Novelty is inverse of average similarity
    avg_similarity = sum(similarities) / len(similarities)
    novelty = 1.0 - avg_similarity
    
    return float(novelty)


def deduplicate_items(items: List[Dict], existing_items: List[Dict] = None) -> Tuple[List[Dict], List[Dict]]:
    """
    Deduplicate a list of news items
    
    Args:
        items: List of new items to process
        existing_items: List of existing items from database
        
    Returns:
        Tuple of (unique_items, duplicate_items)
    """
    if existing_items is None:
        existing_items = []
    
    unique_items = []
    duplicate_items = []
    
    # Add embeddings to new items
    for item in items:
        if "embedding" not in item or not item["embedding"]:
            combined_text = f"{item.get('title', '')} {item.get('content', '')}"
            item["embedding"] = generate_embedding(combined_text)
    
    # Check each item for duplicates
    all_processed = existing_items.copy()
    
    for item in items:
        is_dup, similarity = check_duplicate(item, all_processed)
        
        if is_dup:
            item["is_duplicate"] = True
            item["novelty_score"] = 1.0 - similarity
            duplicate_items.append(item)
        else:
            item["is_duplicate"] = False
            item["novelty_score"] = compute_novelty_score(item, all_processed)
            unique_items.append(item)
            all_processed.append(item)
    
    return unique_items, duplicate_items
