from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

STATUS_CHOICES = (
    ('PD', 'Pending'),
    ('PC', 'Processing'),
    ('SP', 'Shiped'),
)


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    picture = models.ImageField(upload_to='static/img/', null=True)
    price = models.DecimalField(decimal_places=2, max_digits=24, default=0)
    brand = models.ForeignKey(Brand)
    category = models.ForeignKey('Category')
    created_by = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return "%s (%s) - %s" % (self.title, self.brand.name, self.category.name)


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey("self", related_name="children", blank=True, null=True)

    def __str__(self):

        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(User, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "%s %s" % (self.customer.username, self.status)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price_perunit = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=10, null=True)

    def save(self):
        if not self.quantity:
            self.total_price = self.price_perunit * self.quantity

    def __str__(self):
        return "%s %s %s" % (self.product.title, self.quantity, self.price_perunit)
