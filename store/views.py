from django.shortcuts import render

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
    context = {'products': products}

    return render(request, 'shop.html', context)


def about(requests):
    return render(requests, 'about.html')


def contact(requests):
    return render(requests, 'contact.html')
