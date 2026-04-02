import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer

from typing import List, Dict, Any

from pydantic import BaseModel

class OrderItem(BaseModel):
    name: str
    price: str
    qty: int

class Order(BaseModel):
    order_id: str
    date: str
    total: str
    status: str
    order_items: List[OrderItem]

class OrdersState(rx.State):
    orders: List[Order] = []

    def add_order(self, order: Order):
        self.orders.insert(0, order)

from ..components.layout import layout

def order_item_row(item: OrderItem):
    return rx.hstack(
        rx.text(item.name, size="3", color="gray.700"),
        rx.spacer(),
        rx.text("x" + item.qty.to_string(), size="2", color="gray.400"),
        rx.text("₹" + item.price.to_string(), size="3", font_weight="medium"),
        width="100%",
    )

def orders_page() -> rx.Component:
    return layout(
        rx.vstack(
            rx.heading("My Orders", size="8", color="#111827", padding_y="8"),
            
            rx.vstack(
                rx.foreach(
                    OrdersState.orders,
                    lambda order: rx.card(
                        rx.vstack(
                            # Order Header
                            rx.hstack(
                                rx.vstack(
                                    rx.text("Order ID", size="2", color="gray.500"),
                                    rx.text(order.order_id, font_weight="bold"),
                                    align="start", spacing="0",
                                ),
                                rx.spacer(),
                                rx.vstack(
                                    rx.text("Date", size="2", color="gray.500"),
                                    rx.text(order.date, font_weight="medium"),
                                    align="start", spacing="0",
                                ),
                                rx.spacer(),
                                rx.vstack(
                                    rx.text("Status", size="2", color="gray.500"),
                                    rx.badge(order.status, color_scheme=rx.cond(order.status == "Delivered", "green", "blue")),
                                    align="start", spacing="1",
                                ),
                                width="100%",
                                padding_bottom="4",
                                border_bottom="1px solid #f3f4f6",
                            ),
                            
                            # Order Items Summary
                             rx.vstack(
                                 rx.text(order.order_items.length().to_string() + " items", size="3", color="gray.700"),
                                 padding_y="4",
                                 width="100%",
                             ),
                            
                            # Order Footer
                            rx.hstack(
                                rx.spacer(),
                                rx.text("Total Paid:", color="gray.600"),
                                rx.text("₹" + order.total, font_weight="bold", size="5", color="#3b82f6"),
                                align="center",
                                spacing="4",
                                width="100%",
                                padding_top="4",
                                border_top="1px solid #f3f4f6",
                            ),
                            spacing="0",
                            width="100%",
                        ),
                        width="100%",
                        margin_bottom="6",
                        border_radius="2xl",
                        padding="6",
                    )
                ),
                width="100%",
                max_width="800px",
                padding_bottom="20",
            ),
            max_width="1280px",
            width="100%",
            padding_x="8",
            align="center",
        )
    )
