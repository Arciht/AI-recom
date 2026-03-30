import reflex as rx

class CartState(rx.State):
    cart_items: list[dict] = []
    total: float = 0.0

    def add_to_cart(self, product: dict):
        # Check if product already exists
        for item in self.cart_items:
            if item.get("product_id") == product.get("product_id"):
                item["quantity"] = item.get("quantity", 1) + 1
                self.calculate_total()
                return
        
        # Add new item
        product_copy = product.copy()
        product_copy["quantity"] = 1
        self.cart_items.append(product_copy)
        self.calculate_total()

    def remove_from_cart(self, product_id: str):
        self.cart_items = [item for item in self.cart_items if item.get("product_id") != product_id]
        self.calculate_total()

    def calculate_total(self):
        self.total = sum(
            float(item.get("price", 0)) * item.get("quantity", 1) 
            for item in self.cart_items
        )