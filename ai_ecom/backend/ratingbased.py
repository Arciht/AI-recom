import pandas as pd

def rating_based_recommend(data: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Recommend top-rated products (Best for New Users).
    This is a simple but effective popularity-based recommendation.
    """
    
    # Group by product and calculate average rating and count
    avg_ratings = data.groupby('product_id').agg({
        'product_name': 'first',
        'price': 'first',
        'rating': 'mean',
        'rating_count': 'sum',           # Total reviews
        'image_url': 'first',
        'tags': 'first',
        'category': 'first'
    }).reset_index()

    # Rename for clarity
    avg_ratings = avg_ratings.rename(columns={'rating': 'avg_rating'})

    # Sort by average rating (descending) and then by number of ratings (for stability)
    top_rated = avg_ratings.sort_values(
        by=['avg_rating', 'rating_count'], 
        ascending=[False, False]
    )

    # Take top N products
    recommendations = top_rated.head(top_n)

    # Select only the columns needed by frontend
    final_recommendations = recommendations[[
        'product_id',
        'product_name',
        'price',
        'avg_rating',
        'rating_count',
        'image_url',
        'tags',
        'category'
    ]].copy()

    # Rename back to rating for frontend consistency
    final_recommendations = final_recommendations.rename(columns={'avg_rating': 'rating'})

    # Round rating to 1 decimal place
    final_recommendations['rating'] = final_recommendations['rating'].round(1)

    print(f"Rating-based recommendations generated: Top {len(final_recommendations)} products")

    return final_recommendations


# Simple test function
def test_rating_based():
    """Test the rating-based recommendation"""
    try:
        data = pd.read_csv("backend/data/clean_data.csv")
        print(f"Dataset loaded: {data.shape[0]} products")
        
        print("\nGenerating Top Rated Products...")
        recommendations = rating_based_recommend(data, top_n=10)
        
        print("\nTop 10 Trending / Highly Rated Products:")
        print(recommendations[['product_name', 'price', 'rating', 'rating_count']])
        
        return recommendations
        
    except FileNotFoundError:
        print("❌ Error: clean_data.csv not found. Please run cleaning_data.py first.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_rating_based()