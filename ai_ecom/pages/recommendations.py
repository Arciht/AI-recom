import reflex as rx
from components.recommendation_card import recommendation_card
from state.user_state import UserState
from state.recommendation_state import RecommendationState
from state.cart_state import CartState


@rx.page(
    route="/recommendations",
    title="AI Recommendations",
    on_load=RecommendationState.load_recommendations
)
def recommendations_page():
    return rx.vstack(
        # Header Section
        rx.vstack(
            rx.heading(
                rx.cond(
                    UserState.user_type == "new",
                    "Popular Picks For New Users",
                    "Personalized Recommendations For You"
                ),
                size="9",
                text_align="center",
            ),
            rx.text(
                rx.cond(
                    UserState.user_type == "new",
                    "Based on highest customer ratings across all users",
                    "Based on your past behavior & what similar users liked"
                ),
                font_size="lg",
                color="gray.600",
                text_align="center",
                max_width="600px",
            ),
            spacing="2",
            align="center",
        ),

        # Refresh Button
        rx.button(
            rx.hstack(
                rx.icon("refresh-cw"),
                rx.text("Refresh Recommendations"),
                spacing="2",
            ),
            on_click=RecommendationState.load_recommendations,
            color_scheme="green",
            size="4",
            variant="solid",
        ),

        # Recommendations Grid
        rx.grid(
            rx.foreach(
                RecommendationState.recommendations,
                recommendation_card
            ),
            columns=["1", "2", "3", "4"],   # Responsive grid
            spacing="6",
            width="100%",
            padding_y="2em",
        ),

        # Empty State (if no recommendations)
        rx.cond(
            len(RecommendationState.recommendations) == 0,
            rx.vstack(
                rx.icon("alert-circle", size=60, color="gray.400"),
                rx.heading("No recommendations yet", size="6"),
                rx.text(
                    "Please login or try refreshing",
                    color="gray.500"
                ),
                rx.button(
                    "Go to All Products",
                    on_click=rx.redirect("/products"),
                    color_scheme="blue",
                ),
                spacing="4",
                padding="6em",
                align="center",
            )
        ),

        # Quick Links
        rx.hstack(
            rx.button(
                "Browse All Products",
                on_click=rx.redirect("/products"),
                variant="outline",
                size="4",
            ),
            rx.button(
                "View Cart",
                on_click=rx.redirect("/cart"),
                color_scheme="blue",
                size="4",
            ),
            spacing="4",
        ),

        spacing="10",
        padding="2em",
        align="center",
        width="100%",
        min_height="100vh",
        background_color=rx.color("gray", 50),
    )