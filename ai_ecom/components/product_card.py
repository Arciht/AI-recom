import reflex as rx
from typing import Dict, Any

# Import CartState so we can add items to cart
from state.cart_state import CartState


def product_card(product: Dict[str, Any]) -> rx.Component:
    """
    Reusable Product Card Component
    Works for both Recommendations and All Products page
    """
    return rx.card(
        rx.vstack(
            # Product Image
            rx.image(
                src=product.get("image_url", "/assets/placeholder.jpg"),
                alt=product.get("product_name", "Product"),
                width="100%",
                height="220px",
                object_fit="cover",
                border_radius="8px 8px 0 0",
            ),
            
            # Product Details
            rx.vstack(
                rx.heading(
                    product.get("product_name", "Unknown Product"),
                    size="5",
                    text_align="center",
                    no_of_lines=2,
                ),
                
                # Price
                rx.text(
                    f"₹{float(product.get('price', 0)):.2f}",
                    font_size="1.8em",
                    font_weight="bold",
                    color="green.600",
                ),
                
                # Rating (if available in dataset)
                rx.hstack(
                    rx.icon("star", color="gold"),
                    rx.text(
                        f"{product.get('rating', 4.5)} • "
                        f"{product.get('rating_count', 120)} ratings",
                        font_size="0.9em",
                        color="gray.500",
                    ),
                    spacing="1",
                ),
                
                # Short Description / Tags (optional)
                rx.text(
                    product.get("tags", "")[:80] + "..." 
                    if len(product.get("tags", "")) > 80 else product.get("tags", ""),
                    font_size="0.85em",
                    color="gray.600",
                    text_align="center",
                    no_of_lines=2,
                ),
                
                # Action Buttons
                rx.hstack(
                    rx.button(
                        "Add to Cart",
                        on_click=lambda: CartState.add_to_cart(product),
                        color_scheme="blue",
                        variant="solid",
                        size="2",
                        flex="1",
                    ),
                    rx.button(
                        "View Details",
                        on_click=rx.redirect(f"/product/{product.get('product_id')}"),
                        color_scheme="gray",
                        variant="outline",
                        size="2",
                        flex="1",
                    ),
                    spacing="2",
                    width="100%",
                ),
                
                spacing="3",
                padding="1em",
                align="center",
                width="100%",
            ),
            spacing="0",
            width="100%",
            max_width="280px",
        ),
        box_shadow="md",
        border_radius="12px",
        overflow="hidden",
        transition="all 0.2s",
        _hover={
            "box_shadow": "xl",
            "transform": "translateY(-4px)",
        },
    )