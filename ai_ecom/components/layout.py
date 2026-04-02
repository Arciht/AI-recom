import reflex as rx
from .navbar import navbar
from .footer import footer
from .chatbot import chatbot

def layout(child: rx.Component) -> rx.Component:
    return rx.box(
        rx.vstack(
            navbar(),
            rx.box(
                child,
                width="100%",
                min_height="80vh",
                background_color="#f8fafc", # Lighter background
            ),
            # footer(), # Footer removed as requested
            spacing="0",
            width="100%",
        ),
        chatbot(),
        width="100%",
    )
