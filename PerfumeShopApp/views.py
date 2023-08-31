from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductForm
from .models import Product, Cart, CartItem, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Product
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from .forms import ProductForm


# Create your views here.

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)

    cart_items_data = request.session.get('cart_items', {})
    if str(product_id) in cart_items_data:
        cart_items_data[str(product_id)]['quantity'] += 1
    else:
        cart_items_data[str(product_id)] = {'quantity': 1, 'price': float(product.price)}

    request.session['cart_items'] = cart_items_data

    return redirect('cart_view')  # Redirect to cart view

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('shop:view_cart')


def index(request):
    categories = Category.objects.all()
    show_add_product_button = request.user.is_authenticated and request.user.is_staff

    print(f"User: {request.user}")
    print(f"Is Authenticated: {request.user.is_authenticated}")
    print(f"Is Staff: {request.user.is_staff}")
    print(f"Redirect URL: {reverse('add_product')}")  # Check the URL

    context = {
        'categories': categories,
        'show_add_product_button': show_add_product_button
    }
    return render(request, 'index.html', context)
def category_products(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    # category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    context = {"category": category, "products": products}
    return render(request, "category_products.html", context)

def order_success_view(request):
    # Display order success information
    return render(request, "order_success_view.html")

def checkout_view(request):
    if request.method == "POST":

        request.session.pop('cart_items', None)

        return render(request, "order_success_view.html")
    else:
        cart_items_data = request.session.get('cart_items', {})
        cart_item_ids = cart_items_data.keys()
        cart_items = Product.objects.filter(id__in=cart_item_ids)

        total_price = sum(item['price'] * item['quantity'] for item in cart_items_data.values())

        context = {
            "cart_items": cart_items,
            "total_price": total_price
        }

        return render(request, "checkout_view.html", context)


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}
    return render(request, "product_details.html", context)

def cart_view(request):
    cart_items_data = request.session.get('cart_items', {})
    print(cart_items_data)  # Check the session data in the console

    cart_items = []
    total_price = 0

    product_ids = cart_items_data.keys()
    products = Product.objects.filter(id__in=product_ids)

    for product in products:
        quantity = cart_items_data[str(product.id)]['quantity']
        price = cart_items_data[str(product.id)]['price']
        total_price += quantity * price
        cart_items.append({'product': product, 'quantity': quantity, 'price': price})

    context = {
        "cart_items": cart_items,
        "total_price": total_price
    }

    return render(request, 'cart_view.html', context)

def order_success_view(request):
    # Display order success information
    return render(request, "order_success_view.html")

def update_quantity_view(request, product_id):
    if request.method == 'POST':
        cart_items_data = request.session.get('cart_items', {})

        if str(product_id) in cart_items_data:
            action = request.POST.get('action')
            cart_item = cart_items_data[str(product_id)]

            if action == 'increase':
                cart_item['quantity'] += 1
            elif action == 'decrease':
                if cart_item['quantity'] > 1:
                    cart_item['quantity'] -= 1
                else:
                    # Remove the product from the cart if quantity becomes 0
                    del cart_items_data[str(product_id)]

            request.session['cart_items'] = cart_items_data

    return redirect('cart_view')

def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print(request.POST)  # Print POST data
        print(request.FILES)  # Print uploaded files
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


class AddProductView(View):
    template_name = 'add_product.html'

    @method_decorator(login_required)
    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Save the product
            return redirect('index')  # Redirect to the home page
        return render(request, self.template_name, {'form': form})