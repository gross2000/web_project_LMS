import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY



def create_stripe_product(product_name):
    """Создаем stripe продукт"""
    stripe_product = stripe.Product.create(name=product_name)
    return stripe_product



def create_stripe_price(product, payment_sum):
    """ Создает цену в страйпе """

    return stripe.Price.create(
        product=product.get('id'),
        currency="usd",
        unit_amount=payment_sum * 100
    )


def create_stripe_session(price):
    """ Создает сессию На оплату в страйпе """

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')