import reflex as rx
import pandas as pd
import os

class ProductsState(rx.State):
    search_query: str = ""
    all_products: list[dict] = []
    filtered_products: list[dict] = []

    def set_search_query(self, query: str):
        self.search_query = query
        if not query.strip():
            self.filtered_products = self.all_products.copy()
        else:
            q = query.lower().strip()
            self.filtered_products = [
                p for p in self.all_products
                if q in str(p.get("product_name", "")).lower() or
                   q in str(p.get("tags", "")).lower() or
                   q in str(p.get("category", "")).lower()
            ]

    async def load_all_products(self):
        try:
            # This is a placeholder for a real API call
            # In a real app, you would fetch this from your backend
            # For example: response = await rx.call_api("/api/products")
            
            # Get path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, "..", "backend", "clean_data.csv")
            
            df = pd.read_csv(data_path)
            
            # Map columns to match our UI expectations
            df = df.rename(columns={
                "ProdID": "product_id",
                "Name": "product_name",
                "ImageURL": "image_url",
                "Rating": "rating",
                "Review Count": "rating_count",
                "Category": "category",
                "Description": "description",
                "Tags": "tags"
            })
            
            # Clean up image URLs (some have multiple URLs separated by |)
            df["image_url"] = df["image_url"].apply(lambda x: str(x).split(" | ")[0] if pd.notnull(x) else "https://via.placeholder.com/400")
            
            # Add dummy prices if missing
            if "price" not in df.columns:
                df["price"] = df["product_id"].apply(lambda x: round((hash(str(x)) % 10000) / 100 + 499, 2))
                
            self.all_products = df.head(100).to_dict(orient="records")
            self.filtered_products = self.all_products.copy()
        except Exception as e:
            print(f"Error loading products: {e}")
            self.all_products = []
            self.filtered_products = []


class ProductDetailState(rx.State):
    """State for product detail page"""
    product: dict = {}

    async def load_product(self):
        """Load product details"""
        # Get product_id from the route parameters
        product_id = self.router.page.params.get("product_id", "")
        try:
            # Get path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, "..", "backend", "clean_data.csv")
            
            df = pd.read_csv(data_path)
            
            # Map columns
            df = df.rename(columns={
                "ProdID": "product_id",
                "Name": "product_name",
                "ImageURL": "image_url",
                "Rating": "rating",
                "Review Count": "rating_count",
                "Category": "category",
                "Description": "description",
                "Tags": "tags"
            })
            
            result = df[df['product_id'].astype(str) == str(product_id)]
            if not result.empty:
                product = result.iloc[0].to_dict()
                # Clean up image URL
                if "image_url" in product:
                    product["image_url"] = str(product["image_url"]).split(" | ")[0]
                # Add dummy price
                product["price"] = round((hash(str(product["product_id"])) % 10000) / 100 + 499, 2)
                self.product = product
            else:
                self.product = {}
        except Exception as e:
            print(f"Error loading product: {e}")
            self.product = {}
