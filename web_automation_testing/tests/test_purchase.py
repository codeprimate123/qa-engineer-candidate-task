import pytest

from classes.user import User


@pytest.mark.parametrize("saucedemo_item", [
    "Sauce Labs Backpack",
    "Sauce Labs Onesie",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
])
def test_purchase(saucedemo_site, saucedemo_item):
    """Test the login process and a simple purchase flow buying."""
    site = saucedemo_site
    user =  User(
        'standard_user',
        'John', 
        'Doe', 
        '12345'
        )
    site.login(user)
    selected_products = site.select_product(saucedemo_item)
    cart_products = site.verify_cart_products(selected_products)
    site.fill_checkout_info(user)
    site.finish_checkout(cart_products)
    site.complete_checkout()
