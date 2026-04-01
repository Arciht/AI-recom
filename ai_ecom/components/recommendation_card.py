import reflex as rx
from typing import Dict, Any

from state.cart_state import CartState


def recommendation_card(product: Dict[str, Any]) -> rx.Component:
    """
    Specialized card for Personalized Recommendations
    Shows recommendation reason + better visual appeal
    """
    return rx.card(
        rx.vstack(
            # Product Image with overlay badge
            rx.box(
                rx.image(
                    src=product.get("image_url", "/assets/placeholder.jpg"),
                    alt=product.get("product_name", ""),
                    width="100%",
                    height="240px",
                    object_fit="cover",
                ),
                # "Recommended" badge
                rx.badge(
                    "AI Recommended",
                    color_scheme="green",
                    position="absolute",
                    top="12px",
                    right="12px",
                    variant="solid",
                ),
                position="relative",
            ),

            # Content
            rx.vstack(
                rx.heading(
                    product.get("product_name", "Recommended Product"),
                    size="5",
                    text_align="center",
                    no_of_lines=2,
                ),

                # Price
                rx.text(
                    f"₹{float(product.get('price', 0)):.2f}",
                    font_size="2em",
                    font_weight="bold",
                    color="green.700",
                ),

                # Recommendation Reason (Dynamic)
                rx.cond(
                    product.get("reason"),
                    rx.text(
                        product.get("reason", ""),
                        font_size="0.85em",
                        color="blue.600",
                        font_style="italic",
                        text_align="center",
                    ),
                    # Default reasons based on user type
                    rx.cond(
                        UserState.user_type == "new",
                        rx.text("Popular choice with high ratings", 
                               font_size="0.85em", color="gray.500", text_align="center"),
                        rx.text("Based on your browsing & similar users", 
                               font_size="0.85em", color="gray.500", text_align="center"),
                    )
                ),

                # Rating
                rx.hstack(
                    rx.icon("star", color="amber.400", size=18),
                    rx.text(
                        f"{product.get('rating', 4.5)} ({product.get('rating_count', 89)})",
                        color="gray.600",
                    ),
                    spacing="1",
                ),

                # Action Buttons
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("shopping-cart"),
                            rx.text("Add to Cart"),
                            spacing="2",
                        ),
                        on_click=lambda: CartState.add_to_cart(product),
                        color_scheme="blue",
                        flex="1",
                        size="2",
                    ),
                    rx.button(
                        "View Details",
                        on_click=rx.redirect(f"/product/{product.get('product_id')}"),
                        color_scheme="gray",
                        variant="outline",
                        flex="1",
                        size="2",
                    ),
                    spacing="3",
                    width="100%",
                ),

                spacing="4",
                padding_x="1.2em",
                padding_y="1em",
                width="100%",
                align="center",
            ),
            spacing="0",
            width="100%",
        ),
        width="100%",
        max_width="320px",
        box_shadow="lg",
        border_radius="15px",
        overflow="hidden",
        transition="transform 0.3s ease, box-shadow 0.3s ease",
        _hover={
            "transform": "scale(1.03)",
            "box_shadow": "2xl",
        },
    )


# Import UserState at bottom to avoid circular import
from state.user_state import UserState