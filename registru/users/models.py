from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class Department(models.Model):
	name = models.CharField('Nume Departament', max_length=60)

	class Meta:
		verbose_name = "departament"
		verbose_name_plural = "departamente"

	def __str__(self):
		return self.name


class Location(models.Model):
	name = models.CharField('Nume Locatie', max_length=60)

	class Meta:
		verbose_name = "locatie"
		verbose_name_plural = "locatii"

	def __str__(self):
		return self.name 


class CustUserManager(BaseUserManager):
	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		if not email:
			raise ValueError('Este necesara adresa de email')
		email = self.normalize_email(email)
		user = self.model(
			email = email,
			is_active = True,
			is_staff = is_staff,
			is_superuser = is_superuser,
			**extra_fields
		)

		user.set_password(password)
		user.save()
		return user

	def create_user(self, email, password, **extra_fields):
		return self._create_user(email, password, False, False, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, password, True, True, **extra_fields)

class User(AbstractUser):
	email = models.EmailField(max_length=254, unique=True)
	username = models.CharField(max_length=150, blank=True, unique=False)
	first_name = models.CharField(max_length=254, blank=True)
	last_name = models.CharField(max_length=254, blank=True)
	phone = models.CharField(blank=True, max_length=30)
	hire_date = models.DateField(blank=True, null=True)
	position = models.CharField(max_length=150, blank=True)
	department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
	location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL)
	birthday = models.DateField(blank=True, null=True)

	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustUserManager()

	class Meta:
		verbose_name = "utilizator"
		verbose_name_plural = "utilizatori"

	def __str__(self):
		name = self.first_name + " " + self.last_name
		return name
