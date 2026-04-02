import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..state.cart_state import CartState

from ..components.layout import layout

def cart_page() -> rx.Component:
    return layout(
        rx.vstack(
            rx.heading("Shopping Cart", size="8", color="#111827", padding_y="8"),
            
            rx.cond(
                CartState.cart_items.length() == 0,
                # Empty State
                rx.center(
                    rx.vstack(
                        rx.box(
                            rx.icon("shopping_bag", size=100, color="gray.200"),
                            padding="10",
                        ),
                        rx.heading("Your cart is empty", size="6", color="gray.500"),
                        rx.text("Looks like you haven't added anything to your cart yet.", color="gray.400"),
                        rx.button(
                            "Continue Shopping",
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
                # Cart Items
                rx.hstack(
                    # Left: Items List
                    rx.vstack(
                        rx.foreach(
                            CartState.cart_items,
                            lambda item: rx.card(
                                rx.hstack(
                                    rx.image(
                                        src=rx.cond(item["image_url"], item["image_url"], "https://via.placeholder.com/150"),
                                        width="100px", 
                                        height="100px", 
                                        object_fit="cover", 
                                        border_radius="lg"
                                    ),
                                    rx.vstack(
                                        rx.heading(rx.cond(item["product_name"], item["product_name"], "Product"), size="4", color="#111827"),
                                        rx.text(rx.cond(item["category"], item["category"], "Category"), color="gray.500", size="2"),
                                        rx.button(
                                            "Remove",
                                            on_click=lambda: CartState.remove_from_cart(item["product_id"]),
                                            variant="ghost",
                                            color_scheme="red",
                                            size="2",
                                            padding="0",
                                        ),
                                        align="start",
                                        spacing="1",
                                    ),
                                    rx.spacer(),
                                    rx.vstack(
                                        rx.text(
                                            rx.cond(item["price"], "₹" + item["price"].to_string(), "₹0.00"), 
                                            font_weight="bold", 
                                            size="4"
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                rx.icon("minus", size=14),
                                                on_click=lambda: CartState.update_quantity(item["product_id"], -1),
                                                size="1",
                                                variant="soft",
                                            ),
                                            rx.text(
                                                rx.cond(item["quantity"], item["quantity"].to_string(), "1"), 
                                                font_weight="medium", 
                                                padding_x="2"
                                            ),
                                            rx.button(
                                                rx.icon("plus", size=14),
                                                on_click=lambda: CartState.update_quantity(item["product_id"], 1),
                                                size="1",
                                                variant="soft",
                                            ),
                                            spacing="1",
                                            align="center",
                                        ),
                                        align="end",
                                    ),
                                    width="100%",
                                    align="center",
                                    padding="2",
                                ),
                                width="100%",
                                margin_bottom="4",
                            )
                        ),
                        width="70%",
                    ),
                    
                    # Right: Summary
                    rx.vstack(
                        rx.card(
                            rx.vstack(
                                rx.heading("Order Summary", size="5", color="#111827", margin_bottom="4"),
                                rx.hstack(
                                    rx.text("Subtotal", color="gray.600"),
                                    rx.spacer(),
                                    rx.text(f"₹{CartState.total}", font_weight="medium"),
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.text("Shipping", color="gray.600"),
                                    rx.spacer(),
                                    rx.text("Free", color="green.600", font_weight="medium"),
                                    width="100%",
                                ),
                                rx.divider(margin_y="4"),
                                rx.hstack(
                                    rx.text("Total", font_weight="bold", size="5"),
                                    rx.spacer(),
                                    rx.text(f"₹{CartState.total}", font_weight="bold", size="5", color="#3b82f6"),
                                    width="100%",
                                ),
                                rx.button(
                                    "Proceed to Checkout",
                                    on_click=rx.redirect("/checkout"),
                                    color_scheme="blue",
                                    width="100%",
                                    size="4",
                                    margin_top="6",
                                ),
                                spacing="3",
                                width="100%",
                                padding="6",
                            ),
                            width="100%",
                            border_radius="2xl",
                        ),
                        width="30%",
                        padding_left="8",
                        position="sticky",
                        top="100px",
                    ),
                    width="100%",
                    align="start",
                    padding_bottom="20",
                ),
            ),
            max_width="1280px",
            width="100%",
            padding_x="8",
        )
    )
