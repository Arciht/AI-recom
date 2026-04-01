import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..components.product_card import recommendation_card
from ..state.products_state import ProductDetailState, ProductsState
from ..state.cart_state import CartState

from ..components.layout import layout

def product_detail_page() -> rx.Component:
    product = ProductDetailState.product
    
    return layout(
        rx.vstack(
            # Breadcrumbs
            rx.hstack(
                rx.link("Home", href="/", color="gray.500", size="2"),
                rx.icon("chevron_right", size=14, color="gray.400"),
                rx.link("Products", href="/products", color="gray.500", size="2"),
                rx.icon("chevron_right", size=14, color="gray.400"),
                rx.text(product["product_name"], color="gray.900", size="2", font_weight="medium"),
                spacing="2",
                align="center",
                width="100%",
                padding_y="6",
            ),
            
            # Product Info Section
            rx.hstack(
                # Left: Image
                rx.box(
                    rx.image(
                        src=product["image_url"],
                        width="100%",
                        height="auto",
                        border_radius="2xl",
                        box_shadow="lg",
                    ),
                    width="50%",
                ),
                
                # Right: Details
                rx.vstack(
                    rx.badge(product["category"], color_scheme="blue", variant="soft", size="2"),
                    rx.heading(product["product_name"], size="9", color="#111827"),
                    
                    rx.hstack(
                        rx.hstack(
                            rx.icon("star", size=18, color="amber"),
                            rx.text(product["rating"].to_string(), font_weight="bold", size="4"),
                            spacing="1",
                            align="center",
                        ),
                        rx.text(f"({product['rating_count'].to_string()} reviews)", color="gray.500", size="3"),
                        spacing="4",
                        align="center",
                    ),
                    
                    rx.text(
                        f"₹{product['price']}",
                        size="8",
                        font_weight="bold",
                        color="#3b82f6",
                        padding_y="4",
                    ),
                    
                    rx.text(
                        product["description"],
                        color="gray.600",
                        size="3",
                        line_height="1.6",
                    ),
                    
                    rx.divider(padding_y="4"),
                    
                    # Actions
                    rx.hstack(
                        rx.button(
                            "Add to Cart",
                            on_click=CartState.add_to_cart(product),
                            size="4",
                            color_scheme="blue",
                            flex="1",
                        ),
                        rx.button(
                            "Buy Now",
                            on_click=rx.redirect("/checkout"),
                            size="4",
                            variant="outline",
                            color_scheme="blue",
                            flex="1",
                        ),
                        width="100%",
                        spacing="4",
                        padding_top="6",
                    ),
                    
                    # Features
                    rx.grid(
                        rx.hstack(rx.icon("truck", size=18), rx.text("Free Delivery", size="2"), spacing="2"),
                        rx.hstack(rx.icon("rotate_ccw", size=18), rx.text("30 Days Return", size="2"), spacing="2"),
                        rx.hstack(rx.icon("shield_check", size=18), rx.text("Secure Payment", size="2"), spacing="2"),
                        rx.hstack(rx.icon("tag", size=18), rx.text("Best Price", size="2"), spacing="2"),
                        columns="2",
                        spacing="4",
                        width="100%",
                        padding_top="8",
                    ),
                    
                    align="start",
                    spacing="4",
                    width="50%",
                    padding_left="12",
                ),
                width="100%",
                align="start",
                padding_y="8",
            ),
            
            # Similar Products Section
            rx.vstack(
                rx.heading("You may also like", size="7", color="#111827", margin_top="20", margin_bottom="8"),
                rx.grid(
                    rx.foreach(
                        ProductsState.all_products[:4], # Dummy similar products
                        recommendation_card
                    ),
                    columns="4",
                    spacing="6",
                    width="100%",
                ),
                width="100%",
                padding_bottom="20",
            ),
            
            max_width="1280px",
            width="100%",
            padding_x="8",
        )
    )
