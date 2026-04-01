import reflex as rx

class CartState(rx.State):
    cart_items: list[dict] = []
    total: float = 0.0

    def add_to_cart(self, product: dict):
        # Check if product already exists
        new_cart = []
        found = False
        for item in self.cart_items:
            if str(item.get("product_id")) == str(product.get("product_id")):
                item_copy = item.copy()
                item_copy["quantity"] = item_copy.get("quantity", 1) + 1
                new_cart.append(item_copy)
                found = True
            else:
                new_cart.append(item)
        
        if not found:
            # Add new item
            product_copy = product.copy()
            product_copy["quantity"] = 1
            new_cart.append(product_copy)
        
        self.cart_items = new_cart
        self.calculate_total()
        return rx.toast(f"Added {product.get('product_name')} to cart!")

    def remove_from_cart(self, product_id: str):
        self.cart_items = [item for item in self.cart_items if str(item.get("product_id")) != str(product_id)]
        self.calculate_total()

    def clear_cart(self):
        self.cart_items = []
        self.total = 0.0

    def calculate_total(self):
        self.total = sum(
            float(item.get("price", 0)) * item.get("quantity", 1) 
            for item in self.cart_items
        )

class WishlistState(rx.State):
    wishlist_items: list[dict] = []

    def toggle_wishlist(self, product: dict):
        product_id = str(product.get("product_id"))
        if any(str(item.get("product_id")) == product_id for item in self.wishlist_items):
            self.wishlist_items = [item for item in self.wishlist_items if str(item.get("product_id")) != product_id]
            return rx.toast("Removed from wishlist")
        else:
            self.wishlist_items.append(product)
            return rx.toast("Added to wishlist")

    def remove_from_wishlist(self, product_id: str):
        self.wishlist_items = [item for item in self.wishlist_items if str(item.get("product_id")) != str(product_id)]
