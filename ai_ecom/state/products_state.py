import reflex as rx
from state.cart_state import CartState
from state.user_state import UserState
import pandas as pd

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

    def load_all_products(self):
        try:
            df = pd.read_csv("backend/data/clean_data.csv")
            self.all_products = df.to_dict(orient="records")
            self.filtered_products = self.all_products.copy()
        except Exception as e:
            print(f"Error loading products: {e}")
            self.all_products = []
            self.filtered_products = []


class ProductDetailState(rx.State):
    """State for product detail page"""
    product: dict = {}
    pid: str = ""          # Changed from 'product_id' to 'pid' to avoid conflict

    def load_product(self, product_id: str):
        """Load product details"""
        self.pid = product_id
        try:
            import pandas as pd
            df = pd.read_csv("backend/data/clean_data.csv")
            
            result = df[df['product_id'].astype(str) == str(product_id)]
            
            if not result.empty:
                self.product = result.iloc[0].to_dict()
            else:
                self.product = {}
        except Exception as e:
            print(f"Error loading product: {e}")
            self.product = {}


@rx.page(route="/product/[product_id]", title="Product Detail")
def product_detail_page(product_id: str):
    # Load product when page opens
    ProductDetailState.load_product(product_id)

    return rx.center(
        rx.vstack(
            rx.button(
                "← Back to Products",
                on_click=rx.redirect("/products"),
                variant="ghost",
                align_self="flex-start",
            ),

            rx.cond(
                ProductDetailState.product,
                # Product Found
                rx.hstack(
                    rx.image(
                        src=ProductDetailState.product.get("image_url", "/assets/placeholder.jpg"),
                        width="500px",
                        height="auto",
                        border_radius="15px",
                    ),
                    rx.vstack(
                        rx.heading(ProductDetailState.product.get("product_name", ""), size="8"),
                        rx.text(
                            f"₹{float(ProductDetailState.product.get('price', 0)):.2f}",
                            font_size="3em",
                            font_weight="bold",
                            color="green.600",
                        ),
                        rx.text(
                            ProductDetailState.product.get("description", "No description available."),
                            font_size="lg",
                        ),
                        rx.hstack(
                            rx.button(
                                "Add to Cart",
                                on_click=lambda: CartState.add_to_cart(ProductDetailState.product),
                                color_scheme="blue",
                                size="lg",
                            ),
                            rx.button(
                                "Buy Now",
                                on_click=rx.redirect("/checkout"),
                                color_scheme="green",
                                size="lg",
                            ),
                            spacing="4",
                        ),
                        spacing="6",
                        align="stretch",
                    ),
                    spacing="10",
                ),
                # Product Not Found
                rx.text("Product not found", size="7", color="red.500"),
            ),
            spacing="8",
            padding="2em",
        )
    )