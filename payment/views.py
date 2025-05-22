from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import ShippingAddress
from django.forms.models import model_to_dict
from django.contrib import messages
from .forms import PaymentForm
from .models import Order, OrderItem, ShippingAddress
from store.models import Profile
import datetime

# Create your views here.
def checkout(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        products = cart.get_products()
        orders = cart.cart
        total = cart.total()
        shipping_address = ShippingAddress.objects.get(user__id=request.user.id)
        ship_add = model_to_dict(shipping_address)
        payment_form = PaymentForm()
        return render(request, 'checkout.html',
                      {"products": products, "orders": orders, "total": total, "shipping_add": ship_add,
                       "payment_form": payment_form})
    else:
        messages.success(request, "Access denied Login First...")
        return redirect("home")


def process_order(request):
    # Get the Cart
    cart = Cart(request)

    # Get billing information
    # payment_form = PaymentForm(request.POST or None)

    # Get shipping session data
    my_shipping = ShippingAddress.objects.get(user__id=request.user.id)

    # Gather order information
    full_name = my_shipping.shipping_fullname
    email = my_shipping.shipping_email

    # create shipping address from session info
    shipping_address = f"{my_shipping.shipping_address1}\n{my_shipping.shipping_address2}\n{my_shipping.shipping_city}, {my_shipping.shipping_state},{my_shipping.shipping_country}"
    amount_paid = cart.total()
    # Create an Order
    if request.user.is_authenticated:
        # Logged in
        user = request.user
        # Create order
        create_order = Order(
            user=user,
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=amount_paid,

        )
        create_order.save()

        # Add order items
        # Get the order ID
        order_id = create_order.pk
        products = cart.get_products()
        # Get product info
        for product in products:

            # Get product ID
            product_id = product.id
            # Get product price
            if product.is_sale:
                price = product.sale_price
            else:
                price = product.price
            # Get quantity
            for key, value in cart.cart.items():
                # print(key, value)
                if int(key) == product.id:
                    # Create order item
                    create_order_item = OrderItem(
                        order_id=order_id,
                        product_id=product_id,
                        user=user,
                        quantity=value,
                        price=price,
                    )
                    create_order_item.save()
        del request.session["cart"]
        request.session.modified = True

        current_user = Profile.objects.filter(user__id=request.user.id)
        current_user.update(old_cart="")


        messages.success(request, "Order Made Successfully")
        return redirect("home")
    else:
        messages.success(request, "Login First")
        return redirect("home")


def not_shipped_order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, "not_shipped_order.html", {"orders": orders})
    else:
        messages.success(request, "access denied")
        return redirect("home")


def shipped_order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, "shipped_order.html", {"orders": orders})
    else:
        messages.success(request, "access denied")
        return redirect("home")


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order__id=pk)
        if request.POST:
            status = request.POST["shipping_status"]
            # Check if true or false
            if status == "true":
                # get the order
                order = Order.objects.filter(id=pk)
                # Update the status and date shipped
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
                orders = Order.objects.filter(shipped=False)
                messages.success(request, "Shipping status updated!")
                return render(request, "not_shipped_order.html", {"orders": orders, "items": items})
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=False)
                orders = Order.objects.filter(shipped=True)
                messages.success(request, "Shipping status updated!")
                return render(request, "shipped_order.html", {"orders": orders, "items": items})

        context = {"order": order, "items": items}
        return render(request, "orders.html", context)
    else:
        messages.warning(request, "Access Denied!")
        return redirect("home")
