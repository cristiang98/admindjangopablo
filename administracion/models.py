from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.core.validators import MinLengthValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

def validate_born_on(value):
    if value > timezone.now().date():
        raise ValidationError("El campo 'bornOn' debe ser una fecha en el pasado.")

# Create your models here.
class Horse(models.Model):


    idHorse = models.AutoField(primary_key=True)
    breed = models.CharField(
        max_length=100, 
        validators=[
            MinLengthValidator(1, "El campo 'breed' debe tener al menos 1 caracter."),
            MaxLengthValidator(100, "El campo 'breed' debe tener entre 1 y 100 caracteres.")
        ],
        blank=False,
        null=False
    )
    description = models.TextField(
        validators=[
            MinLengthValidator(1, "El campo 'description' no puede estar en blanco."),
            MaxLengthValidator(1000, "El campo 'description' puede tener hasta 1000 caracteres.")
        ],
        blank=False,
        null=False
    )
    price = models.PositiveIntegerField(
        validators=[MinValueValidator(0, "El campo 'price' debe ser cero o un número positivo.")],
        blank=False,
        null=False
    )
    imagePath = models.ImageField(upload_to='images/', blank=True, null=True)
    bornOn = models.DateField(
        validators=[validate_born_on],
        blank=False,
        null=False
    )


class Product(models.Model):
    ALIMENTACION = 'AL'
    CUIDADOS = 'CU'
    UTILIDADES = 'UT'

    CATEGORY_CHOICES = [
        (ALIMENTACION, 'Alimentacion'),
        (CUIDADOS, 'Cuidados'),
        (UTILIDADES, 'Utilidades'),
    ]

    idProduct = models.AutoField(primary_key=True)
    nameProduct = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(
        validators=[MinValueValidator(0, "El campo 'price' debe ser cero o un número positivo.")],
    )
    stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0, "El campo 'stock' debe ser cero o un número positivo.")],
    )
    imagePath = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=ALIMENTACION,
    )

class Userdata(models.Model):

    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="El correo electrónico debe ser válido")],
        blank=False,
        null=False,
        error_messages={
            'unique': "Un usuario con ese correo electrónico ya existe.",
        }
    )
    name = models.CharField(max_length=200, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    cellphone = models.CharField(max_length=200, blank=False, null=False)
    dni = models.CharField(max_length=200, unique=True, blank=False, null=False)
    role = models.CharField(max_length=200)
    idCart = models.PositiveIntegerField(blank=True, null=True)

class Sale(models.Model):

    
    id = models.AutoField(primary_key=True)
    total = models.PositiveIntegerField()
    userEmail = models.EmailField()
    dni = models.CharField(max_length=200)
    items = HStoreField()
    date = models.DateField()

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    items = HStoreField()
    total = models.PositiveIntegerField()