import reflex as rx
import sys
from pathlib import Path

# Add the project root to sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from ai_ecom.state.user_state import UserState
from ai_ecom.state.cart_state import CartState, WishlistState
from ai_ecom.state.recommendation_state import RecommendationState
from ai_ecom.state.products_state import ProductsState, ProductDetailState

# Import pages
from ai_ecom.pages.index import index
from ai_ecom.pages.login import login_page
from ai_ecom.pages.signup import signup_page
from ai_ecom.pages.products import products_page
from ai_ecom.pages.product_details import product_detail_page
from ai_ecom.pages.recommendations import recommendations_page
from ai_ecom.pages.cart import cart_page
from ai_ecom.pages.checkout import checkout_page
from ai_ecom.pages.payment import payment_page
from ai_ecom.pages.payment_success import payment_success_page
from ai_ecom.pages.wishlist import wishlist_page
from ai_ecom.pages.orders import orders_page
from ai_ecom.pages.profile import profile_page

# Create the app
app = rx.App(
    theme=rx.theme(
        accent_color="blue",
        radius="large",
        appearance="light",
    ),
    style={
        "font_family": "Inter, sans-serif",
        "background_color": "#ffffff",
        "color": "#111827", # Default text color (almost black)
        "font_size": "16px", # Balanced base font size
    }
)

# Register pages
app.add_page(index, route="/", title="AI Shop - Home", on_load=[ProductsState.load_all_products, RecommendationState.load_recommendations])
app.add_page(login_page, route="/login", title="Login - AI Shop")
app.add_page(signup_page, route="/signup", title="Sign Up - AI Shop")
app.add_page(products_page, route="/products", title="All Products", on_load=ProductsState.load_all_products)
app.add_page(product_detail_page, route="/product/[product_id]", title="Product Detail", on_load=[ProductDetailState.load_product, ProductsState.load_all_products])
app.add_page(recommendations_page, route="/recommendations", title="Recommended For You", on_load=RecommendationState.load_recommendations)
app.add_page(cart_page, route="/cart", title="Shopping Cart")
app.add_page(checkout_page, route="/checkout", title="Checkout")
app.add_page(payment_page, route="/payment", title="Payment")
app.add_page(payment_success_page, route="/payment-success", title="Success - AI Shop")
app.add_page(wishlist_page, route="/wishlist", title="My Wishlist")
app.add_page(orders_page, route="/orders", title="My Orders")
app.add_page(profile_page, route="/profile", title="My Profile")
