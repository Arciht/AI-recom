import reflex as rx

def footer():
    return rx.box(
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.vstack(
                    rx.heading("AI Shop", size="6", color="#3b82f6"),
                    rx.text("Personalized shopping experience powered by AI.", color="gray.600", size="2"),
                    align="start",
                    spacing="2",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.vstack(
                        rx.text("Shop", font_weight="bold", size="3"),
                        rx.link("Products", href="/products", color="gray.600", size="2"),
                        rx.link("Recommendations", href="/recommendations", color="gray.600", size="2"),
                        align="start",
                        spacing="2",
                    ),
                    rx.vstack(
                        rx.text("Account", font_weight="bold", size="3"),
                        rx.link("Profile", href="/profile", color="gray.600", size="2"),
                        rx.link("Orders", href="/orders", color="gray.600", size="2"),
                        align="start",
                        spacing="2",
                    ),
                    spacing="8",
                ),
                width="100%",
                padding_y="8",
            ),
            rx.hstack(
                rx.text("© 2024 AI Shop. All rights reserved.", color="gray.500", size="1"),
                rx.spacer(),
                rx.hstack(
                    rx.icon("facebook", size=18, color="gray.400"),
                    rx.icon("twitter", size=18, color="gray.400"),
                    rx.icon("instagram", size=18, color="gray.400"),
                    spacing="4",
                ),
                width="100%",
                padding_y="4",
                border_top="1px solid #f3f4f6",
            ),
            spacing="0",
        ),
        padding_x="8",
        width="100%",
        background_color="white",
    )
