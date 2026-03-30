import reflex as rx
from state.user_state import UserState


@rx.page(route="/signup", title="Sign Up - AI Shop")
def signup_page():
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Create Account", size="8", text_align="center"),
                rx.text("Join us and get AI-powered recommendations", 
                       color="gray.600", text_align="center"),

                # Email Input
                rx.vstack(
                    rx.text("Email", font_weight="medium", margin_bottom="4px"),
                    rx.input(
                        placeholder="Enter your email",
                        type="email",
                        on_blur=UserState.set_signup_email,
                        width="100%",
                        size="3",
                    ),
                    align="stretch",
                    spacing="1",
                ),

                # Password Input
                rx.vstack(
                    rx.text("Password", font_weight="medium", margin_bottom="4px"),
                    rx.input(
                        placeholder="Create a password (min 6 characters)",
                        type="password",
                        on_blur=UserState.set_signup_password,
                        width="100%",
                        size="3",
                    ),
                    align="stretch",
                    spacing="1",
                ),

                # Error Message
                rx.cond(
                    UserState.error_message != "",
                    rx.text(
                        UserState.error_message,
                        color="red.500",
                        font_size="sm",
                        text_align="center"
                    )
                ),

                # Signup Button
                rx.button(
                    "Create Account",
                    on_click=UserState.signup,
                    width="100%",
                    size="lg",
                    color_scheme="green",
                ),

                # Login Link
                rx.hstack(
                    rx.text("Already have an account?"),
                    rx.link(
                        "Login here",
                        on_click=rx.redirect("/login"),
                        color="blue.500",
                        font_weight="medium",
                    ),
                    spacing="2",
                    justify="center",
                ),

                spacing="6",
                width="100%",
                max_width="420px",
                padding="2.5em",
            ),
            box_shadow="xl",
            border_radius="15px",
        ),
        min_height="100vh",
        background_color="gray.50",
    )