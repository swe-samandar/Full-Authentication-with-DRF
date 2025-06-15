from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey('auth_user_app.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(max_length=20)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title 
    
    @property
    def format(self):
        return {
            'id': self.id,
            'category': self.category.name,
            'title': self.title,
            'short_desc': self.short_desc,
            'price': self.price,
            'price_type': self.price_type,
            'image': self.image,
            'created_at': self.created_at
        }
