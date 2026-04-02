import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Global cache for collaborative components
_user_item_matrix_cache = None
_user_similarity_cache = None
_last_data_len = 0

def collaborative_recommend(data: pd.DataFrame, user_id: str, top_n: int = 10) -> pd.DataFrame:
    """
    Recommend products using User-Based Collaborative Filtering.
    """
    global _user_item_matrix_cache, _user_similarity_cache, _last_data_len
    
    # Convert user_id to proper type
    user_id = str(user_id)
    
    # Check if user exists in dataset
    if user_id not in data['user_id'].astype(str).unique():
        print(f"User ID {user_id} not found. Returning top rated products instead.")
        return rating_based_recommend(data, top_n)

    # Use cached components if data hasn't changed
    if _user_item_matrix_cache is None or len(data) != _last_data_len:
        print("Precomputing User-Item Matrix and User Similarity...")
        # Create User-Item Matrix (User ID × Product ID)
        _user_item_matrix_cache = data.pivot_table(
            index='user_id',
            columns='product_id',
            values='rating',
            aggfunc='mean'
        ).fillna(0)

        # Compute User Similarity Matrix using Cosine Similarity
        _user_similarity_cache = cosine_similarity(_user_item_matrix_cache)
        _last_data_len = len(data)
        print("Precomputation complete.")

    # Get index of target user
    try:
        target_user_index = _user_item_matrix_cache.index.get_loc(user_id)
    except KeyError:
        print(f"User {user_id} not found in user-item matrix.")
        return pd.DataFrame()

    # Get similarity scores for target user
    user_similarities = _user_similarity_cache[target_user_index]

    # Get indices of most similar users (excluding self)
    similar_users_indices = user_similarities.argsort()[::-1][1:top_n*2]

    # Collect recommended products
    recommended_product_ids = set()

    for sim_user_index in similar_users_indices:
        sim_user_id = _user_item_matrix_cache.index[sim_user_index]
        
        # Products rated highly by similar user
        sim_user_ratings = _user_item_matrix_cache.iloc[sim_user_index]
        target_user_ratings = _user_item_matrix_cache.iloc[target_user_index]

        # Products that similar user liked but target user hasn't rated yet
        candidate_products = sim_user_ratings[(sim_user_ratings > 3.5) & 
                                              (target_user_ratings == 0)]
        
        for prod_id in candidate_products.index:
            if len(recommended_product_ids) >= top_n * 2:
                break
            recommended_product_ids.add(prod_id)

        if len(recommended_product_ids) >= top_n * 2:
            break

    # If we don't have enough recommendations, fallback to popular items
    if len(recommended_product_ids) < 5:
        popular_items = data.groupby('product_id')['rating'].mean().nlargest(top_n*2).index
        recommended_product_ids.update(popular_items)

    # Get product details
    recommended_products = data[data['product_id'].isin(recommended_product_ids)].drop_duplicates('product_id')

    # Sort by rating (best first)
    recommended_products = recommended_products.nlargest(top_n, 'rating')

    # Select columns needed by frontend
    final_recommendations = recommended_products[[
        'product_id',
        'product_name',
        'price',
        'rating',
        'rating_count',
        'image_url',
        'tags',
        'category'
    ]].copy()

    print(f"Collaborative recommendations generated for user: {user_id}")
    return final_recommendations


# Fallback function (will be used by recommender.py)
def rating_based_recommend(data: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return top rated products - used for new users or fallback"""
    return data.nlargest(top_n, 'rating')[[
        'product_id', 'product_name', 'price', 'rating', 
        'rating_count', 'image_url', 'tags', 'category'
    ]]


# Test function
def test_collaborative():
    try:
        data = pd.read_csv("backend/data/clean_data.csv")
        print(f"Dataset loaded: {data.shape[0]} rows")
        
        # Test with a sample user
        sample_user = data['user_id'].astype(str).iloc[0]
        print(f"\nTesting collaborative filtering for user: {sample_user}")
        
        recommendations = collaborative_recommend(data, sample_user, top_n=8)
        
        print("\nRecommended Products:")
        print(recommendations[['product_name', 'price', 'rating']])
        
        return recommendations
        
    except FileNotFoundError:
        print("❌ clean_data.csv not found. Run cleaning_data.py first.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_collaborative()