from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from order.views import user_orders
from store.models import Product

from .forms import RegistrationForm, UserAddressForm, UserEditForm
from .models import Address, Customer
from .token import account_activation_token


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user.id)
    return render(request, 'dashboard/user_wish_list.html', {'wishlist': products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.title + " has been removed from your WishList.")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your WishList.")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'dashboard/dashboard.html', {'orders': orders})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            cd = registerForm.cleaned_data
            user.email = cd['email']
            user.set_password(cd['password'])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'registration/activation_invalid.html')


# Addresses

@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, 'dashboard/addresses.html', {'addresses': addresses})


@login_required
def add_address(request):
    if request.method == 'POST':
        form = UserAddressForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user
            form.save()
            return HttpResponseRedirect(reverse('account:addresses'))
    else:
        form = UserAddressForm()
    return render(request, 'dashboard/edit_addresses.html', {"form": form})


@login_required
def edit_address(request, id):
    if request.method == 'POST':
        address = Address.objects.get(pk=id, customer=request.user)
        form = UserAddressForm(data=request.POST, instance=address)
        if form.is_valid():
            form.save()
            HttpResponseRedirect(reverse('account:addresses'))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        form = UserAddressForm(instance=address)
    return render(request, 'dashboard/edit_addresses.html', {"form": form})


@login_required
def delete_address(request, id):
    address = Address.objects.get(pk=id, customer=request.user)
    address.delete()
    return redirect(reverse("account:addresses"))


@login_required
def set_default(request, id):
    """ set default address """
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect("account:addresses")
