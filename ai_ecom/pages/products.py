import reflex as rx
from components.product_card import product_card
from state.user_state import UserState
from state.cart_state import CartState

# We'll create this state next if you don't have it yet
class ProductsState(rx.State):
    all_products: list[dict] = []
    search_query: str = ""
    filtered_products: list[dict] = []

    def load_products(self):
        """Load all products from the dataset"""
        try:
            import pandas as pd
            df = pd.read_csv("backend/data/clean_data.csv")
            
            # Convert DataFrame to list of dicts for Reflex
            self.all_products = df.to_dict(orient="records")
            self.filtered_products = self.all_products.copy()
        except Exception as e:
            print(f"Error loading products: {e}")
            self.all_products = []
            self.filtered_products = []

    def set_search_query(self, query: str):
        self.search_query = query
        if not query:
            self.filtered_products = self.all_products.copy()
        else:
            query = query.lower()
            self.filtered_products = [
                p for p in self.all_products
                if query in str(p.get("product_name", "")).lower() or
                   query in str(p.get("tags", "")).lower() or
                   query in str(p.get("category", "")).lower()
            ]

    def clear_search(self):
        self.search_query = ""
        self.filtered_products = self.all_products.copy()


@rx.page(route="/products", title="All Products")
def products_page():
    # Load products when page loads
    rx.call_script("window.onload = function() { ProductsState.load_products() }")  # Alternative: use on_load

    return rx.vstack(
        # Navbar will be added globally later
        rx.vstack(
            # Header
            rx.heading("All Products", size="9", text_align="center"),
            rx.text(
                "Browse our complete collection",
                font_size="lg",
                color="gray.600",
                text_align="center",
            ),
            
            # Search Bar
            rx.hstack(
                rx.input(
                    placeholder="Search products by name, category or tags...",
                    value=ProductsState.search_query,
                    on_change=ProductsState.set_search_query,
                    width="500px",
                    size="3",
                ),
                rx.button(
                    "Clear",
                    on_click=ProductsState.clear_search,
                    color_scheme="gray",
                    variant="outline",
                ),
                spacing="3",
            ),
            
            # Products Grid
            rx.grid(
                rx.foreach(
                    ProductsState.filtered_products,
                    product_card   # Reusing the product_card you already have
                ),
                columns=["1", "2", "3", "4"],   # Responsive: 1 on mobile → 4 on desktop
                spacing="6",
                width="100%",
                padding_y="2em",
            ),
            
            # Empty state
            rx.cond(
                len(ProductsState.filtered_products) == 0,
                rx.vstack(
                    rx.text("No products found matching your search.", font_size="lg"),
                    rx.button("Show All Products", on_click=ProductsState.clear_search),
                    spacing="4",
                    padding="4em",
                )
            ),
            
            width="100%",
            align="center",
            spacing="8",
            padding="2em",
        ),
        
        # Optional: Floating Cart Button
        rx.button(
            rx.hstack(
                rx.icon("shopping-cart"),
                rx.text(f"Cart ({len(CartState.cart_items)})"),
                spacing="2",
            ),
            on_click=rx.redirect("/cart"),
            position="fixed",
            bottom="20px",
            right="20px",
            size="4",
            color_scheme="blue",
            z_index="100",
        ) if UserState.logged_in else rx.fragment(),
        
        align="center",
        min_height="100vh",
        background_color="gray.50",
    )