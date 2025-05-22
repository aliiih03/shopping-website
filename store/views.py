from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect , HttpResponse
from .forms import signUpForm, UpdateUserForm, ChangePasswordForm, UpdateInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
import json
from cart.cart import Cart


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "home.html", {"products": products, "categories": categories})


def about_page(request):
    user_profile = Profile.objects.get(user_id=request.user.id)
    old_cart = user_profile.old_cart

    return HttpResponse(f"<p>{request.session.keys()}<p/> <p> {request.session.get('cart')}</p> <p> {old_cart}</p>")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # do some carting stuff
            user_profile = Profile.objects.get(user__id=request.user.id)
            if user_profile.old_cart:
                saved_cart = user_profile.old_cart
                saved_cart = json.loads(saved_cart)
                cart = Cart(request)
                if saved_cart:
                    for key, value in saved_cart.items():
                        cart.db_add(key, value)

                messages.success(request, "you are now logged in")
                return redirect("home")
            else:
                messages.success(request, "you are now logged in")
                return redirect("home")
        else:
            messages.success(request, "User Not Exist...")
            return redirect("home")
    else:
        return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("login")


def register_user(request):
    if request.method == "GET":
        form = signUpForm()
        return render(request, "register.html", {"form": form})
    else:
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You registered now fill Your Info Bellow...")
                return redirect("update_info")
            else:
                messages.success(request, "something went wrong")
                return redirect("register")
        else:
            messages.success(request, "something went wrong")
            return redirect("register")


def product_view(request, pk):
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    return render(request, "product.html", {"product": product, "categories": categories})


def category_view(request, cat):
    cat = cat.replace("-", " ")
    category = Category.objects.get(name=cat)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    if products is not None:
        return render(request, "home.html", {"products": products, "category": cat, "categories": categories})
    else:
        messages.success(request, "there is no products")
        return redirect("home")


def update_user(request):
    form = UpdateUserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        login(request, request.user)
        messages.success(request, "Profile Updated...")
        return redirect("home")
    return render(request, "update_user.html", {"form": form})


def update_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            login(request, request.user)
            messages.success(request, "Password Changed...")
            return redirect('update_user')
        else:
            for err in list(form.errors.values()):
                messages.error(request, err)
                return redirect('update_password')
    else:
        form = ChangePasswordForm(request.user)
        return render(request, "update_password.html", {"form": form})


def update_info(request):
    profile = Profile.objects.get(user__id=request.user.id)
    user_shipping = ShippingAddress.objects.get(user__id=request.user.id)
    form = UpdateInfoForm(request.POST or None, instance=profile)
    shipping_form = ShippingForm(request.POST or None, instance=user_shipping)
    if form.is_valid() or shipping_form.is_valid():
        form.save()
        shipping_form.save()
        messages.success(request, "Your Info Updated...")
        return redirect("home")
    else:
        for err in list(form.errors.values()):
            messages.error(request, err)
            return redirect('update_info')
    return render(request, "update_info.html", {"form": form, "shipping_form": shipping_form})


def search(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        categories = Category.objects.all()
        products = Product.objects.filter(Q(name__icontains=searched) | Q(category__name__icontains=searched))
        if len(products) == 0:
            messages.success(request, "No Products Found !!!")
            return render(request, "home.html", {"products": None, "categories": categories})

        return render(request, "home.html", {"products": products, "categories": categories})
    else:
        return redirect("home")
