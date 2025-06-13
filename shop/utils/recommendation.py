from .redis_client import r

def update_recommendations(item_ids):
    """
    For each item, increment co-purchase score with all other items in the cart.
    """
    for i in item_ids:
        for j in item_ids:
            if i != j:
                r.zincrby(f"recommend:item:{i}", 1, j)

def get_recommendations(item_id, top_n=5):
    """
    Get top-N item IDs that are most often bought with this item.
    """
    return [int(i) for i in r.zrevrange(f"recommend:item:{item_id}", 0, top_n - 1)]


def get_combined_recommendations(item_ids, top_n=5):
    """
    Get top-N item IDs most often bought with any of the given item_ids.
    Uses Redis ZUNIONSTORE to sum co-purchase scores.
    """
    if not item_ids:
        return []

    # Temporary key for storing union result
    temp_key = "recommend:temp:union"

    # Source keys: co-purchase sets for each item
    source_keys = [f"recommend:item:{item_id}" for item_id in item_ids]

    # Perform weighted union (default weight = 1 for each)
    r.zunionstore(temp_key, source_keys)

    # Get top N recommendations, excluding the original items
    recommendations = r.zrevrange(temp_key, 0, top_n + len(item_ids) - 1, withscores=False)
    
    # Filter out original items
    filtered = [int(item) for item in recommendations if int(item) not in item_ids]

    # Return top N after filtering
    return filtered[:top_n]
