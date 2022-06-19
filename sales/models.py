from django.db import models
from users.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Category(models.Model):
	name = models.CharField("Nume", max_length=120)

	class Meta:
		verbose_name = "gama"
		verbose_name_plural = "game"

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField("Nume", max_length=120)
	weight = models.CharField("Gramaj", max_length=20)
	unit = models.CharField("U.M.", max_length=10)
	category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="gama")
	packing = models.CharField("Ambalaj", max_length=25, blank=True)
	
	class Meta:
		verbose_name = "produs"
		verbose_name_plural = "produse"
	
	def __str__(self):
		return self.name


class Zone(models.Model):
	name = models.CharField("Zona", max_length=10)
	area = models.CharField("Regiunea", max_length=10)

	class Meta:
		verbose_name = "zona"
		verbose_name_plural = "zone"

	def __str__(self):
		return self.name


class County(models.Model):
	name = models.CharField("Județ", max_length=50, default="ALBA")
	zone = models.ForeignKey(Zone, blank=True, null=True, on_delete=models.SET_NULL)
	area = models.CharField("Regiunea", max_length=10)

	class Meta:
		verbose_name = "județ"
		verbose_name_plural = "județe"

	def __str__(self):
		return self.name


class Agent(models.Model):
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	zone = models.ForeignKey(Zone, blank=True, null=True, on_delete=models.SET_NULL)

	class Meta:
		verbose_name = "ASS"
		verbose_name_plural = "ASSi"

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name


class Channel(models.Model):
	name = models.CharField("Tip Canal", max_length=25)

	class Meta:
		verbose_name = "canal"
		verbose_name_plural = "canale"

	def __str__(self):
		return self.name


class Client(models.Model):
	name = models.CharField("Numele", max_length=254)
	loc_name = models.CharField("Numele locatiei", max_length=254, null=True, blank=True)
	CUI = models.IntegerField("CUI", blank=True, null=True)
	channel = models.ForeignKey(Channel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Canal distributie")
	distributor = models.BooleanField("Distribuitor", blank=True)
	lka = models.BooleanField("Local Key Accout", blank=True)
	zone = models.ForeignKey(Zone, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Zona")
	address = models.CharField("Adresa", max_length=254, blank=True)
	city = models.CharField("Localitatea", max_length=50, blank=True)
	county = models.ForeignKey(County, blank=True, null=True, on_delete=models.SET_NULL)
	contact_person = models.CharField("Persoana de contact", max_length=254, blank=True)
	contact_position = models.CharField("Functia", max_length=254, blank=True, null=True)
	phone = models.CharField("Telefon", max_length=10, blank=True)
	email = models.EmailField("Email", max_length=100, blank=True)

	class Meta:
		verbose_name = "client"
		verbose_name_plural = "clienti"

	def __str__(self):
		return self.name


class ShopType(models.Model):
	name = models.CharField("Tipul", max_length=50, blank=True, null=True)
	short = models.CharField("Prescurtat", max_length=3, blank=True, null=True)

	class Meta:
		verbose_name = "categorie magazin"
		verbose_name_plural = "categorii magazine"

	def __str__(self):
		return self.short


class Shop(models.Model):
	name = models.CharField("Numele", max_length=254)
	client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.CASCADE)
	shop_type = models.ForeignKey(ShopType, blank=True, null=True, on_delete=models.SET_NULL)
	address = models.CharField("Adresa", max_length=254, blank=True)
	city = models.CharField("Localitatea", max_length=50, blank=True)
	county = models.ForeignKey(County, blank=True, null=True, on_delete=models.SET_NULL)	

	class Meta:
		verbose_name = "magazin"
		verbose_name_plural = "magazine"

	def __str__(self):
		return self.name


class Visit(models.Model):
	agent = models.ForeignKey(Agent, blank=True, null=True, on_delete=models.SET_NULL)
	client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL, related_name="client")
	shop = models.ForeignKey(Shop, blank=True, null=True, on_delete=models.SET_NULL, related_name="shop")
	date_created = models.DateTimeField(default=timezone.now, blank=True)
	last_modified = models.DateTimeField(auto_now=True)
	products = models.ManyToManyField(Product, related_name="products")
	products_ordered = models.ManyToManyField(Product, related_name="products_ordered")
	shelf_image = models.ImageField(upload_to="images/", blank=True)
	quantity_ordered = models.IntegerField("Baxuri comandate", blank=True, null=True)
	observations = models.TextField(blank=True, null=True)

	class Meta:
		verbose_name = "vizita"
		verbose_name_plural = "vizite"

	def __str__(self):
		name = f"{self.client} - {self.shop} - {self.date_created}"
		return name

