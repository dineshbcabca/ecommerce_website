from django.shortcuts import get_object_or_404, render
from category.models import Category
from .models import Product


# Create your views here.

def store(request,category_slug=None):
    categories= None
    products= None

    if category_slug != None:
        categories= get_object_or_404(Category, slug=category_slug) #secount category_slug is url, 1 nd slug is category model field name
        products=Product.objects.filter(category=categories, is_available=True)
        product_count=products.count()
    
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count=products.count()
    context={

        "products":products,
        "product_count":product_count,
    }
    return render(request, "store/store.html", context)
    

def product_details(request, category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug, slug=product_slug) 
    # 1 st category isa category name and __slug is the category access the pariticular models table.2 nd category_slug is url in broswer++++ next product_slug is this product url in browser
    except Exception as e:
        raise e
    context={
        "single_product":single_product,
        
    } 

    return render(request, "store/product_details.html",context)
    
