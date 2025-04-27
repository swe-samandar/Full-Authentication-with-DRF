from django.db import models


class Card(models.Model):
    user = models.ForeignKey('auth_user_app.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'card'
        verbose_name_plural = 'cards'        

    def __str__(self):
        return f"{self.user} - {self.product}"
    
    @property
    def format(self):
        return {
        'id': self.id,
        'user': self.user.phone,
        'product_id': self.product.id,
        'product_title': self.product.title,
        'quantity': self.quantity,
    }


class Like(models.Model):
    user = models.ForeignKey(to='auth_user_app.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(to='products.Product', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'likes'

    def __str__(self):
        return f"{self.user} - {self.product}"

    @property
    def format(self):
        return {
        'id': self.id,
        'user': self.user.phone,
        'product_id': self.product.id,
        'product_title': self.product.title,
        'quantity': self.quantity,
    }
