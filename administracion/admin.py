import json
from django.contrib import admin
from .models import Product,Horse
import requests

class HorseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Primero, guardar el objeto en la base de datos
        super().save_model(request, obj, form, change)

        # Luego, enviar los datos del caballo a la API
        horse_data = {
            "idHorse": obj.idHorse,
            "breed": obj.breed,
            "description": obj.description,
            "price": obj.price,
            "imagePath": request.build_absolute_uri(obj.imagePath.url) if obj.imagePath else None,
            "bornOn": obj.bornOn.isoformat(),
        }

        horse_json = json.dumps(horse_data)

        # URL de la API
        url = 'http://localhost:443/horse/v1/upload'

        # Hacer la solicitud POST
        response = requests.post(url, data=horse_json, headers={'Content-Type': 'application/json'})

        # Verificar la respuesta
        if response.status_code != 200:
            # Aquí puedes manejar el error como prefieras
            print('Error al crear el caballo:', response.content)

    
    list_display = ('idHorse', 'breed', 'description', 'price', 'imagePath', 'bornOn')


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Primero, guardar el objeto en la base de datos
        super().save_model(request, obj, form, change)

        # Luego, enviar los datos del producto a la API
        product_data = {
            "idProduct": obj.idProduct,
            "nameProduct": obj.nameProduct,
            "description": obj.description,
            "price": obj.price,
            "stock": obj.stock,
            "imagePath": request.build_absolute_uri(obj.imagePath.url) if obj.imagePath else None,
            "category": obj.get_category_display(),
        }

        product_json = json.dumps(product_data)

        # URL de la API
        url = 'http://localhost:443/product/v1/upload'

        # Hacer la solicitud POST
        response = requests.post(url, data=product_json, headers={'Content-Type': 'application/json'})

        # Verificar la respuesta
        if response.status_code != 200:
            # Aquí puedes manejar el error como prefieras
            print('Error al crear el producto:', response.content)

    list_display = ('idProduct', 'nameProduct', 'description', 'price', 'stock', 'imagePath', 'category')

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Horse, HorseAdmin)
