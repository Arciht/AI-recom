import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..state.cart_state import CartState

class PaymentState(rx.State):
    is_processing: bool = False
    
    def process_payment(self):
        self.is_processing = True
        return rx.wait(2, PaymentState.complete_payment)
    
    def complete_payment(self):
        self.is_processing = False
        CartState.clear_cart()
        return rx.redirect("/payment-success")

from ..components.layout import layout

def payment_page() -> rx.Component:
    return layout(
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Payment", size="8", color="#111827"),
                    rx.text("Complete your purchase securely.", color="gray.600"),
                    
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("Order Total", font_weight="medium"),
                                rx.spacer(),
                                rx.text(f"₹{CartState.total}", font_weight="bold", color="#3b82f6", size="6"),
                                width="100%",
                            ),
                            padding="6",
                            background_color="#f9fafb",
                            border_radius="xl",
                            width="100%",
                            margin_y="6",
                        ),
                        width="100%",
                    ),
                    
                    rx.vstack(
                        rx.button(
                            rx.cond(
                                PaymentState.is_processing,
                                rx.hstack(rx.spinner(size="1"), rx.text("Processing...")),
                                rx.hstack(rx.icon("credit_card"), rx.text("Pay with Razorpay (Test)"))
                            ),
                            on_click=PaymentState.process_payment,
                            color_scheme="blue",
                            width="100%",
                            size="4",
                            is_disabled=PaymentState.is_processing,
                        ),
                        rx.button(
                            "Pay Later",
                            on_click=rx.redirect("/orders"),
                            variant="ghost",
                            width="100%",
                            size="3",
                            is_disabled=PaymentState.is_processing,
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    
                    rx.hstack(
                        rx.icon("shield_check", size=16, color="green.600"),
                        rx.text("SSL Secured Payment", size="1", color="gray.500"),
                        spacing="1",
                        align="center",
                        padding_top="6",
                    ),
                    
                    spacing="4",
                    width="400px",
                    padding="8",
                    align="center",
                ),
                box_shadow="2xl",
                border_radius="2xl",
            ),
            width="100%",
            padding_y="24",
            background_color="#f9fafb",
        )
    )
