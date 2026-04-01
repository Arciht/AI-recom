import reflex as rx
from ..state.user_state import UserState
from ..components.navbar import navbar
from ..components.footer import footer

from ..components.layout import layout

def signup_page() -> rx.Component:
    return layout(
        rx.center(
            rx.card(
                rx.vstack(
                    rx.vstack(
                        rx.heading("Create Account", size="8", color="#111827"),
                        rx.text("Join us for a personalized shopping experience", color="gray.600", size="3"),
                        align="center",
                        spacing="2",
                    ),
                    
                    rx.vstack(
                        rx.text("Full Name", size="2", font_weight="medium", width="100%"),
                        rx.input(
                            placeholder="John Doe",
                            size="3",
                            width="100%",
                        ),
                        rx.text("Email Address", size="2", font_weight="medium", width="100%"),
                        rx.input(
                            placeholder="name@example.com",
                            on_change=UserState.set_signup_email,
                            value=UserState.signup_email,
                            size="3",
                            width="100%",
                        ),
                        rx.text("Password", size="2", font_weight="medium", width="100%"),
                        rx.input(
                            type="password",
                            placeholder="••••••••",
                            on_change=UserState.set_signup_email,
                            value=UserState.signup_password,
                            size="3",
                            width="100%",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    
                    rx.button(
                        "Create Account",
                        on_click=UserState.signup,
                        width="100%",
                        color_scheme="blue",
                        size="4",
                    ),
                    
                    rx.cond(
                        UserState.error_message,
                        rx.text(UserState.error_message, color="red.500", size="2", text_align="center"),
                    ),
                    
                    rx.hstack(
                        rx.text("Already have an account?", size="2", color="gray.600"),
                        rx.link("Sign In", href="/login", size="2", color="#3b82f6", font_weight="medium"),
                        spacing="2",
                    ),
                    spacing="6",
                    width="400px",
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
