import reflex as rx
from state.user_state import UserState
from state.cart_state import CartState


@rx.page(route="/profile", title="My Profile")
def profile_page():
    return rx.vstack(
        rx.heading("My Profile", size="9", text_align="center"),

        # Main Content
        rx.cond(
            UserState.logged_in,
            # Logged-in User View
            rx.vstack(
                # User Info Card
                rx.card(
                    rx.vstack(
                        rx.icon("user", size=80, color="blue.500"),
                        rx.heading(UserState.email, size="6"),
                        rx.text(f"User ID: {UserState.user_id}", color="gray.500"),
                        rx.badge(
                            rx.cond(
                                UserState.user_type == "new",
                                "New User",
                                "Existing User"
                            ),
                            color_scheme=rx.cond(
                                UserState.user_type == "new", "orange", "green"
                            ),
                            size="lg",
                        ),
                        spacing="4",
                        align="center",
                        padding="2em",
                    ),
                    width="100%",
                    max_width="500px",
                ),

                # Quick Stats
                rx.hstack(
                    rx.card(
                        rx.vstack(
                            rx.text("Orders", font_weight="bold"),
                            rx.text("0", font_size="2xl", font_weight="bold"),  # TODO: connect later
                            align="center",
                        ),
                        padding="1.5em",
                        width="100%",
                    ),
                    rx.card(
                        rx.vstack(
                            rx.text("Wishlist", font_weight="bold"),
                            rx.text("0", font_size="2xl", font_weight="bold"),
                            align="center",
                        ),
                        padding="1.5em",
                        width="100%",
                    ),
                    rx.card(
                        rx.vstack(
                            rx.text("Cart Items", font_weight="bold"),
                            rx.text(len(CartState.cart_items), font_size="2xl", font_weight="bold"),
                            align="center",
                        ),
                        padding="1.5em",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="600px",
                ),

                # Action Buttons
                rx.vstack(
                    rx.button(
                        "View My Orders",
                        width="100%",
                        size="lg",
                        variant="outline",
                        # on_click=... (we'll add later)
                    ),
                    rx.button(
                        "Wishlist",
                        width="100%",
                        size="lg",
                        variant="outline",
                    ),
                    rx.button(
                        "View Cart",
                        on_click=rx.redirect("/cart"),
                        width="100%",
                        size="lg",
                        color_scheme="blue",
                    ),
                    rx.button(
                        "Logout",
                        on_click=UserState.logout,
                        color_scheme="red",
                        width="100%",
                        size="lg",
                    ),
                    spacing="3",
                    width="100%",
                    max_width="400px",
                ),

                spacing="8",
                align="center",
                padding_y="4em",
            ),

            # Not Logged In View
            rx.vstack(
                rx.heading("Please Login to view your profile", size="7"),
                rx.text("You need to be logged in to access this page.", color="gray.600"),
                rx.button(
                    "Go to Login",
                    on_click=rx.redirect("/login"),
                    size="lg",
                    color_scheme="blue",
                ),
                spacing="6",
                padding="6em",
                align="center",
            )
        ),

        width="100%",
        align="center",
        min_height="100vh",
        background_color="gray.50",
    )