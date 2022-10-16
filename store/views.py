from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
    # products = Product.objects.all().order_by('-created')[:5]
    # context = {'products': products}
    return render(request, 'home.html')


def shop(request):
    """
    all_products
    """
    products = Product.objects.all()
    context = {'products': products
               }

    return render(request, 'shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    context = {'product': product
               }
    return render(request, 'shop-single.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    context = {'category': category,
               'products': products
               }
    return render(request, 'category.html', context)
