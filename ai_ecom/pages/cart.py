import reflex as rx
from state.cart_state import CartState
from state.user_state import UserState


@rx.page(route="/cart", title="Your Cart")
def cart_page():
    return rx.vstack(
        rx.heading("Your Shopping Cart", size="9", text_align="center"),

        rx.cond(
            # If cart has items
            len(CartState.cart_items) > 0,
            rx.vstack(
                # Cart Items List
                rx.vstack(
                    rx.foreach(
                        CartState.cart_items,
                        lambda item: rx.card(
                            rx.hstack(
                                # Product Image
                                rx.image(
                                    src=item.get("image_url", "/assets/placeholder.jpg"),
                                    width="100px",
                                    height="100px",
                                    object_fit="cover",
                                    border_radius="8px",
                                ),
                                
                                # Product Details
                                rx.vstack(
                                    rx.heading(item.get("product_name", ""), size="5"),
                                    rx.text(f"₹{float(item.get('price', 0)):.2f}", 
                                           font_size="lg", 
                                           font_weight="bold"),
                                    spacing="1",
                                    align="start",
                                ),
                                
                                rx.spacer(),
                                
                                # Quantity & Remove
                                rx.hstack(
                                    rx.text(f"Qty: {item.get('quantity', 1)}"),
                                    rx.button(
                                        "Remove",
                                        on_click=lambda i=item.get("product_id"): CartState.remove_from_cart(i),
                                        color_scheme="red",
                                        variant="ghost",
                                        size="sm",
                                    ),
                                    spacing="4",
                                    align="center",
                                ),
                                width="100%",
                                align="center",
                            ),
                            padding="1.2em",
                            width="100%",
                        )
                    ),
                    spacing="4",
                    width="100%",
                    max_width="800px",
                ),

                # Order Summary Card
                rx.card(
                    rx.vstack(
                        rx.heading("Order Summary", size="6"),
                        rx.hstack(
                            rx.text("Subtotal", font_size="lg"),
                            rx.spacer(),
                            rx.text(f"₹{CartState.total:.2f}", font_size="lg", font_weight="bold"),
                        ),
                        rx.hstack(
                            rx.text("Shipping", font_size="lg"),
                            rx.spacer(),
                            rx.text("Free", color="green.600", font_weight="bold"),
                        ),
                        rx.divider(),
                        rx.hstack(
                            rx.text("Total", font_size="xl", font_weight="bold"),
                            rx.spacer(),
                            rx.text(
                                f"₹{CartState.total:.2f}",
                                font_size="2xl",
                                font_weight="bold",
                                color="green.700"
                            ),
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    padding="2em",
                    width="100%",
                    max_width="800px",
                ),

                # Action Buttons
                rx.hstack(
                    rx.button(
                        "Continue Shopping",
                        on_click=rx.redirect("/products"),
                        variant="outline",
                        size="lg",
                    ),
                    rx.button(
                        "Proceed to Checkout",
                        on_click=rx.redirect("/checkout"),
                        color_scheme="green",
                        size="lg",
                    ),
                    spacing="6",
                ),

                spacing="8",
                align="center",
                width="100%",
                padding_y="2em",
            ),

            # Empty Cart State
            rx.vstack(
                rx.icon("shopping-cart", size=100, color="gray.300"),
                rx.heading("Your cart is empty", size="7"),
                rx.text(
                    "Looks like you haven't added anything to your cart yet.",
                    font_size="lg",
                    color="gray.500",
                ),
                rx.button(
                    "Browse Products",
                    on_click=rx.redirect("/products"),
                    size="lg",
                    color_scheme="blue",
                ),
                spacing="6",
                padding="8em 0",
                align="center",
            )
        ),

        width="100%",
        align="center",
        padding="2em",
    )