import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..components.product_card import recommendation_card
from ..state.recommendation_state import RecommendationState

from ..components.layout import layout

def recommendations_page() -> rx.Component:
    return layout(
        rx.vstack(
            # Header Section
            rx.vstack(
                rx.heading("Personalized Recommendations", size="9", color="#111827"),
                rx.text("AI-powered suggestions based on your unique preferences and history.", color="gray.600", size="4"),
                rx.button(
                    "Refresh Recommendations",
                    on_click=RecommendationState.refresh_recommendations,
                    color_scheme="blue",
                    variant="soft",
                    size="3",
                    margin_top="6",
                ),
                align="center",
                spacing="4",
                padding_y="16",
                width="100%",
            ),
            
            # Content Section
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Based on Your History", value="history", size="3"),
                    rx.tabs.trigger("Similar Users Also Liked", value="collaborative", size="3"),
                    justify_content="center",
                    width="100%",
                    padding_bottom="8",
                ),
                rx.tabs.content(
                    rx.cond(
                        RecommendationState.is_loading,
                        rx.center(rx.spinner(size="3", color="#3b82f6"), width="100%", height="400px"),
                        rx.grid(
                            rx.foreach(
                                RecommendationState.content_based_recs,
                                recommendation_card
                            ),
                            columns="4",
                            spacing="6",
                            width="100%",
                            padding_bottom="20",
                        ),
                    ),
                    value="history",
                ),
                rx.tabs.content(
                    rx.cond(
                        RecommendationState.is_loading,
                        rx.center(rx.spinner(size="3", color="#3b82f6"), width="100%", height="400px"),
                        rx.grid(
                            rx.foreach(
                                RecommendationState.collaborative_recs,
                                recommendation_card
                            ),
                            columns="4",
                            spacing="6",
                            width="100%",
                            padding_bottom="20",
                        ),
                    ),
                    value="collaborative",
                ),
                default_value="history",
                width="100%",
            ),
            
            max_width="1280px",
            width="100%",
            padding_x="8",
        )
    )
