from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Category, Tag, Product, Order, OrderItem

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProductSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, source='tags', write_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'image',
            'created_at', 'updated_at', 'is_deleted',
            'category', 'category_id', 'tags', 'tag_ids'
        ]

class OrderItemSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_id', 'quantity', 'discount']

class OrderSerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all(), write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'number', 'created_at', 'delivery_address',
            'phone', 'customer_name', 'products', 'product_ids'
        ]

    def create(self, validated_data):
        product_ids = validated_data.pop('product_ids')
        order = Order.objects.create(**validated_data)
        for product in product_ids:
            OrderItem.objects.create(order=order, product=product, quantity=1, discount=0)
        return order
