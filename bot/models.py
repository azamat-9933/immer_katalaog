from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class BotUser(models.Model):
    telegram_id = models.BigIntegerField()
    interface_lang = models.CharField(max_length=3, default=" ", null=True, blank=True)

    def __str__(self):
        return f"BotUser(id={self.telegram_id}, lang={self.interface_lang})"

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"


class Category(MPTTModel):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            related_name='children', blank=True, null=True)

    def __str__(self):
        return f"{self.name_uz} | {self.name_ru}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    description_uz = models.TextField()
    description_ru = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    action = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product(id={self.pk}, name={self.model}, category={self.category})"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ProductImage(id={self.pk}, product={self.product})"

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self):
        return f"Contact(id={self.pk}, name={self.name}, phone={self.phone})"

    class Meta:
        verbose_name = "Контактное лицо"
        verbose_name_plural = "Контактные лица"
