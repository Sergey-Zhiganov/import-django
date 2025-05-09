from decimal import Decimal
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from shop.forms import CategoryForm, ProductForm
from .models import Category, Product, Tag
from .serializers import *

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

# Create your views here.
def home(request: HttpRequest):
    return render(request, 'home.html')

def catalog(request: HttpRequest):
    products = Product.objects.filter(is_deleted=False)
    return render(request, 'catalog.html', {'products': products})

@permission_required('shop.add_product', raise_exception=True)
@login_required
def add_product(request: HttpRequest):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

def product_detail(request: HttpRequest, product_id: int):
    product = Product.objects.filter(id=product_id, is_deleted=False).first()

    return render(request, 'product_detail.html', {'product': product})

@permission_required('shop.change_product', raise_exception=True)
@login_required
def edit_product(request: HttpRequest, product_id: int):
    product = Product.objects.filter(id=product_id, is_deleted=False).first()

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'product': product, 'form': form})

@permission_required('shop.delete_product', raise_exception=True)
@login_required
def delete_product(request: HttpRequest, product_id: int):
    product = Product.objects.filter(id=product_id, is_deleted=False).first()

    if request.method == 'POST':
        product.is_deleted = True

    return redirect('catalog')

def categories(request: HttpRequest):
    categories_list = Category.objects.all()

    return render(request, 'categories.html', {'categories': categories_list})

def products_by_category(request: HttpRequest, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    
    products = Product.objects.filter(category=category)

    return render(request, 'products_by_category.html', {'category': category, 'products': products})

def add_category(request: HttpRequest):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

def tags(request: HttpRequest):
    tags_list = Tag.objects.all()

    return render(request, 'tags.html', {'tags': tags_list})

def contact(request: HttpRequest):
    return render(request, 'contact.html')

@login_required
def profile(request: HttpRequest):
    return render(request, 'profile.html')

def cart(request: HttpRequest):
    cart: dict = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')

    item: dict
    for product_id, item in cart.items():
        product = Product.objects.filter(id=product_id, is_deleted=False).first()

        if not product:
            continue

        quantity = item['quantity']
        discount = item.get('discount', 0)

        item_total = quantity * product.price * (Decimal('1') - Decimal(discount) / Decimal('100'))
        total_price += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'discount': discount,
            'total': item_total,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': round(total_price, 2),
    })

def cart_add(request: HttpRequest, product_id: int):
    product = Product.objects.filter(id=product_id, is_deleted=False).first()

    if not product:
        return Http404('Товар не найден')

    cart: dict = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'quantity': 1,
            'discount': 0
        }

    request.session['cart'] = cart

    return redirect('cart')

def cart_descrease(request: HttpRequest, product_id: int):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if cart[str(product_id)]['quantity'] > 1:
            cart[str(product_id)]['quantity'] -= 1
        else:
            del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')

def cart_remove(request: HttpRequest, product_id: int):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')

def cart_clear(request: HttpRequest):
    request.session['cart'] = {}
    return redirect('cart')