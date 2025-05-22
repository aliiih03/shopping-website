from django.shortcuts import render, get_object_or_404, redirect , HttpResponse
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def summary(request):
    cart = Cart(request)
    products = cart.get_products()
    orders = cart.cart
    total = cart.total()
    return render(request, 'cart.html', {"products": products , "orders": orders , "total": total})





def add(request):
    cart = Cart(request)
    if request.POST.get("action") == 'post':
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quan=product_qty)

        cart_q = cart.__len__()
        response = JsonResponse({"product name": product.name, "quantity": cart_q})
        messages.success(request, "Item Added To The Cart...")
        return response


def update(request):

    cart = Cart(request)
    if request.POST.get("action") == 'post':
        product_id = int(request.POST.get("product_id"))
        product_quantity= int(request.POST.get("product_qty"))
        cart.update(product_id=product_id , quantity=product_quantity)
        response = JsonResponse({f"{{product_id}}": product_quantity})
        messages.success(request, "Item Updated...")
        return response
def delete(request):
    cart = Cart(request)
    if request.POST.get("action") == 'post':
        product_id = int(request.POST.get("product_id"))
        cart.delete(product_id=product_id)
        response = JsonResponse({f"{{product_id}}": "deleted"})
        messages.success(request, "Item deleted...")
        return response
