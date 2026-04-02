import pandas as pd
from .Content_Based import content_based_recommend
from .collaborative import collaborative_recommend
from .ratingbased import rating_based_recommend

import os

# Global cache for the dataframe
_cached_df = None

def get_df():
    """Helper to get or load the dataframe"""
    global _cached_df
    if _cached_df is not None:
        return _cached_df
        
    try:
        # Get the path to clean_data.csv relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "clean_data.csv")
        
        df = pd.read_csv(data_path)
        
        # Normalize column names for internal logic
        df = df.rename(columns={
            "User's ID": "user_id",
            "ProdID": "product_id",
            "Name": "product_name",
            "ImageURL": "image_url",
            "Rating": "rating",
            "Review Count": "rating_count",
            "Category": "category",
            "Description": "description",
            "Tags": "tags"
        })
        
        # Add dummy price if missing
        if "price" not in df.columns:
            df["price"] = df["product_id"].apply(lambda x: round((hash(str(x)) % 10000) / 100 + 499, 2))
            
        print(f"Loaded dataset with {len(df)} products")
        _cached_df = df
        return df
    except FileNotFoundError:
        print(f"Error: clean_data.csv not found at {data_path}")
        return None

def get_recommendations(user_id=None, user_type: str = "new", top_n: int = 10):
    """
    Main recommendation orchestrator.
    Combines different recommendation strategies based on user type.
    
    Args:
        user_id: Numeric user ID from dataset (for existing users)
        user_type: "new" or "old"
        top_n: Number of recommendations to return
    """
    df = get_df()
    if df is None:
        return []

    # === New User → Rating Based (Popular Products) ===
    if user_type == "new" or user_id is None:
        print(f"New User detected -> Returning Top Rated Products")
        recommendations = rating_based_recommend(df, top_n)
        # Ensure columns exist even in output
        if not recommendations.empty:
            # Map columns if they were lost/renamed in the sub-functions
            # Most sub-functions return from the original 'df' or a slice
            pass 
        return recommendations.to_dict(orient="records")

    # === Existing User → Hybrid Approach ===
    print(f"Existing User (ID: {user_id}) -> Using Hybrid Recommendations")

    # 1. Collaborative Filtering (Similar Users)
    collab_recs = collaborative_recommend(df, user_id, top_n=top_n // 2 + 2)

    # 2. Content-Based Filtering (Based on one product user liked)
    content_recs = pd.DataFrame()
    user_products = df[df['user_id'].astype(str) == str(user_id)]['product_id'].unique()

    if len(user_products) > 0:
        # Use the first product the user has interacted with
        sample_product_name = df[df['product_id'] == user_products[0]]['product_name'].iloc[0]
        content_recs = content_based_recommend(df, sample_product_name, top_n=top_n // 2 + 2)
    else:
        # Fallback if no previous products found
        content_recs = rating_based_recommend(df, top_n=top_n // 2 + 2)

    # Combine both recommendations
    combined = pd.concat([collab_recs, content_recs], ignore_index=True)

    # Remove duplicates based on product_id
    combined = combined.drop_duplicates(subset=['product_id'])

    # Sort by rating (best first) and take top_n
    final_recommendations = combined.nlargest(top_n, 'rating')

    # Convert to list of dictionaries for Reflex State
    result = final_recommendations[[
        'product_id',
        'product_name',
        'price',
        'rating',
        'rating_count',
        'image_url',
        'tags',
        'category'
    ]].to_dict(orient="records")

    print(f"Final recommendations ready: {len(result)} products")
    return result


# Test function
def test_recommender():
    """Test the main recommender"""
    print("🧪 Testing Recommender System...\n")
    
    # Test for New User
    print("=== Testing New User ===")
    new_user_recs = get_recommendations(user_id=None, user_type="new", top_n=8)
    print(f"Returned {len(new_user_recs)} recommendations for new user\n")

    # Test for Existing User (using first user_id from dataset)
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "clean_data.csv")
        df = pd.read_csv(data_path)
        sample_user = str(df['user_id'].iloc[0])
        
        print(f"=== Testing Existing User (ID: {sample_user}) ===")
        old_user_recs = get_recommendations(user_id=sample_user, user_type="old", top_n=8)
        print(f"Returned {len(old_user_recs)} recommendations for existing user")
        
    except Exception as e:
        print(f"Could not test existing user: {e}")


if __name__ == "__main__":
    test_recommender()