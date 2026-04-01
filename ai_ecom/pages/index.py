import reflex as rx
from components.recommendation_card import recommendation_card
from state.user_state import UserState
from state.recommendation_state import RecommendationState
from state.cart_state import CartState


@rx.page(route="/", title="AI Shop - Home")
def index():
    return rx.vstack(
        # Hero Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "Discover Products You’ll Love",
                    size="9",
                    text_align="center",
                    line_height="1.1",
                ),
                rx.text(
                    "AI-powered recommendations tailored just for you",
                    font_size="2xl",
                    color="gray.600",
                    text_align="center",
                    max_width="700px",
                ),
                rx.cond(
                    UserState.logged_in,
                    rx.button(
                        "View My Recommendations",
                        on_click=rx.redirect("/recommendations"),
                        size="4",
                        color_scheme="blue",
                        height="55px",
                        font_size="lg",
                    ),
                    rx.hstack(
                        rx.button(
                            "Login to Get Personalized Recommendations",
                            on_click=rx.redirect("/login"),
                            size="4",
                            color_scheme="blue",
                        ),
                        rx.button(
                            "Browse All Products",
                            on_click=rx.redirect("/products"),
                            size="4",
                            variant="outline",
                        ),
                        spacing="4",
                    )
                ),
                spacing="6",
                align="center",
                padding_y="4em",
            ),
            width="100%",
            background="linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%)",
            border_bottom="1px solid #e2e8f0",
        ),

        # Recommendations Section
        rx.vstack(
            rx.hstack(
                rx.heading(
                    rx.cond(
                        UserState.logged_in,
                        "Recommended For You",
                        "Popular Products"
                    ),
                    size="7",
                ),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("refresh-cw"),
                        rx.text("Refresh"),
                        spacing="2",
                    ),
                    on_click=RecommendationState.load_recommendations,
                    variant="outline",
                    size="2",
                ),
                width="100%",
                align="center",
            ),

            # Recommendations Grid
            rx.grid(
                rx.foreach(
                    RecommendationState.recommendations,
                    recommendation_card
                ),
                columns=["1", "2", "3", "4"],
                spacing="6",
                width="100%",
            ),

            # Empty State
            rx.cond(
                len(RecommendationState.recommendations) == 0,
                rx.vstack(
                    rx.text("No recommendations loaded yet", font_size="lg", color="gray.500"),
                    rx.button(
                        "Load Recommendations",
                        on_click=RecommendationState.load_recommendations,
                        color_scheme="green",
                    ),
                    padding="4em",
                    align="center",
                )
            ),

            spacing="8",
            width="100%",
            padding_x="2em",
            padding_y="3em",
        ),

        # Quick Links Section
        rx.vstack(
            rx.heading("Explore More", size="6", text_align="center"),
            rx.hstack(
                rx.card(
                    rx.vstack(
                        rx.icon("package", size=40, color="blue.500"),
                        rx.text("All Products", font_weight="bold"),
                        rx.button(
                            "Browse",
                            on_click=rx.redirect("/products"),
                            variant="ghost",
                            size="2",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    padding="2em",
                    width="280px",
                ),
                rx.card(
                    rx.vstack(
                        rx.icon("heart", size=40, color="red.500"),
                        rx.text("Recommendations", font_weight="bold"),
                        rx.button(
                            "View All",
                            on_click=rx.redirect("/recommendations"),
                            variant="ghost",
                            size="2",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    padding="2em",
                    width="280px",
                ),
                rx.card(
                    rx.vstack(
                        rx.icon("user", size=40, color="purple.500"),
                        rx.text("My Profile", font_weight="bold"),
                        rx.button(
                            "Go to Profile",
                            on_click=rx.redirect("/profile"),
                            variant="ghost",
                            size="2",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    padding="2em",
                    width="280px",
                ),
                spacing="6",
            ),
            padding_y="4em",
            width="100%",
            align="center",
        ),

        width="100%",
        spacing="0",
        align="center",
    )