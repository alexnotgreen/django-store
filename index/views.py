from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
import telebot


# Create your views here.
def index(request):
	all_products = models.Product.objects.all()

	return render(request, 'index.html', {'products': all_products})


def about(request):
	return HttpResponse('Hello my name is Alexander. Hudoholasi Im not shakhzod')


def location(request):
	return HttpResponse(
		'https://www.google.com/maps/d/viewer?msa=0&mid=1KUWpAJRMOgiDJu729AT9BgBeIUI&ll=41.31235512450395%2C69.269813&z=16')


# get full info about product
def about_product(request, pk):
	product = models.Product.objects.get(product_name=pk)

	return render(request, 'about_product.html', {'product': product})


# страница корзины
def user_cart(request):
	user_products = models.UserCart.objects.filter(user_id=request.user.id)

	total_amount = sum([total.quantity * total.product.product_price for total in user_products])

	return render(request, 'user_cart.html', {'product': user_products, 'total': total_amount})


# Добавление в корзину
def add_pr_to_cart(request, pk):
	if request.method == 'POST':
		quantity = int(request.POST.get('quantity'))
		user_id = request.user.id
		product_id = models.Product.objects.get(id=pk)

		if product_id.product_count > quantity:
			# уменьшение кол-ва на складе
			product_id.product_count -= quantity

			product_id.save()

			# проверка есть ли этот товар в корзине
			checker = models.UserCart.objects.filter(user_id=user_id, product=product_id)
			if not checker:
				# Добавление в корзину
				models.UserCart.objects.create(user_id=user_id, product=product_id, quantity=quantity)


			else:
				pr_to_add = models.UserCart.objects.get(user_id=user_id, product=product_id)
				pr_to_add.quantity += quantity
				pr_to_add.save()

			return redirect('/')

		else:
			return redirect(f'/product/{product_id.product_name}')


# Удаление с корзины
def delete_from_cart(request, pk):
	if request.method == 'POST':
		product_to_delete = models.Product.objects.get(id=pk)

		user_cart = models.UserCart.objects.get(product=product_to_delete, user_id=request.user.id)

		product_to_delete.product_count += user_cart.quantity

		user_cart.delete()

		product_to_delete.save()

		return redirect('/cart')

	return redirect('/')


def confirm_order(request, pk):
	if request.method == 'POST':
		user_cart = models.UserCart.objects.filter(user_id=request.user.id)

		full_message = 'Новый заказ:\n\n'

		for item in user_cart:
			full_message += f'Продукт: {item.product.product_name}: {item.quantity} шт\n'

		total = [i.product.product_price * i.quantity for i in user_cart]

		full_message += f'\n\nВсего за заказ: {sum(total)}'

		bot = telebot.TeleBot("5310045536:AAHK1AEcJDMxGf0pabscUyRst2wRst8Zza8")
		bot.send_message(299748548, full_message)

		user_cart.delete()

		return redirect('/')
