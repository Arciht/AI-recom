import reflex as rx
import pandas as pd
import os
from ..backend.recommender import get_df

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
                if isinstance(p, dict) and (
                   q in str(p.get("product_name", "")).lower() or
                   q in str(p.get("tags", "")).lower() or
                   q in str(p.get("category", "")).lower()
                )
            ]

    async def load_all_products(self):
        try:
            df = get_df()
            if df is None:
                self.all_products = []
                self.filtered_products = []
                return
            
            # Use a copy to avoid modifying the cached dataframe
            df_display = df.copy()
            
            # Clean up image URLs (some have multiple URLs separated by |)
            df_display["image_url"] = df_display["image_url"].apply(lambda x: str(x).split(" | ")[0] if pd.notnull(x) else "https://via.placeholder.com/400")
            
            self.all_products = df_display.head(100).to_dict(orient="records")
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
            df = get_df()
            if df is None:
                self.product = {}
                return
            
            result = df[df['product_id'].astype(str) == str(product_id)]
            if not result.empty:
                product = result.iloc[0].to_dict()
                # Clean up image URL
                if "image_url" in product:
                    product["image_url"] = str(product["image_url"]).split(" | ")[0]
                self.product = product
            else:
                self.product = {}
        except Exception as e:
            print(f"Error loading product detail: {e}")
            self.product = {}
