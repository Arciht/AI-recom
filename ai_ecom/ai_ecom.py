import reflex as rx
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from pages.login import login_page
from pages.signup import signup_page
from pages.index import index
from pages.products import products_page
from pages.recommendations import recommendations_page
from pages.product_details import product_detail_page
from pages.cart import cart_page
from pages.checkout import checkout_page
from pages.profile import profile_page

from components.navbar import navbar

from state.user_state import UserState
from state.cart_state import CartState
from state.recommendation_state import RecommendationState
from state.products_state import ProductsState


def base_template(content: rx.Component):
    return rx.vstack(
        navbar(),
        rx.box(
            content,
            width="100%",
            min_height="calc(100vh - 70px)",
            padding="1.5em",
        ),
        width="100%",
        spacing="0",
    )


app = rx.App(
    theme=rx.theme(
        accent_color="indigo",
        radius="large",
    )
)

# ====================== Register Pages ======================
app.add_page(lambda: base_template(index()), route="/", title="AI Shop - Home")
app.add_page(login_page, route="/login", title="Login - AI Shop")
app.add_page(signup_page, route="/signup", title="Sign Up - AI Shop")
app.add_page(lambda: base_template(products_page()), route="/products", title="All Products")
app.add_page(lambda: base_template(recommendations_page()), route="/recommendations", title="Recommendations")
app.add_page(lambda: base_template(cart_page()), route="/cart", title="Your Cart")
app.add_page(product_detail_page, route="/product/[product_id]", title="Product Detail")
app.add_page(checkout_page, route="/checkout", title="Checkout")

if __name__ == "__main__":
    app.run()