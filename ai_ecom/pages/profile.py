import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..state.user_state import UserState
from ..state.cart_state import WishlistState

from ..components.layout import layout

def profile_page() -> rx.Component:
    return layout(
        rx.cond(
            UserState.logged_in,
            rx.vstack(
                rx.heading("My Profile", size="8", color="#111827", padding_y="8"),
                
                rx.hstack(
                    # Left Sidebar: Avatar and Info
                    rx.vstack(
                        rx.card(
                            rx.vstack(
                                rx.avatar(
                                    fallback=UserState.user_name[:2].upper(),
                                    size="9",
                                    color_scheme="blue",
                                    margin_bottom="4",
                                ),
                                rx.heading(UserState.user_name, size="6", color="#111827"),
                                rx.text(UserState.email, color="gray.500", size="2"),
                                rx.badge(
                                    rx.cond(UserState.user_type == "new", "New User", "Returning User"),
                                    color_scheme=rx.cond(UserState.user_type == "new", "orange", "green"),
                                    variant="soft",
                                    margin_top="4",
                                ),
                                rx.button(
                                    "Logout",
                                    on_click=UserState.logout,
                                    color_scheme="red",
                                    variant="ghost",
                                    width="100%",
                                    margin_top="8",
                                ),
                                align="center",
                                padding="8",
                                width="100%",
                            ),
                            width="100%",
                            border_radius="2xl",
                        ),
                        width="300px",
                        spacing="6",
                    ),
                    
                    # Right: Navigation Cards
                    rx.vstack(
                        rx.grid(
                            rx.link(
                                rx.card(
                                    rx.hstack(
                                        rx.box(
                                            rx.icon("shopping_bag", size=32, color="#3b82f6"),
                                            padding="4",
                                            background_color="blue.50",
                                            border_radius="xl",
                                        ),
                                        rx.vstack(
                                            rx.heading("Order History", size="5", color="#111827"),
                                            rx.text("View your past orders and status.", color="gray.500", size="2"),
                                            align="start", spacing="1",
                                        ),
                                        rx.spacer(),
                                        rx.icon("chevron_right", size=20, color="gray.400"),
                                        width="100%", align="center", padding="4",
                                    ),
                                    _hover={"transform": "scale(1.02)", "box_shadow": "lg"},
                                    transition="all 0.2s",
                                    width="100%",
                                    border_radius="xl",
                                ),
                                href="/orders",
                                width="100%",
                                text_decoration="none",
                            ),
                            rx.link(
                                rx.card(
                                    rx.hstack(
                                        rx.box(
                                            rx.icon("heart", size=32, color="red.500"),
                                            padding="4",
                                            background_color="red.50",
                                            border_radius="xl",
                                        ),
                                        rx.vstack(
                                            rx.heading("Wishlist", size="5", color="#111827"),
                                            rx.text(f"You have {WishlistState.wishlist_items.length().to_string()} items saved.", color="gray.500", size="2"),
                                            align="start", spacing="1",
                                        ),
                                        rx.spacer(),
                                        rx.icon("chevron_right", size=20, color="gray.400"),
                                        width="100%", align="center", padding="4",
                                    ),
                                    _hover={"transform": "scale(1.02)", "box_shadow": "lg"},
                                    transition="all 0.2s",
                                    width="100%",
                                    border_radius="xl",
                                ),
                                href="/wishlist",
                                width="100%",
                                text_decoration="none",
                            ),
                            columns="2",
                            spacing="6",
                            width="100%",
                        ),
                        
                        # Settings Placeholder
                        rx.card(
                            rx.vstack(
                                rx.heading("Account Settings", size="5", color="#111827", margin_bottom="4"),
                                rx.grid(
                                    rx.vstack(
                                        rx.text("Personal Information", font_weight="medium"),
                                        rx.text("Update your name, email, and contact details", color="gray.500", size="2"),
                                        align="start",
                                    ),
                                    rx.vstack(
                                        rx.text("Security", font_weight="medium"),
                                        rx.text("Change your password and secure your account", color="gray.500", size="2"),
                                        align="start",
                                    ),
                                    rx.vstack(
                                        rx.text("Addresses", font_weight="medium"),
                                        rx.text("Manage your shipping and billing addresses", color="gray.500", size="2"),
                                        align="start",
                                    ),
                                    rx.vstack(
                                        rx.text("Notifications", font_weight="medium"),
                                        rx.text("Choose how we communicate with you", color="gray.500", size="2"),
                                        align="start",
                                    ),
                                    columns="2",
                                    spacing="8",
                                    width="100%",
                                ),
                                width="100%",
                                padding="8",
                                align="start",
                            ),
                            width="100%",
                            border_radius="xl",
                            margin_top="6",
                        ),
                        width="100%",
                        padding_x="8",
                    ),
                    width="100%",
                    align="start",
                ),
                max_width="1280px",
                width="100%",
                padding_x="8",
                padding_bottom="20",
            ),
            rx.center(
                rx.vstack(
                    rx.heading("Access Denied", size="7", color="#111827"),
                    rx.text("Please login to view your profile.", color="gray.600"),
                    rx.button("Login Now", on_click=rx.redirect("/login"), color_scheme="blue", size="4"),
                    spacing="6",
                    padding_y="32",
                ),
                width="100%",
            ),
        )
    )
