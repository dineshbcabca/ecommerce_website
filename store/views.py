from django.shortcuts import get_object_or_404, render
from category.models import Category
from .models import Product
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
#from django.http import HttpResponse
from django.db.models import Q


# Create your views here.

def store(request,category_slug=None):
    categories= None
    products= None

    if category_slug != None:
        categories= get_object_or_404(Category, slug=category_slug) #secount category_slug is url, 1 nd slug is category model field name
        products=Product.objects.filter(category=categories, is_available=True)
        paginator= Paginator(products, 1)
        page     =request.GET.get('page') #url of ?page 2
        paged_products=paginator.get_page(page)
        product_count=products.count()
    
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator= Paginator(products, 3)
        page     =request.GET.get('page') #url of ?page 2
        paged_products=paginator.get_page(page)
        product_count=products.count()
    context={

        "products":paged_products,
        "product_count":product_count,
    }
    return render(request, "store/store.html", context)
    

def product_details(request, category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug, slug=product_slug) 
    # 1 st category isa category name and __slug is the category access the pariticular models table.2 nd category_slug is url in broswer++++ next product_slug is this product url in browser
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists() #_cart_id is the session key
        #the cart is the foreinkey of CartItem,the cart access by the cart_id in Cart model so we use __cart_id.
        # return HttpResponse(in_cart)
        # exit() debugging
    except Exception as e:
        raise e
    context={
        "single_product":single_product,
        "in_cart"       :in_cart,
        
    } 

    return render(request, "store/product_details.html",context)


def search(request):
    if "keyword" in request.GET:
        keyword= request.GET["keyword"]
        if keyword:
            products=Product.objects.order_by("-created_date").filter(Q(description__icontains=keyword) | Q(product_title__icontains=keyword))
            product_count=products.count()
        context={
            "products":products,
            "product_count":product_count
        }
    return render(request, "store/store.html", context)
    
