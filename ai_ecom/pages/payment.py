import reflex as rx
import asyncio
import razorpay
import os
from dotenv import load_dotenv
from ..components.navbar import navbar
from ..components.footer import footer
from ..state.cart_state import CartState
from .orders import OrdersState, Order, OrderItem
import datetime

load_dotenv()

class PaymentState(rx.State):
    is_processing: bool = False
    razorpay_order_id: str = ""
    
    @rx.var
    def razorpay_key(self) -> str:
        return os.getenv("RAZORPAY_KEY_ID", "")

    async def create_razorpay_order(self):
        self.is_processing = True
        yield
        
        # 1. Initialize Razorpay client
        key_id = os.getenv("RAZORPAY_KEY_ID")
        key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        
        if not key_id or not key_secret:
            self.is_processing = False
            yield rx.toast("Razorpay keys not configured", color_scheme="red")
            return
            
        client = razorpay.Client(auth=(key_id, key_secret))
        
        # 2. Get the actual cart state and total
        cart_state = await self.get_state(CartState)
        
        # 3. Create order on Razorpay
        # Amount is in paisa (e.g., ₹100 = 10000 paisa)
        amount_paisa = int(float(cart_state.total) * 100)
        
        try:
            data = {
                "amount": amount_paisa,
                "currency": "INR",
                "receipt": f"receipt_{datetime.datetime.now().strftime('%M%S')}",
                "payment_capture": 1 # Auto capture
            }
            order = client.order.create(data=data)
            self.razorpay_order_id = order['id']
            
            # 3. Trigger Razorpay Checkout on Frontend
            yield rx.call_script(
                f"""
                var options = {{
                    "key": "{key_id}",
                    "amount": "{amount_paisa}",
                    "currency": "INR",
                    "name": "AI Shop",
                    "description": "Purchase from AI Recommender Shop",
                    "order_id": "{self.razorpay_order_id}",
                    "handler": function (response) {{
                        // Redirect to success page with payment details
                        window.location.href = "/payment-success?payment_id=" + response.razorpay_payment_id + "&order_id=" + response.razorpay_order_id + "&signature=" + response.razorpay_signature;
                    }},
                    "prefill": {{
                        "name": "Customer",
                        "email": "customer@example.com"
                    }},
                    "theme": {{
                        "color": "#3b82f6"
                    }}
                }};
                var rzp1 = new Razorpay(options);
                rzp1.open();
                """
            )
        except Exception as e:
            self.is_processing = False
            yield rx.toast(f"Error creating payment: {str(e)}", color_scheme="red")

    async def handle_payment_success(self, details: dict):
        """Callback from Frontend after successful Razorpay payment"""
        self.is_processing = False
        
        # Create new order in our local state
        order_items = [
            OrderItem(name=item["product_name"], price=str(item["price"]), qty=item["quantity"])
            for item in CartState.cart_items
        ]
        
        new_order = Order(
            order_id=details.get("order_id", f"ORD-{datetime.datetime.now().strftime('%M%S')}"),
            date=datetime.datetime.now().strftime("%b %d, %Y"),
            total=str(CartState.total),
            status="Paid",
            order_items=order_items
        )
        
        orders_state = await self.get_state(OrdersState)
        orders_state.add_order(new_order)
        
        CartState.clear_cart()
        return rx.redirect("/payment-success")

from ..components.layout import layout

def payment_page() -> rx.Component:
    return layout(
        rx.center(
            # Just load the Razorpay SDK
            rx.script(src="https://checkout.razorpay.com/v1/checkout.js"),
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
                            on_click=PaymentState.create_razorpay_order,
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
                    
                    spacing="6",
                    align="center",
                    width="450px",
                    padding="8",
                ),
                box_shadow="2xl",
                border_radius="2xl",
            ),
            width="100%",
            padding_y="24",
            background_color="#f9fafb",
        )
    )
