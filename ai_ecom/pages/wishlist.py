import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..components.product_card import product_card, wishlist_item_card
from ..state.cart_state import WishlistState

from ..components.layout import layout

def wishlist_page() -> rx.Component:
    return layout(
        rx.vstack(
            rx.heading("My Wishlist", size="8", color="#111827", padding_y="8"),
            
            rx.cond(
                WishlistState.wishlist_items.length() == 0,
                # Empty State
                rx.center(
                    rx.vstack(
                        rx.box(
                            rx.icon("heart", size=100, color="gray.200"),
                            padding="10",
                        ),
                        rx.heading("Your wishlist is empty", size="6", color="gray.500"),
                        rx.text("Save items you love to find them easily later.", color="gray.400"),
                        rx.button(
                            "Start Shopping",
                            on_click=rx.redirect("/products"),
                            color_scheme="blue",
                            size="3",
                            margin_top="6",
                        ),
                        spacing="4",
                        align="center",
                        padding_y="20",
                    ),
                    width="100%",
                ),
                # Wishlist Grid
                rx.grid(
                    rx.foreach(
                        WishlistState.wishlist_items,
                        wishlist_item_card
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                    spacing="6",
                    width="100%",
                    padding_bottom="20",
                ),
            ),
            max_width="1280px",
            width="100%",
            padding_x="8",
        )
    )
