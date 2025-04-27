from products.models import Product, Like
from methodism import custom_response, MESSAGE

def add_remove_reaction(request, params):
    """
    Bu funksiya avval paramsning `product_id` mavjudligini, to'g'ri tartibda kiritilganligi
    va shu `id` ga ega mahsulot mavjudligini tekshirib javob yuboradi. Mavjud mahsulot(product) va 
    so'rov yuborayotgan foydalanuvchi(reqeust.user) orqali 'like` obyektini `get_or_create` metodi yordamida,
    obyekt bo'lsa undagi ma'lumotlarni yangilaydi, agar bo'lmasa uni yaratadi.

    Params orqali `product_id` bilan `like` yoki `dislike` ni har qanday qiymat bilan jo'natish mumkin.
    Agar like ham, dislike ham yuborilmasa "is_reacted"(False) xabari bilan likelar soni va dislikelar sonini ma'lumot sifatida qaytaradi,

    Agar params `like` bo'lsa product uchun like True bo'lsa False qilinadi, aks holda like True qiymatga tenglashtiriladi.
    Shu bilan birga `dislike` True qiymatga ega bo'lsa uni False qiymatga aylantiradi, False bo'lsa uni o'zgartirmaydi.

    Agar params `dislike` bo'lsa product uchun dislike True bo'lsa False qilinadi, aks holda dislike True qiymatga tenglashtiriladi.
    Shu bilan birga `like` True qiymatga ega bo'lsa uni False qiymatga aylantiradi, False bo'lsa uni o'zgartirmaydi.

    Eslatme: Agar like va dislike ham paramsda mavjud bo'lsa `dislike` hisobga olinmaydi. Yaxshi gumonda:)
    """
    if 'product_id' not in params:
        return custom_response(False, message=MESSAGE['DataNotFull'])
    
    try:
        product_id = int(params['product_id'])
    except:
        return custom_response(False, message=MESSAGE['NotData'])
    
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return custom_response(False, message=MESSAGE['NotData'])
    
    like = Like.objects.get_or_create(user=request.user, product=product)[0]
    
    if 'like' in params:
        like.like = False if like.like else True
        like.dislike = False if like.like else like.dislike
    
    elif 'dislike' in params:
        like.dislike = False if like.dislike else True
        like.like = False if like.dislike else like.like

    like.save()
    like_count = product.like_set.filter(like=True).count()
    dislike_count = product.like_set.filter(dislike=True).count()
    return custom_response(True if 'like' in params or 'dislike' in params else False, data={
        'like_count': like_count, 
        'dislike_count': dislike_count,
        ('is_liked') if 'like' in params else ('is_disliked') if 'dislike' in params else ('is_reacted'): \
            (True if like.like else False) if 'like' in params \
                else (True if like.dislike else False)  if 'dislike' in params \
                    else False,
        'like': like.like,
        'dislike': like.dislike
        }, message=('Successfully liked!' if like.like else 'Successfully unliked!') if 'like' in params \
            else ('Successfully disliked!' if like.dislike else 'Successfully undisliked!') if 'dislike' in params \
                else 'No reaction')


def get_reaction_count(request, params):
    """
    Mahsulot uchun bildirilgan reaksiyalar sonini qaytaradi.
    """
    if 'product_id' not in params:
        return custom_response(False, message=MESSAGE['DataNotFull'])
    
    try:
        product_id = int(params['product_id'])
    except:
        return custom_response(False, message=MESSAGE['NotData'])
    
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return custom_response(False, message=MESSAGE['NotData'])
    return custom_response(True, data={
        'like_count': product.like_set.filter(like=True).count(), 
        'dislike_count': product.like_set.filter(dislike=True).count()
        }, message='Success!')
