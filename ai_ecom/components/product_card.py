import reflex as rx
from ..state.cart_state import CartState, WishlistState

def product_card(product: dict):
    return rx.card(
        rx.vstack(
            # Product Image
            rx.box(
                rx.image(
                    src=product["image_url"],
                    width="100%",
                    height="200px",
                    object_fit="cover",
                    border_radius="lg",
                ),
                rx.icon(
                    "heart",
                    size=20,
                    position="absolute",
                    top="3",
                    right="3",
                    cursor="pointer",
                    color=rx.cond(
                        WishlistState.wishlist_items.contains(product),
                        "red",
                        "gray"
                    ),
                    on_click=lambda: WishlistState.toggle_wishlist(product),
                ),
                position="relative",
                width="100%",
            ),
            
            # Product Details
            rx.vstack(
                rx.heading(
                    product["product_name"],
                    size="5",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                    overflow="hidden",
                    width="100%",
                    color="#1e293b", # Slate-800
                ),
                rx.hstack(
                    rx.text(f"₹{product['price']}", font_weight="bold", color="#2563eb", size="4"),
                    rx.spacer(),
                    rx.hstack(
                        rx.icon("star", size=14, color="#f59e0b"), # Amber-500
                        rx.text(product["rating"].to_string(), size="2", color="#64748b"), # Slate-500
                        spacing="1",
                        align="center",
                    ),
                    width="100%",
                ),
                
                # Buttons
                rx.hstack(
                    rx.button(
                        "Add to Cart",
                        on_click=CartState.add_to_cart(product),
                        variant="soft",
                        color_scheme="blue",
                        size="2",
                        flex="1",
                    ),
                    rx.button(
                        "Details",
                        on_click=rx.redirect(f"/product/{product['product_id']}"),
                        variant="outline",
                        size="2",
                        flex="1",
                        color="#3b82f6",
                    ),
                    width="100%",
                    spacing="2",
                ),
                spacing="3",
                width="100%",
                padding_y="2",
            ),
            spacing="3",
        ),
        _hover={
            "transform": "translateY(-4px)",
            "box_shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
        },
        transition="all 0.2s",
        width="100%",
        border_radius="xl",
        padding="3",
    )

def recommendation_card(product: dict):
    return rx.box(
        rx.card(
            rx.vstack(
                # Badge
                rx.badge(
                    "Recommended for you",
                    variant="solid",
                    color_scheme="blue",
                    position="absolute",
                    top="3",
                    left="3",
                    z_index="10",
                    size="1",
                    border_radius="full",
                ),
                
                # Product Image
                rx.image(
                    src=product["image_url"],
                    width="100%",
                    height="200px",
                    object_fit="cover",
                    border_radius="lg",
                ),
                
                # Product Details
                rx.vstack(
                    rx.heading(
                        product["product_name"],
                        size="5",
                        text_overflow="ellipsis",
                        white_space="nowrap",
                        overflow="hidden",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text(f"₹{product['price']}", font_weight="bold", color="#3b82f6", size="4"),
                        rx.spacer(),
                        rx.hstack(
                            rx.icon("star", size=14, color="amber"),
                            rx.text(product["rating"].to_string(), size="2", color="gray.600"),
                            spacing="1",
                            align="center",
                        ),
                        width="100%",
                    ),
                    
                    # Buttons
                    rx.hstack(
                        rx.button(
                            "Add to Cart",
                            on_click=CartState.add_to_cart(product),
                            variant="soft",
                            color_scheme="blue",
                            size="2",
                            flex="1",
                        ),
                        rx.button(
                            "Details",
                            on_click=rx.redirect(f"/product/{product['product_id']}"),
                            variant="outline",
                            size="2",
                            flex="1",
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    spacing="3",
                    width="100%",
                    padding_y="2",
                ),
                spacing="3",
                position="relative",
            ),
            _hover={
                "transform": "translateY(-4px)",
                "box_shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
            },
            transition="all 0.2s",
            width="100%",
            border_radius="xl",
            padding="3",
        ),
        width="100%",
    )

def wishlist_item_card(product: dict):
    return rx.card(
        rx.vstack(
            # Product Image
            rx.box(
                rx.image(
                    src=product["image_url"],
                    width="100%",
                    height="200px",
                    object_fit="cover",
                    border_radius="lg",
                ),
                position="relative",
                width="100%",
            ),
            
            # Product Details
            rx.vstack(
                rx.heading(
                    product["product_name"],
                    size="5",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                    overflow="hidden",
                    width="100%",
                ),
                rx.hstack(
                    rx.text(f"₹{product['price']}", font_weight="bold", color="#3b82f6", size="4"),
                    rx.spacer(),
                    rx.hstack(
                        rx.icon("star", size=14, color="amber"),
                        rx.text(product["rating"].to_string(), size="2", color="gray.600"),
                        spacing="1",
                        align="center",
                    ),
                    width="100%",
                ),
                
                # Buttons
                rx.vstack(
                    rx.button(
                        "Add to Cart",
                        on_click=CartState.add_to_cart(product),
                        variant="soft",
                        color_scheme="blue",
                        size="2",
                        width="100%",
                    ),
                    rx.button(
                        "Remove from Wishlist",
                        on_click=lambda: WishlistState.remove_from_wishlist(product["product_id"]),
                        variant="ghost",
                        color_scheme="red",
                        size="2",
                        width="100%",
                    ),
                    width="100%",
                    spacing="2",
                ),
                spacing="3",
                width="100%",
                padding_y="2",
            ),
            spacing="3",
        ),
        _hover={
            "transform": "translateY(-4px)",
            "box_shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
        },
        transition="all 0.2s",
        width="100%",
        border_radius="xl",
        padding="3",
    )
