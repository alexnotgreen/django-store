from django.db import models

# Create your models here.
class Category(models.Model):
	category_name = models.CharField(max_length=100)
	added_data = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.category_name

class Product(models.Model):
	product_name = models.CharField(max_length=100)
	product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
	product_price = models.FloatField()
	product_description = models.TextField()
	product_count = models.IntegerField()
	product_added_data = models.DateTimeField(auto_now_add=True)
	product_image = models.ImageField(upload_to='media', blank=True, null=True)


	def __str__(self):
		return self.product_name

#Таблица корзина
class UserCart(models.Model):
	user_id = models.IntegerField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	ordered_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user_id)