import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..state.cart_state import CartState

class CheckoutState(rx.State):
    full_name: str = ""
    address: str = ""
    city: str = ""
    pin_code: str = ""
    phone: str = ""
    email: str = ""
    
    def set_full_name(self, value): self.full_name = value
    def set_address(self, value): self.address = value
    def set_city(self, value): self.city = value
    def set_pin_code(self, value): self.pin_code = value
    def set_phone(self, value): self.phone = value
    def set_email(self, value): self.email = value
    
    def proceed_to_payment(self):
        if not all([self.full_name, self.address, self.city, self.pin_code, self.phone, self.email]):
            return rx.toast("Please fill all fields", color_scheme="red")
        return rx.redirect("/payment")

from ..components.layout import layout

def checkout_page() -> rx.Component:
    return layout(
        rx.vstack(
            rx.heading("Checkout", size="8", color="#111827", padding_y="8"),
            
            rx.hstack(
                # Left: Shipping Form
                rx.vstack(
                    rx.card(
                        rx.vstack(
                            rx.heading("Shipping Information", size="5", margin_bottom="4"),
                            rx.grid(
                                rx.vstack(
                                    rx.text("Full Name", size="2", font_weight="medium"),
                                    rx.input(placeholder="John Doe", on_change=CheckoutState.set_full_name, size="3", width="100%"),
                                    align="start", spacing="1", width="100%",
                                ),
                                rx.vstack(
                                    rx.text("Email Address", size="2", font_weight="medium"),
                                    rx.input(placeholder="john@example.com", on_change=CheckoutState.set_email, size="3", width="100%"),
                                    align="start", spacing="1", width="100%",
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.text("Address", size="2", font_weight="medium"),
                                        rx.text_area(placeholder="House No, Street Name", on_change=CheckoutState.set_address, size="3", width="100%"),
                                        align="start", spacing="1", width="100%",
                                    ),
                                    grid_column="span 2",
                                ),
                                rx.vstack(
                                    rx.text("City", size="2", font_weight="medium"),
                                    rx.input(placeholder="New York", on_change=CheckoutState.set_city, size="3", width="100%"),
                                    align="start", spacing="1", width="100%",
                                ),
                                rx.vstack(
                                    rx.text("Pin Code", size="2", font_weight="medium"),
                                    rx.input(placeholder="10001", on_change=CheckoutState.set_pin_code, size="3", width="100%"),
                                    align="start", spacing="1", width="100%",
                                ),
                                rx.vstack(
                                    rx.text("Phone Number", size="2", font_weight="medium"),
                                    rx.input(placeholder="+1 234 567 890", on_change=CheckoutState.set_phone, size="3", width="100%"),
                                    align="start", spacing="1", width="100%",
                                ),
                                columns="2",
                                spacing="4",
                                width="100%",
                            ),
                            spacing="4",
                            width="100%",
                            padding="6",
                        ),
                        width="100%",
                        border_radius="2xl",
                    ),
                    width="65%",
                ),
                
                # Right: Summary
                rx.vstack(
                    rx.card(
                        rx.vstack(
                            rx.heading("Order Summary", size="5", margin_bottom="4"),
                            rx.vstack(
                                rx.foreach(
                                    CartState.cart_items,
                                    lambda item: rx.hstack(
                                        rx.text(item["product_name"], size="2", color="gray.600", text_overflow="ellipsis", white_space="nowrap", overflow="hidden", width="150px"),
                                        rx.spacer(),
                                        rx.text(f"x{item['quantity']}", size="2", color="gray.400"),
                                        rx.spacer(),
                                        rx.text(f"₹{item['price']}", size="2", font_weight="medium"),
                                        width="100%",
                                    )
                                ),
                                spacing="2",
                                width="100%",
                                max_height="200px",
                                overflow_y="auto",
                            ),
                            rx.divider(margin_y="4"),
                            rx.hstack(
                                rx.text("Total Amount", font_weight="bold"),
                                rx.spacer(),
                                rx.text(f"₹{CartState.total}", font_weight="bold", color="#3b82f6", size="5"),
                                width="100%",
                            ),
                            rx.button(
                                "Place Order",
                                on_click=CheckoutState.proceed_to_payment,
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
                    width="35%",
                    padding_left="8",
                ),
                width="100%",
                align="start",
                padding_bottom="20",
            ),
            max_width="1280px",
            width="100%",
            padding_x="8",
        )
    )
