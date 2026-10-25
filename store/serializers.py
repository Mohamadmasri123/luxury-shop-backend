from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from .models import Category, Product

class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = ('id', 'slug', 'translations')


class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'category_name', 'price', 'stock', 'image', 'translations')

    def get_category_name(self, obj):
        return obj.category.safe_translation_getter('name', any_language=True)