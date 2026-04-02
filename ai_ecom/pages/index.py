import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..components.product_card import product_card, recommendation_card
from ..components.chatbot import chatbot
from ..state.recommendation_state import RecommendationState
from ..state.products_state import ProductsState

from ..components.layout import layout

def index() -> rx.Component:
    return layout(
        rx.vstack(
            # Hero Section
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Discover Your Next Favorite Thing",
                        size="7", # Reduced from 8
                        color="#111827", # Black instead of white
                        text_align="center",
                        line_height="1.2",
                        font_weight="bold",
                    ),
                    rx.text(
                        "AI-powered recommendations tailored just for you. Shop the best products across electronics, fashion, and home.",
                        size="4",
                        color="#374151", # Darker gray for better contrast
                        text_align="center",
                        max_width="700px",
                    ),
                    rx.button(
                        "Get Personalized Recommendations",
                        on_click=RecommendationState.trigger_recommendations,
                        size="4",
                        color_scheme="blue",
                        background_color="#2563eb",
                        color="white",
                        _hover={
                            "background_color": "#1d4ed8",
                            "transform": "scale(1.05)",
                            "box_shadow": "0 10px 15px -3px rgba(37, 99, 235, 0.4)"
                        },
                        padding_x="10",
                        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                        border_radius="full",
                    ),
                    spacing="6",
                    align="center",
                    justify="center",
                    height="500px",
                    width="100%",
                ),
                # Lighter gradient background for black text
                background="linear-gradient(rgba(248, 250, 252, 0.8), rgba(248, 250, 252, 0.9)), url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=2070&auto=format&fit=crop')",
                background_size="cover",
                background_position="center",
                width="100%",
                padding_x="8",
            ),
            
            # Main Content
            rx.vstack(
                # Recommended Section
                rx.vstack(
                    rx.hstack(
                        rx.heading("Recommended for You", size="7", color="#111827"),
                        rx.spacer(),
                        rx.link("View All", href="/recommendations", color="#3b82f6", font_weight="medium"),
                        width="100%",
                        align="end",
                    ),
                    rx.cond(
                        RecommendationState.is_loading,
                        rx.center(rx.spinner(size="3", color="#3b82f6"), width="100%", height="200px"),
                        rx.cond(
                            RecommendationState.recommendations.length() > 0,
                            rx.grid(
                                rx.foreach(
                                    RecommendationState.recommendations,
                                    recommendation_card
                                ),
                                columns="4",
                                spacing="6",
                                width="100%",
                            ),
                            rx.center(
                                rx.vstack(
                                    rx.text("No recommendations found yet.", color="gray.500"),
                                    rx.button("Get Recommendations", on_click=RecommendationState.trigger_recommendations, variant="outline"),
                                    spacing="4",
                                    padding="20",
                                ),
                                width="100%",
                            ),
                        ),
                    ),
                    width="100%",
                    padding_y="12",
                ),
                
                # Trending Section
                rx.vstack(
                    rx.hstack(
                        rx.heading("Trending Products", size="7", color="#111827"),
                        rx.spacer(),
                        rx.link("Shop All", href="/products", color="#3b82f6", font_weight="medium"),
                        width="100%",
                        align="end",
                    ),
                    rx.grid(
                        rx.foreach(
                            ProductsState.all_products[:8],
                            product_card
                        ),
                        columns="4",
                        spacing="6",
                        width="100%",
                    ),
                    width="100%",
                    padding_y="12",
                ),
                
                max_width="1280px",
                width="100%",
                padding_x="8",
                spacing="0",
            ),
            spacing="0",
            width="100%",
        )
    )
