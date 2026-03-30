import reflex as rx
from state.user_state import UserState
from state.cart_state import CartState


class CheckoutState(rx.State):
    """State for Checkout Page"""
    address: str = ""
    phone: str = ""
    name: str = ""
    payment_status: str = ""   # "success", "failed", ""
    is_processing: bool = False

    def set_name(self, value: str):
        self.name = value

    def set_address(self, value: str):
        self.address = value

    def set_phone(self, value: str):
        self.phone = value

    def process_payment(self):
        """Dummy Razorpay Payment Simulation"""
        if not self.name or not self.address or not self.phone:
            self.payment_status = "Please fill all delivery details"
            return

        if len(CartState.cart_items) == 0:
            self.payment_status = "Your cart is empty"
            return

        self.is_processing = True
        self.payment_status = ""

        # Simulate payment processing delay (like real Razorpay)
        def simulate_razorpay():
            import time
            time.sleep(1.5)  # Simulate network delay
            self.is_processing = False
            self.payment_status = "success"
            # Clear cart after successful payment
            CartState.cart_items = []
            CartState.total = 0.0

        # In real app, you would call Razorpay API here
        rx.call_script("setTimeout(() => { window.location.reload() }, 1800)")  # Simple refresh simulation
        simulate_razorpay()  # This won't actually work in Reflex due to threading, so we'll use a better approach below


    def complete_dummy_payment(self):
        """Better dummy Razorpay flow"""
        if not self.name or not self.address or not self.phone:
            self.payment_status = "Please fill all the delivery details"
            return

        if len(CartState.cart_items) == 0:
            self.payment_status = "Cart is empty!"
            return

        self.is_processing = True

        # Simulate Razorpay success after 1.5 seconds
        self.payment_status = "Processing payment with Razorpay..."

        # Use rx.set_value + delay simulation
        rx.call_script("""
            setTimeout(() => {
                window.location.href = '/success';
            }, 1800);
        """)


@rx.page(route="/checkout", title="Checkout")
def checkout_page():
    return rx.vstack(
        rx.heading("Checkout", size="9", text_align="center"),

        rx.cond(
            UserState.logged_in,
            # Main Checkout Form
            rx.hstack(
                # Left: Delivery Details
                rx.card(
                    rx.vstack(
                        rx.heading("Delivery Details", size="6"),
                        rx.input(
                            placeholder="Full Name",
                            value=CheckoutState.name,
                            on_change=CheckoutState.set_name,
                            size="3",
                        ),
                        rx.input(
                            placeholder="Phone Number",
                            type="tel",
                            value=CheckoutState.phone,
                            on_change=CheckoutState.set_phone,
                            size="3",
                        ),
                        rx.textarea(
                            placeholder="Full Address (House no, Street, City, Pincode)",
                            value=CheckoutState.address,
                            on_change=CheckoutState.set_address,
                            height="120px",
                            size="3",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    padding="2em",
                    width="100%",
                    max_width="500px",
                ),

                # Right: Order Summary + Payment
                rx.vstack(
                    rx.card(
                        rx.vstack(
                            rx.heading("Order Summary", size="6"),
                            
                            # Cart Items Summary
                            rx.foreach(
                                CartState.cart_items,
                                lambda item: rx.hstack(
                                    rx.text(item.get("product_name", "")),
                                    rx.spacer(),
                                    rx.text(f"₹{float(item.get('price', 0)) * item.get('quantity', 1):.2f}"),
                                    width="100%",
                                )
                            ),
                            
                            rx.divider(),
                            
                            # Total
                            rx.hstack(
                                rx.text("Total Amount", font_weight="bold", font_size="lg"),
                                rx.spacer(),
                                rx.text(
                                    f"₹{CartState.total:.2f}",
                                    font_size="2xl",
                                    font_weight="bold",
                                    color="green.600"
                                ),
                                width="100%",
                            ),
                            
                            spacing="4",
                            width="100%",
                        ),
                        padding="2em",
                        width="100%",
                        max_width="450px",
                    ),

                    # Razorpay Payment Button
                    rx.button(
                        rx.cond(
                            CheckoutState.is_processing,
                            rx.hstack(
                                rx.spinner(),
                                rx.text("Processing Payment with Razorpay..."),
                                spacing="3",
                            ),
                            rx.hstack(
                                rx.icon("credit-card"),
                                rx.text("Pay with Razorpay"),
                                spacing="3",
                            )
                        ),
                        on_click=CheckoutState.complete_dummy_payment,
                        width="100%",
                        size="lg",
                        color_scheme="green",
                        height="60px",
                        font_size="lg",
                        is_disabled=CheckoutState.is_processing,
                    ),

                    # Payment Status
                    rx.cond(
                        CheckoutState.payment_status != "",
                        rx.text(
                            CheckoutState.payment_status,
                            color=rx.cond(
                                CheckoutState.payment_status.contains("success"), "green", "red"
                            ),
                            text_align="center",
                        )
                    ),

                    spacing="6",
                    width="100%",
                    max_width="450px",
                ),
                spacing="8",
                align="start",
                width="100%",
                padding="2em",
            ),

            # Not Logged In
            rx.vstack(
                rx.heading("Please Login to Checkout", size="7"),
                rx.button(
                    "Go to Login",
                    on_click=rx.redirect("/login"),
                    size="lg",
                ),
                padding="6em",
            )
        ),

        width="100%",
        max_width="1200px",
        padding_y="2em",
        align="center",
    )