from typing import List, Optional, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver, WebElement

from classes.user import User
from classes.product import Product



class SauceDemoSite:
    def __init__(
            self, 
            driver: WebDriver
            ):
        self.driver = driver

    def veryify_page(
            self, 
            expected_url: str
            ) -> None:
        
        assert self.driver.current_url == expected_url, f"Actual URL: {self.driver.current_url}"

    def find_element_by_data_test(
            self, 
            data_test: str, 
            tag: str = '*', 
            parent: Optional[WebElement] = None
            ) -> WebElement:
        
        if parent is not None:
            xpath = f'.//{tag}[@data-test="{data_test}"]'
        else:
            parent = self.driver
            xpath = f'//{tag}[@data-test="{data_test}"]'
        
        return WebDriverWait(parent, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))


    def find_all_elements_by_data_test(
            self, 
            data_test: str, 
            tag: str = '*', 
            parent: Optional[WebElement] = None
            ) -> List[WebElement]:
        
        if parent is not None:
            xpath = f'.//{tag}[@data-test="{data_test}"]'
        else:
            parent = self.driver
            xpath = f'//{tag}[@data-test="{data_test}"]'

        return WebDriverWait(parent, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))


    def get_text(
            self, 
            data_test: str, 
            tag: str = '*'
            ) -> str:
        
        element = self.find_element_by_data_test(data_test, tag)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(element)
        )
        return element.text


    def fill_input(
            self, 
            data_test: str, 
            value: str, 
            tag: str = 'input'
            ) -> None:
        
        element = self.find_element_by_data_test(data_test, tag)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(element)
        )
        element.send_keys(value)


    def click_button_by_data_test(
            self, 
            data_test: str, 
            tag: str
            ) -> None:
        
        element = self.find_element_by_data_test(data_test, tag)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(element)
        )
        element.click()


    def get_elements_by_text(
            self, 
            text: str, 
            tag: str = '*', 
            parent: Optional[WebElement] = None
            ) -> List[WebElement]:
        
        if parent is not None:
            xpath = f'.//{tag}[text()="{text}"]'
        else:
            parent = self.driver
            xpath = f'//{tag}[text()="{text}"]'
        
        return WebDriverWait(parent, 10).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))


    def click_button_by_text(
            self, 
            text: str, 
            tag: str, 
            parent: Optional[WebElement] = None
            ) -> None:
        
        elements = self.get_elements_by_text(text=text, tag=tag, parent=parent)
        if not elements:
            raise ValueError(f"No button with text {text} was found")
        if len(elements) > 1:
            raise ValueError(f"Multiple buttons with text {text} were found")
        else:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(elements[0]))
            elements[0].click()


    def fill_username(
            self, 
            user: User
            ) -> None:
        
        self.fill_input('username', user.username, tag='input')


    def get_password_from_page(self) -> str:

        password_div = self.find_element_by_data_test('login-password', tag='div')
        all_text = password_div.text
        h4_text = ""
        h4_elements = password_div.find_elements(By.TAG_NAME, 'h4')
        if h4_elements:
            h4_text = h4_elements[0].text
        password_text = all_text.replace(h4_text, "").strip()
        return password_text


    def fill_password(self) -> None:

        password = self.get_password_from_page()
        self.fill_input('password', password, tag='input')


    def login(
            self, 
            user: User
            ) -> None:
        
        self.fill_username(user)
        self.fill_password()
        self.click_button_by_data_test('login-button', tag='input')


    def select_product(
            self, 
            items: Union[str, List[str]]
            ) -> List[Product]:
        
        item_elements = self.find_all_elements_by_data_test('inventory-item', tag='div')
        items = [item.lower() for item in items] if isinstance(items, list) else [items.lower()]
        products = []
        for element in item_elements:
            item_name = self.find_element_by_data_test('inventory-item-name', tag='div', parent=element).text.strip()
            if item_name.lower() in items:
                self.click_button_by_text('Add to cart', tag='button', parent=element)
                item_description = self.find_element_by_data_test('inventory-item-desc', tag='div', parent=element).text.strip()
                try:
                    item_price = float(self.find_element_by_data_test('inventory-item-price', tag='div', parent=element).text.strip().replace('$', ''))
                except ValueError:
                    item_price = self.find_element_by_data_test('inventory-item-price', tag='div', parent=element).text.strip().replace('$', '')
                
                product = Product(
                    label=item_name,
                    description=item_description,
                    price=item_price,
                    quantity=1
                )
                products.append(product)

        return products
    

    def enumerate_cart_items(
            self, 
            cart: WebElement
            ) -> List[Product]:
        
        cart_items = self.find_all_elements_by_data_test('inventory-item', tag='div', parent=cart)
        products = []
        for item in cart_items:
            item_name = self.find_element_by_data_test('inventory-item-name', tag='div', parent=item).text.strip()
            item_description = self.find_element_by_data_test('inventory-item-desc', tag='div', parent=item).text.strip()
            try:
                item_price = float(self.find_element_by_data_test('inventory-item-price', tag='div', parent=item).text.strip().replace('$', ''))
            except ValueError:
                item_price = self.find_element_by_data_test('inventory-item-price', tag='div', parent=item).text.strip().replace('$', '')
            # try:
            #     item_quantity = int(self.find_element_by_data_test('cart_quantity', tag='div', parent=item).text.strip())
            # except ValueError:
            #     item_quantity = self.find_element_by_data_test('cart_quantity', tag='div', parent=item).text.strip()
            
            product = Product(
                label=item_name,
                description=item_description,
                price=item_price,
                quantity=1,
            )
            products.append(product)
        
        return products


    def check_cart(
            self, 
            ) -> List[Product]:

        self.click_button_by_data_test('shopping-cart-link', tag='a')
        self.veryify_page('https://www.saucedemo.com/cart.html')
        cart = self.find_element_by_data_test('cart-list', tag='div')
        cart_items = self.enumerate_cart_items(cart)
        self.click_button_by_data_test('checkout', tag='button')
        return cart_items
    

    def check_checkout(self) -> List[Product]:
            
        self.veryify_page('https://www.saucedemo.com/checkout-step-two.html')
        cart = self.find_element_by_data_test('cart-list', tag='div')
        checkout = self.find_element_by_data_test('checkout-summary-container', tag='div')
        checkout_cart = self.find_element_by_data_test('cart-list', tag='div', parent=checkout)
        checkout_cart_items = self.enumerate_cart_items(cart)
        return checkout_cart_items
    

    def compare_carts(
            self, 
            cart_products: List[Product], 
            selected_products: List[Product]
            ) -> bool:
        
        assert len(cart_products) == len(selected_products), "Different number of products selected and in cart"
        sorted_cart_products = sorted(cart_products, key=lambda product: product.label)
        sorted_selected_products = sorted(selected_products, key=lambda product: product.label)
        for cart_product, selected_product in zip(sorted_cart_products, sorted_selected_products):
            assert cart_product.label == selected_product.label
            assert cart_product.description == selected_product.description
            assert cart_product.price == selected_product.price
            assert cart_product.quantity == selected_product.quantity # we are only getting one product in current implementation,
                                                                    # otherwise cart could have more than one product
        return True
    

    def verify_cart_products(
            self,
            selected_products: List[Product]
            ) -> List[Product]:
        
        cart_products = self.check_cart()
        assert self.compare_carts(cart_products, selected_products)
        return cart_products


    def fill_checkout_info(
            self, 
            user: User
            ) -> None:
        
        self.fill_input('firstName', user.first_name)
        self.fill_input('lastName', user.last_name)
        self.fill_input('postalCode', user.zip_code)
        self.click_button_by_data_test('continue', tag='input')


    def verify_checkout_products(
            self, 
            selected_products: List[Product]
            ) -> None:
        
        checkout_products = self.check_checkout()
        assert self.compare_carts(checkout_products, selected_products)
        return checkout_products


    def finish_checkout(self, selected_products: List[Product]) -> None:

        self.veryify_page('https://www.saucedemo.com/checkout-step-two.html')
        self.verify_checkout_products(selected_products)
        self.click_button_by_data_test('finish', tag='button')


    def complete_checkout(self) -> None:

        self.veryify_page('https://www.saucedemo.com/checkout-complete.html')
