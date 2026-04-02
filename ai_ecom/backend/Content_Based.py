import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Global cache for content-based components
_tfidf_matrix_cache = None
_cosine_sim_cache = None
_last_data_len = 0

def content_based_recommend(data: pd.DataFrame, item_name: str, top_n: int = 10) -> pd.DataFrame:
    """
    Recommend similar products based on Tags using TF-IDF + Cosine Similarity.
    """
    global _tfidf_matrix_cache, _cosine_sim_cache, _last_data_len
    
    # Check if item exists
    if item_name not in data['product_name'].values:
        print(f"Product '{item_name}' not found in the dataset.")
        # Return top popular products as fallback
        cols = ['product_id', 'product_name', 'price', 'rating', 'rating_count', 'image_url', 'tags', 'category']
        return data.nlargest(top_n, 'rating')[cols]

    # Use cached components if data hasn't changed
    if _tfidf_matrix_cache is None or len(data) != _last_data_len:
        print("Precomputing TF-IDF matrix and Cosine Similarity...")
        tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)
        )
        
        try:
            _tfidf_matrix_cache = tfidf_vectorizer.fit_transform(data['tags'].fillna(''))
            _cosine_sim_cache = cosine_similarity(_tfidf_matrix_cache, _tfidf_matrix_cache)
            _last_data_len = len(data)
            print("Precomputation complete.")
        except Exception as e:
            print(f"Error in precomputation: {e}")
            return data.nlargest(top_n, 'rating')

    try:
        # Get index of the input item
        item_index = data[data['product_name'] == item_name].index[0]
        
        # Get similarity scores for all items
        similarity_scores = list(enumerate(_cosine_sim_cache[item_index]))
        
        # Sort by similarity score (descending)
        similar_items = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N similar items (excluding the item itself)
        top_similar = similar_items[1:top_n + 1]
        
        # Get recommended indices
        recommended_indices = [idx for idx, score in top_similar]
        
        # Return recommended products with important columns for frontend
        recommended_products = data.iloc[recommended_indices][[
            'product_id',
            'product_name',
            'price',
            'rating',
            'rating_count',
            'image_url',
            'tags',
            'category'
        ]].copy()
        
        # Add similarity score for debugging (optional)
        recommended_products['similarity_score'] = [score for idx, score in top_similar]
        
        print(f"Content-based recommendations generated for: {item_name}")
        return recommended_products
        
    except Exception as e:
        print(f"Error in content-based recommendation: {e}")
        # Fallback: Return top rated products
        return data.nlargest(top_n, 'rating')[[
            'product_id', 'product_name', 'price', 'rating', 'rating_count', 'image_url'
        ]]


# Optional: Simple test function
def test_content_recommendation():
    """Test the content filtering"""
    try:
        data = pd.read_csv("backend/data/clean_data.csv")
        print(f"Dataset loaded: {data.shape[0]} products")
        
        # Test with first product
        sample_item = data['product_name'].iloc[0]
        print(f"\nTesting with item: {sample_item}")
        
        recommendations = content_based_recommend(data, sample_item, top_n=8)
        
        print("\nTop Recommendations:")
        print(recommendations[['product_name', 'price', 'rating']])
        
        return recommendations
        
    except FileNotFoundError:
        print("❌ clean_data.csv not found. Please run cleaning_data.py first.")
    except Exception as e:
        print(f"❌ Test failed: {e}")


# Run test if file is executed directly
if __name__ == "__main__":
    test_content_recommendation()