from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def home(request):
    products = Product.objects.filter(is_active=True).order_by('-created')[:5]
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
