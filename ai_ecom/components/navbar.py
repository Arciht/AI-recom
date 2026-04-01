import reflex as rx
from ..state.user_state import UserState
from ..state.cart_state import CartState
from ..state.products_state import ProductsState

class NavbarState(rx.State):
    """State for navbar interactions"""
    is_menu_open: bool = False

    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open

    def handle_search(self, query: str):
        ProductsState.set_search_query(query)
        return rx.redirect("/products")

def navbar():
    return rx.box(
        rx.hstack(
            # Logo (Left)
            rx.link(
                rx.hstack(
                    rx.icon("shopping-cart", size=24, color="#3b82f6"),
                    rx.heading("AI Shop", size="6", color="#111827", font_weight="bold"),
                    spacing="2",
                ),
                href="/",
                _hover={"text_decoration": "none"},
            ),
            
            rx.spacer(),
            
            # Search bar (Center)
            rx.hstack(
                rx.input(
                    placeholder="Search products...",
                    width=["150px", "250px", "400px"],
                    size="3",
                    border_radius="full",
                    value=ProductsState.search_query,
                    on_change=ProductsState.set_search_query,
                    on_key_down=lambda e: rx.cond(e == "Enter", NavbarState.handle_search(ProductsState.search_query), rx.console_log("")),
                ),
                rx.icon("search", size=20, color="gray.500", cursor="pointer", on_click=NavbarState.handle_search(ProductsState.search_query)),
                spacing="2",
                align="center",
                display=["none", "none", "flex"],
            ),
            
            rx.spacer(),
            
            # Navigation links (Right) - Desktop
            rx.hstack(
                rx.link("Home", href="/", color="#374151", font_weight="500", _hover={"color": "#3b82f6"}),
                rx.link("Products", href="/products", color="#374151", font_weight="500", _hover={"color": "#3b82f6"}),
                rx.link("Recommendations", href="/recommendations", color="#374151", font_weight="500", _hover={"color": "#3b82f6"}),
                rx.link("Wishlist", href="/wishlist", color="#374151", font_weight="500", _hover={"color": "#3b82f6"}),
                rx.link("Orders", href="/orders", color="#374151", font_weight="500", _hover={"color": "#3b82f6"}),
                
                rx.box(width="4"), # Extra spacing
                
                # Cart Icon with badge
                rx.link(
                    rx.box(
                        rx.icon("shopping-bag", size=24, color="gray.700"),
                        rx.cond(
                            CartState.cart_items.length() > 0,
                            rx.badge(
                                CartState.cart_items.length().to_string(),
                                color_scheme="blue",
                                border_radius="full",
                                position="absolute",
                                top="-2",
                                right="-2",
                                size="1",
                            ),
                        ),
                        position="relative",
                    ),
                    href="/cart",
                    _hover={"color": "#3b82f6"},
                ),
                
                # User Menu
                rx.cond(
                    UserState.logged_in,
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.avatar(
                                fallback=UserState.user_name[:2].upper(),
                                size="3",
                                cursor="pointer",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item("Profile", on_click=rx.redirect("/profile")),
                            rx.menu.item("Orders", on_click=rx.redirect("/orders")),
                            rx.menu.item("Wishlist", on_click=rx.redirect("/wishlist")),
                            rx.menu.separator(),
                            rx.menu.item("Logout", on_click=UserState.logout, color="red"),
                        ),
                    ),
                    rx.button(
                        "Login",
                        on_click=rx.redirect("/login"),
                        color_scheme="blue",
                        size="3",
                    ),
                ),
                spacing="6",
                align="center",
                display=["none", "none", "flex"],
            ),
            
            # Mobile Hamburger
            rx.box(
                rx.icon("menu", size=24, on_click=NavbarState.toggle_menu),
                display=["block", "block", "none"],
                cursor="pointer",
            ),
            
            padding_x="8",
            padding_y="4",
            align="center",
            width="100%",
        ),
        
        # Mobile Menu
        rx.cond(
            NavbarState.is_menu_open,
            rx.vstack(
                rx.link("Home", href="/", color="gray.700", padding_y="2", width="100%"),
                rx.link("Products", href="/products", color="gray.700", padding_y="2", width="100%"),
                rx.link("Recommendations", href="/recommendations", color="gray.700", padding_y="2", width="100%"),
                rx.link("Cart", href="/cart", color="gray.700", padding_y="2", width="100%"),
                rx.cond(
                    UserState.logged_in,
                    rx.vstack(
                        rx.link("Profile", href="/profile", color="gray.700", padding_y="2", width="100%"),
                        rx.link("Logout", on_click=UserState.logout, color="red", padding_y="2", width="100%"),
                        width="100%",
                        align="start",
                    ),
                    rx.link("Login", href="/login", color="gray.700", padding_y="2", width="100%"),
                ),
                padding="4",
                background_color="white",
                border_top="1px solid #e5e7eb",
                width="100%",
                display=["flex", "flex", "none"],
                align="start",
            ),
        ),
        
        position="sticky",
        top="0",
        z_index="1000",
        background_color="white",
        border_bottom="1px solid #e5e7eb",
        width="100%",
    )
