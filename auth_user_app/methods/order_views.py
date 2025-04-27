from products.models import Card, Order
from methodism import custom_response, error_messages, MESSAGE

def new_order(request, params):
    cards = Card.objects.filter(user=request.user, status=True)
    if not cards.exists():
        return custom_response(False, message="Savatingizda hali hech narsa yo'q!")
    
    order = Order.objects.create(user=request.user)
    order.card.set(cards)
    
    total = 0 
    for card in cards:
        total += card.product.price * card.quantity
    
    order.summa = total
    order.save()
    cards.delete()
    return custom_response(True, message="Buyurtma qabul qilindi")


def get_orders(request, params):
    orders = Order.objects.filter(user=request.user)
    if not orders.exists():
        return custom_response(False, message="Sizda hali buyurtmalar mavjud emas!")
    
    return custom_response(True, data={f"{order.created_at.date()} kundagi ${order.summa} lik buyurtma(status={order.status})!" for order in orders})


def recieve_order(request, params):
    if 'order_id' not in params:
        return custom_response(False, message=MESSAGE['DataNotFull'])
    
    order = Order.objects.filter(id=params.get('order_id')).first()
    if not order:
        return custom_response(False, message="Bunday buyurtma mavjud emas!")
    
    if order.status:
        return custom_response(False, message="Buyurtma yetkazib berilgan!")
    
    order.status = True
    order.save()
    return custom_response(True, message="Buyurtma yetkazildi")

def cancel_order(request, params):
    return custom_response(True)