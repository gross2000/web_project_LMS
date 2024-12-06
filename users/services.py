import stripe
from config.settings import STRIPE_API_KEY

# STRIPE_API_KEY
stripe.api_key = "django-insecure-p!q_@pd_-lypq=i2s-b&tivtp*p79&34q=dfw26rz#6#k$lcjc"


def create_stripe_product(instance):
    """Создаем stripe продукт"""

    title_product = (f"{instance.paid_course}" if instance.paid_course else f"{instance.paid_lesson}")
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.get("id")


def create_stripe_price(stripe_product_id, amount):
    """ Создает цену в страйпе """

    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=stripe_product_id,)


def create_stripe_session(price):
    """ Создает сессию на оплату в страйп """

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')