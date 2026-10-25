from django.db import models
from parler.models import TranslatableModel, TranslatedFields

class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="Category Name / اسم التصنيف")
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Category {self.id}"


class Product(TranslatableModel):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="التصنيف")
    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name="Product Title / اسم المنتج"),
        description=models.TextField(verbose_name="Description / الوصف")
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر (SAR)")
    stock = models.IntegerField(default=0, verbose_name="الكمية المتوفرة")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="صورة المنتج")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f"Product {self.id}"