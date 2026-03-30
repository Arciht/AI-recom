import reflex as rx
from state.cart_state import CartState


class ProductDetailState(rx.State):
    """State for single product detail page"""
    product: dict = {}
    current_product_id: str = ""   # Changed name to avoid conflict with route param

    def load_product(self, product_id: str):
        self.current_product_id = product_id
        try:
            import pandas as pd
            df = pd.read_csv("backend/data/clean_data.csv")
            
            result = df[df['product_id'].astype(str) == str(product_id)]
            if not result.empty:
                self.product = result.iloc[0].to_dict()
            else:
                self.product = {}
        except Exception as e:
            print(f"Error loading product {product_id}: {e}")
            self.product = {}


@rx.page(route="/product/[product_id]", title="Product Detail")
def product_detail_page(product_id: str):
    # Load the product when the page loads
    ProductDetailState.load_product(product_id)

    return rx.center(
        rx.vstack(
            # Back button
            rx.button(
                "← Back to Products",
                on_click=rx.redirect("/products"),
                variant="ghost",
                align_self="flex-start",
                margin_bottom="1em",
            ),

            rx.cond(
                ProductDetailState.product,
                # Product details
                rx.hstack(
                    # Image
                    rx.image(
                        src=ProductDetailState.product.get("image_url", "/assets/placeholder.jpg"),
                        width="480px",
                        height="auto",
                        border_radius="15px",
                        object_fit="contain",
                    ),
                    # Details
                    rx.vstack(
                        rx.heading(
                            ProductDetailState.product.get("product_name", "Product"),
                            size="8",
                        ),
                        rx.text(
                            f"₹{float(ProductDetailState.product.get('price', 0)):.2f}",
                            font_size="3em",
                            font_weight="bold",
                            color="green.600",
                        ),
                        rx.text(
                            ProductDetailState.product.get("description", "No description available."),
                            font_size="lg",
                            color="gray.700",
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
                    width="100%",
                    max_width="1100px",
                ),
                # Not found
                rx.vstack(
                    rx.heading("Product Not Found", size="7", color="red.500"),
                    rx.button("Browse All Products", on_click=rx.redirect("/products"), size="lg"),
                )
            ),
            spacing="8",
            padding="2em",
            width="100%",
        )
    )