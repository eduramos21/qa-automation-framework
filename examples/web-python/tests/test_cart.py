"""Cart. These need a session, so they take signed_in_page from conftest."""

from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage


def test_adding_an_item_shows_a_count_of_one_on_the_cart(signed_in_page: Page) -> None:
    inventory = InventoryPage(signed_in_page)
    inventory.goto()

    expect(inventory.cart_badge).to_have_count(0)

    inventory.add_to_cart("Sauce Labs Backpack")

    expect(inventory.cart_badge).to_have_text("1")


def test_adding_a_second_item_raises_the_count_to_two(signed_in_page: Page) -> None:
    inventory = InventoryPage(signed_in_page)
    inventory.goto()

    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.add_to_cart("Sauce Labs Bike Light")

    expect(inventory.cart_badge).to_have_text("2")
