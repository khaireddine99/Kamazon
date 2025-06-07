from .redis_client import r

def update_recommendations(item_ids):
    """
    For each item, increment co-purchase score with all other items in the cart.
    """
    print("adding items to the redis database -----------------------------------------------")
    for i in item_ids:
        for j in item_ids:
            if i != j:
                r.zincrby(f"recommend:item:{i}", 1, j)

def get_recommendations(item_id, top_n=5):
    """
    Get top-N item IDs that are most often bought with this item.
    """
    print("recommending items from the redis database ------------------------------------")
    return [int(i) for i in r.zrevrange(f"recommend:item:{item_id}", 0, top_n - 1)]