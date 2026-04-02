import reflex as rx

class CartState(rx.State):
    cart_items: list[dict] = rx.LocalStorage([], name="cart_items_v4")
    total: float = rx.LocalStorage(0.0, name="cart_total_v4")

    @rx.var
    def total_items(self) -> int:
        """Calculate total number of items in cart (sum of quantities)"""
        count = 0
        for item in self.cart_items:
            if isinstance(item, dict):
                count += int(item.get("quantity", 1))
        return count

    def add_to_cart(self, product: dict):
        if not isinstance(product, dict):
            return rx.toast("Error adding to cart", color_scheme="red")
            
        # Check if product already exists
        new_cart = []
        found = False
        for item in self.cart_items:
            if not isinstance(item, dict):
                continue
                
            if str(item.get("product_id")) == str(product.get("product_id")):
                item_copy = item.copy()
                item_copy["quantity"] = int(item_copy.get("quantity", 1)) + 1
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
        return rx.toast(f"Added {product.get('product_name', 'item')} to cart!")

    def remove_from_cart(self, product_id: str):
        self.cart_items = [item for item in self.cart_items if isinstance(item, dict) and str(item.get("product_id")) != str(product_id)]
        self.calculate_total()

    def update_quantity(self, product_id: str, delta: int):
        new_cart = []
        for item in self.cart_items:
            if isinstance(item, dict) and str(item.get("product_id")) == str(product_id):
                item_copy = item.copy()
                new_qty = int(item_copy.get("quantity", 1)) + delta
                if new_qty > 0:
                    item_copy["quantity"] = new_qty
                    new_cart.append(item_copy)
            else:
                new_cart.append(item)
        self.cart_items = new_cart
        self.calculate_total()

    def clear_cart(self):
        self.cart_items = []
        self.total = 0.0

    def calculate_total(self):
        total_val = 0.0
        for item in self.cart_items:
            if isinstance(item, dict):
                try:
                    price = float(item.get("price", 0))
                    qty = int(item.get("quantity", 1))
                    total_val += price * qty
                except (ValueError, TypeError):
                    continue
        self.total = float(total_val)

class WishlistState(rx.State):
    wishlist_items: list[dict] = rx.LocalStorage([], name="wishlist_items_v4")

    def toggle_wishlist(self, product: dict):
        if not isinstance(product, dict):
            return rx.toast("Error: Invalid product data", color_scheme="red")

        product_id = str(product.get("product_id"))
        if any(isinstance(item, dict) and str(item.get("product_id")) == product_id for item in self.wishlist_items):
            self.wishlist_items = [item for item in self.wishlist_items if isinstance(item, dict) and str(item.get("product_id")) != product_id]
            return rx.toast("Removed from wishlist")
        else:
            self.wishlist_items.append(product)
            return rx.toast("Added to wishlist")

    def remove_from_wishlist(self, product_id: str):
        self.wishlist_items = [item for item in self.wishlist_items if isinstance(item, dict) and str(item.get("product_id")) != str(product_id)]
