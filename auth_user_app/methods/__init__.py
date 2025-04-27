from .auth_views import register, login, first_step_auth, second_step_auth, logout,  get_profile, update_profile, delete_user, change_password
from .product_views import products_list, new_product
from .card_views import new_card, get_cards, delete_product_from_card, delete_cards
from .order_views import new_order, get_orders, recieve_order, cancel_order
from .like_views import add_remove_reaction, get_reaction_count