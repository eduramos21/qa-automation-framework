from playwright.sync_api import Locator, Page


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title: Locator = page.get_by_text("Products", exact=True)
        self.items: Locator = page.locator(".inventory_item")
        self.cart_badge: Locator = page.locator(".shopping_cart_badge")

    def goto(self) -> None:
        self.page.goto("/inventory.html")

    def item(self, name: str) -> Locator:
        """The card for one product, so actions stay scoped to it."""
        return self.items.filter(has_text=name)

    def add_to_cart(self, name: str) -> None:
        self.item(name).get_by_role("button", name="Add to cart").click()
