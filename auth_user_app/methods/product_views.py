from products.models import Category, Product 
from methodism import custom_response, MESSAGE

def products_list(request, params):
    products = Product.objects.all()
    return custom_response(True, data=[product.format for product in products] if products.exists() else 'No products yet!', message='Success!')


def new_product(request, params):
    """
    Rasm qo'shish uchun hozirch imkoniyat yo'q!
    """
    fields = ['category_id', 'title', 'short_desc', 'price', 'price_type']
    for field in fields:
        if field not in params:
            return custom_response(False, data=fields, message=MESSAGE['DataNotFull'])
        
    # `category_id` bilan kategoriya tanlab olinadi yoki xatolik bo'lsa, `category_id` datada qaytariladi.
    category = Category.objects.filter(id=params['category_id']).first()
    if not category:
        return custom_response(False, data={'category_id':params['category_id']}, message=MESSAGE['NotData'])
    
    # `title` ni tekshirish
    try:
        title = str(params['title'])
        if len(title) > 200:
            raise ValueError()
    except:
        return custom_response(False, data={'title':params['title'], "valid_title": "0<len(title)<=200"}, message="Title not valid")
    
    # `short_desc` ni tekshirish
    try:
        short_desc = str(params['short_desc'])
        if len(short_desc) > 300:
            raise ValueError()
    except:
        return custom_response(False, data={'short_desc':params['short_desc'], "valid_short_desc": "0<len(short_desc)<=300"}, message="Short_desc not valid")

    # `price` ni tekshirish
    try: 
        price = float(params['price'])
        if price < 0 or price >= 100_000_000:
            raise ValueError()
    except:
        return custom_response(False, data={'price':params['price'], "valid_price": "Price must int or float and 0<price<100_000_000"}, message="Price not valid")

    # `price_type` ni tekshirish
    valid_price_type =['UZS', 'USD', 'EUR', 'RUB']
    try: 
        price_type = str(params['price_type'])
        if price_type not in valid_price_type:
            raise ValueError()
    except:
        return custom_response(False, data={'price_type':params['price_type'], "valid_price_type": valid_price_type}, message="Price_type not valid")
    
    product = Product.objects.create(
        category=category,
        user=request.user,
        title=title,
        short_desc=short_desc,
        price=price,
        price_type=price_type,
        )
    return custom_response(True, data=product.format, message='Product created!')