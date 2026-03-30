import reflex as rx
from state.user_state import UserState
from state.cart_state import CartState
from state.products_state import ProductsState   # Make sure this matches exactly


def navbar():
    return rx.box(
        rx.hstack(
            # Logo
            rx.hstack(
                rx.icon("shopping-bag", size=28, color="blue.600"),
                rx.heading("AI Shop", size="6", color="blue.600", font_weight="bold"),
                on_click=rx.redirect("/"),
                cursor="pointer",
                spacing="2",
            ),

            # Search Bar
            rx.box(
                rx.hstack(
                    rx.input(
                        placeholder="Search products...",
                        value=ProductsState.search_query,
                        on_change=ProductsState.set_search_query,
                        width="420px",
                        size="3",
                        border_radius="full",
                    ),
                    rx.icon("search", position="absolute", left="1.2em", top="50%", transform="translateY(-50%)", color="gray.400"),
                    position="relative",
                ),
                display=rx.cond(UserState.logged_in, "block", "none"),
            ),

            # Navigation Links
            rx.hstack(
                rx.link("Home", on_click=rx.redirect("/"), padding="0.5em 1em"),
                rx.link("Products", on_click=rx.redirect("/products"), padding="0.5em 1em"),
                rx.link("Recommendations", on_click=rx.redirect("/recommendations"), padding="0.5em 1em"),
                spacing="2",
            ),

            # Right side
            rx.hstack(
                # Cart
                rx.link(
                    rx.hstack(
                        rx.icon("shopping-cart", size=22),
                        rx.badge(
                            rx.cond(len(CartState.cart_items) > 0, len(CartState.cart_items), ""),
                            color_scheme="red",
                            size="sm",
                            position="absolute",
                            top="-6px",
                            right="-8px",
                        ),
                    ),
                    on_click=rx.redirect("/cart"),
                    position="relative",
                    padding="0.5em",
                ),

                # Auth Section
                rx.cond(
                    UserState.logged_in,
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.button(
                                rx.hstack(rx.icon("user"), rx.text(UserState.email.split("@")[0] if UserState.email else ""), spacing="2"),
                                variant="ghost",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item("Profile", on_click=rx.redirect("/profile")),
                            rx.menu.separator(),
                            rx.menu.item("Logout", on_click=UserState.logout, color="red.600"),
                        ),
                    ),
                    rx.hstack(
                        rx.button("Login", on_click=rx.redirect("/login"), variant="ghost"),
                        rx.button("Sign Up", on_click=rx.redirect("/signup"), color_scheme="blue"),
                        spacing="3",
                    )
                ),
                spacing="4",
                align="center",
            ),

            spacing="8",
            width="100%",
            align="center",
            padding_x="2em",
            padding_y="1em",
            border_bottom="1px solid #e2e8f0",
            background_color="white",
            position="sticky",
            top="0",
            z_index="1000",
        ),
        width="100%",
    )