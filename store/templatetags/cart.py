from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    if str(product) in keys:
        return True
    return False

@register.filter(name='count_quantity')
def count_quantity(product, cart):
    keys = cart.keys()
    for key in keys:
        if key == str(product.id):
            quantity = cart.get(key)
            return quantity
    return 0

@register.filter(name="total_price")
def total_price(product, cart):
    return product.price * count_quantity(product, cart)

@register.filter(name="total_cart_price")
def total_cart_price(products, cart):
    total = 0
    keys = cart.keys()
    for product in products:
        total += total_price(product, cart)
    return total

@register.filter(name="total_order_price")
def toatl_order_price(quantity, price):
    return quantity * price

# for qty to evaluate the product quantity using tempalte
@register.filter(name='qty_calculate')
def qty_calculate(product, cart):
    keys = cart.keys()
    if str(product.id) in keys:
        return cart.get(str(product.id))
    return 0

# subtracting two variable
@register.filter(name="subtract")
def subtract(val1, val2):
    return val1 - val2

# compare product in cart quantity and store quantity
@register.filter(name="compare_cart_and_qty")
def compare_cart_and_qty(product, cart):
    keys = cart.keys()
    # print("0" * 30)
    # print(cart.get(str(product.id)))
    if str(product.id) in keys:
        if product.qty == cart.get(str(product.id)):
            return True
    return False
