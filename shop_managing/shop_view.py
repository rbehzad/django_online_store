from shopping.models import *
from blog.models import Post


def shop_base(request):
    try:
        context = {
            'carts': Cart.objects.filter(shop__user=request.user, status='Paid'),
            'posts': Post.objects.filter(author=request.user),
            'tags': Tag.objects.all()
        }
        return context  
    except:
        return {}

