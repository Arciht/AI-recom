import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..components.product_card import product_card
from ..state.products_state import ProductsState

from ..components.layout import layout

def products_page() -> rx.Component:
    return layout(
        rx.vstack(
            # Search and Header
            rx.vstack(
                rx.heading("Explore Our Collection", size="8", color="#111827"),
                rx.text("Find exactly what you're looking for with our smart search.", color="gray.600"),
                rx.hstack(
                    rx.input(
                        placeholder="Search by name, category, or tags...",
                        value=ProductsState.search_query,
                        on_change=ProductsState.set_search_query,
                        width="100%",
                        max_width="600px",
                        size="3",
                        border_radius="full",
                    ),
                    rx.button(
                        "Clear",
                        on_click=lambda: ProductsState.set_search_query(""),
                        variant="ghost",
                        color_scheme="blue",
                    ),
                    width="100%",
                    justify="center",
                    padding_top="4",
                ),
                width="100%",
                padding_y="12",
                align="center",
            ),
            
            # Main Content with Sidebar
            rx.hstack(
                # Sidebar Filters
                rx.vstack(
                    rx.heading("Categories", size="4", color="#111827", margin_bottom="4"),
                    rx.vstack(
                        rx.button("All Products", variant="ghost", width="100%", justify_content="start", color_scheme="blue"),
                        rx.button("Electronics", variant="ghost", width="100%", justify_content="start", color="gray.600"),
                        rx.button("Fashion", variant="ghost", width="100%", justify_content="start", color="gray.600"),
                        rx.button("Home & Kitchen", variant="ghost", width="100%", justify_content="start", color="gray.600"),
                        rx.button("Beauty", variant="ghost", width="100%", justify_content="start", color="gray.600"),
                        spacing="1",
                        width="100%",
                    ),
                    rx.divider(margin_y="6"),
                    rx.heading("Price Range", size="4", color="#111827", margin_bottom="4"),
                    rx.vstack(
                        rx.checkbox("Under ₹500", size="2"),
                        rx.checkbox("₹500 - ₹2000", size="2"),
                        rx.checkbox("₹2000 - ₹5000", size="2"),
                        rx.checkbox("Over ₹5000", size="2"),
                        align="start",
                        spacing="3",
                    ),
                    width="250px",
                    padding="6",
                    background_color="white",
                    border_radius="xl",
                    border="1px solid #f3f4f6",
                    display=["none", "none", "flex"],
                    align_self="start",
                ),
                
                # Products Grid
                rx.vstack(
                    rx.cond(
                        ProductsState.filtered_products.length() == 0,
                        rx.center(
                            rx.vstack(
                                rx.icon("search_x", size=48, color="gray.300"),
                                rx.heading("No products found", size="6", color="gray.500"),
                                rx.button("Reset Search", on_click=lambda: ProductsState.set_search_query("")),
                                spacing="4",
                                padding="20",
                            ),
                            width="100%",
                        ),
                        rx.grid(
                            rx.foreach(
                                ProductsState.filtered_products,
                                product_card
                            ),
                            columns=rx.breakpoints(initial="1", sm="2", md="3", lg="3"),
                            spacing="6",
                            width="100%",
                        ),
                    ),
                    width="100%",
                ),
                width="100%",
                spacing="8",
                align="start",
            ),
            
            max_width="1280px",
            width="100%",
            padding_x="8",
            padding_bottom="20",
        )
    )
