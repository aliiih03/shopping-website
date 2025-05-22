from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def db_add(self, product, quan):
        product_id = str(product)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(quan)

        self.session.modified = True

        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            user_profile.update(old_cart=str(carty))

    def add(self, product, quan):

        product_id = str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(quan)

        self.session.modified = True

        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            user_profile.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def update(self, product_id, quantity):
        product_id = str(product_id)
        quan = int(quantity)
        self.cart[product_id] = quan
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            user_profile.update(old_cart=carty)
        self.session.modified = True

    def delete(self, product_id):
        product_id = str(product_id)
        del self.cart[product_id]
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            user_profile.update(old_cart=carty)
        self.session.modified = True

    def total(self):
        sum = 0
        for key, value in self.cart.items():
            product = Product.objects.get(id=key)
            if product.is_sale:
                sum += value * product.sale_price
            else:
                sum += value * product.price
        return sum
