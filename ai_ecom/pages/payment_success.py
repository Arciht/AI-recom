import reflex as rx
import datetime
from ..components.navbar import navbar
from ..components.footer import footer
from ..state.cart_state import CartState
from .orders import OrdersState, Order, OrderItem

class PaymentSuccessState(rx.State):
    payment_id: str = ""
    order_id: str = ""
    
    async def finalize_order(self):
        """Pick up Razorpay params from URL and create order"""
        self.payment_id = self.router.page.params.get("payment_id", "")
        self.order_id = self.router.page.params.get("order_id", "ORD-UNKNOWN")
        
        cart_state = await self.get_state(CartState)
        
        # Only process if we have a payment ID (means we just arrived from Razorpay)
        if self.payment_id and cart_state.cart_items:
            # Create new order in our local state
            order_items = [
                OrderItem(name=item["product_name"], price=str(item["price"]), qty=item["quantity"])
                for item in cart_state.cart_items
            ]
            
            new_order = Order(
                order_id=self.order_id,
                date=datetime.datetime.now().strftime("%b %d, %Y"),
                total=str(cart_state.total),
                status="Paid",
                order_items=order_items
            )
            
            orders_state = await self.get_state(OrdersState)
            orders_state.add_order(new_order)
            
            # Clear the cart now that payment is confirmed
            cart_state.clear_cart()
            
            return rx.toast("Payment verified and order placed!")

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
                        rx.text(PaymentSuccessState.order_id, color="#3b82f6", font_weight="bold"),
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