class WeekPlan(models.Model):
	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)
	agent = models.ForeignKey(Agent, blank=True, null=True, on_delete=models.SET_NULL)
	date_created = models.DateField(default=timezone.now, blank=True)
	last_modified = models.DateTimeField(auto_now=True)
	monday_location = models.ForeignKey(County, blank=True, null=True, on_delete=models.SET_NULL, related_name="monday_location")
	monday_goal = models.TextField(blank=True)
	monday_achieved = models.TextField(blank=True)
	tuesday_location = models.ForeignKey(County, blank=True, null=True, on_delete=models.SET_NULL, related_name="tuesday_location")
	tuesday_goal = models.TextField(blank=True)
	tuesday_achieved = models.TextField(blank=True)
	wendsday_location = models.ForeignKey(County, blank=True, null=True, on_delete=models.SET_NULL, related_name="wendsday_location")
	wendsday_goal = models.TextField(blank=True)
	wendsday_achieved = models.TextField(blank=True)
	thursday_location = models.ForeignKey(County, blank=True, null=True, on_delete=models.SET_NULL, related_name="thursday_location")
	thursday_goal = models.TextField(blank=True)
	thursday_achieved = models.TextField(blank=True)
	friday_location = models.ForeignKey(County, blank=True, null=True, on_delete=models.SET_NULL, related_name="friday_location")
	friday_goal = models.TextField(blank=True)
	friday_achieved = models.TextField(blank=True)

	class Meta:
		verbose_name = "plan saptamanal"
		verbose_name_plural = "planuri saptamanale"


class Brand(models.Model):
	name = models.CharField("Brand", max_length=100)

	def __str__(self):
		return self.name

class Producer(models.Model):
	name = models.CharField("Producator", max_length=100)

	def __str__(self):
		return self.name


class ProductInfo(models.Model):
	name = models.CharField("Nume produs", max_length=254)
	weight = models.CharField("Gramaj", max_length=20)
	unit = models.CharField("U.M.", max_length=10)
	category = models.ForeignKey("Category", blank=True, null=True, on_delete=models.SET_NULL, verbose_name="gama")
	packing = models.CharField("Ambalaj", max_length=25, blank=True)
	brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="brand")
	producer = models.ForeignKey("Producer", on_delete=models.CASCADE, verbose_name="producator")

	class Meta:
		verbose_name = "produs concurenta"
		verbose_name_plural = "produse concurenta"

	def __str__(self):
		product_name = f"{self.brand} - {self.name}"
		return product_name
	
	def get_absolute_url(self):
		return reverse('sales:productinfo_detail', args=[str(self.id)])


class PriceEntry(models.Model):
	price_value = models.FloatField(null=True, default=0)
	product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='productinfo')
	agent = models.ForeignKey(Agent, blank=True, null=True, on_delete=models.SET_NULL)
	client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL, related_name="priceinfo_client")
	shop = models.ForeignKey(Shop, blank=True, null=True, on_delete=models.SET_NULL, related_name="priceinfo_shop")
	date_created = models.DateTimeField(default=timezone.now, blank=True)
	last_modified = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "inregistrare pret"
		verbose_name_plural = "inregistrari pret"