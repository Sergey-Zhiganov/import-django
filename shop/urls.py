from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'api/categories', CategoryViewSet)
router.register(r'api/tags', TagViewSet)
router.register(r'api/products', ProductViewSet)
router.register(r'api/orders', OrderViewSet)
router.register(r'api/order-items', OrderItemViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/add', add_product, name='add_product'),
    path('catalog/<int:product_id>/', product_detail, name='product_detail'),
    path('catalog/<int:product_id>/edit', edit_product, name='edit_product'),
    path('catalog/<int:product_id>/delete', delete_product, name='delete_product'),
    path('categories/', categories, name='categories'),
    path('categories/<int:category_id>/products/', products_by_category, name='products_by_category'),
    path('categories/add', add_category, name='add_category'),
    path('tags/', tags, name='tags'),
    path('contact/', contact, name='contact'),
    path('profile/', profile, name='profile'),
    path('cart/', cart, name='cart'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/decrease/<int:product_id>/', cart_descrease, name='cart_descrease'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)