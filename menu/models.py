from typing import cast
from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    # slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # def get_url(self):
    #     return reverse('products_by_category', args=[self.slug])
    # def __str__(self):
    #     return self.category_name

class Food(models.Model):
    food_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    # stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    # 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Food Menu"
        ordering = ('created_date',)

    def get_url(self):
        return reverse('product_detail' )
    def __str__(self):
        return self.food_name
