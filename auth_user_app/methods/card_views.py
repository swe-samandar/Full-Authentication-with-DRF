from products.models import Product, Card
from methodism import custom_response, error_messages, MESSAGE
import time

def new_card(request, params):
    if 'product_id' not in params:
        return custom_response(False, message=MESSAGE['DataNotFull'])

    try:
        quantity = int(params['quantity'])
    except:
        quantity = 1
    
    product = Product.objects.filter(id=params.get('product_id')).first()
    if not product:
        return custom_response(False, message=MESSAGE['NotData'])

    card, is_created = Card.objects.get_or_create(user=request.user, product=product)
    if is_created:
        card.quantity = quantity
    else:
        card.quantity += quantity
    card.save()
    
    return custom_response(True, data=card.format, message=f"{product.title} savatga qo'shildi!")


def get_cards(request, params):
    cards = Card.objects.filter(user=request.user)
    if not cards.exists():
        return custom_response(False, message="Savatingiz bo'sh!")
    
    return custom_response(True, data=[card.format for card in cards], message="Savatingizdagi jami mahsulotlar!")


def delete_product_from_card(request, params):
    if 'product_id' not in params:
        return custom_response(False, message=MESSAGE['DataNotFull'])
    
    product = Product.objects.filter(id=params.get('product_id')).first()
    if not product:
        return custom_response(False, message=MESSAGE['NotData'])
    
    try:
        quantity = int(params['quantity'])
        if not quantity:
            return custom_response(False, message="Siz savatdan bir dona ham {}ni olib tashlashni xohlamaysizmi?".format(product.title))
    except:
        quantity = 1

    card = Card.objects.filter(user=request.user, product=product).first()
    if not card:
        return custom_response(False, message="Siz {}ni savatga qo'shmagansiz".format(product.title))
    
    if quantity < card.quantity:
        card.quantity -= quantity
        card.save()
        return custom_response(True, data=card.format, message=f"Savatdan {quantity} dona {card.product.title} olib tashlandi!")
    
    card.delete()
    return custom_response(True, message="Savat butunlay o'chirib yuborildi!")


def delete_cards(request, params):
    cards = Card.objects.filter(user=request.user)
    if not cards.exists():
        return custom_response(False, message=MESSAGE['NotData'])
    
    cards.delete()
    return custom_response(True, message="Savatingiz tozalandi!")
