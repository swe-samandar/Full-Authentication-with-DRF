from django.db import models


class Order(models.Model):
    user = models.ForeignKey('auth_user_app.CustomUser', on_delete=models.CASCADE)
    card = models.ManyToManyField('products.Card')
    summa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.card}"
    