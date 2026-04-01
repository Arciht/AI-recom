import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer

from ..components.layout import layout

def payment_success_page() -> rx.Component:
    return layout(
        rx.center(
            rx.vstack(
                rx.box(
                    rx.icon("circle_check", size=80, color="green.500"),
                    padding="6",
                    background_color="green.50",
                    border_radius="full",
                    margin_bottom="8",
                ),
                rx.heading("Payment Successful!", size="9", color="#111827"),
                rx.text(
                    "Your order has been placed successfully. We'll send you a confirmation email shortly.",
                    color="gray.600",
                    text_align="center",
                    max_width="500px",
                ),
                rx.box(
                    rx.hstack(
                        rx.text("Order ID:", font_weight="medium"),
                        rx.text("ORD-2024-AI89", color="#3b82f6", font_weight="bold"),
                        spacing="2",
                    ),
                    padding_y="6",
                ),
                rx.hstack(
                    rx.button(
                        "View My Orders",
                        on_click=rx.redirect("/orders"),
                        color_scheme="blue",
                        size="4",
                    ),
                    rx.button(
                        "Continue Shopping",
                        on_click=rx.redirect("/products"),
                        variant="outline",
                        size="4",
                    ),
                    spacing="4",
                    padding_top="8",
                ),
                spacing="4",
                align="center",
                padding_y="20",
            ),
            width="100%",
        )
    )
