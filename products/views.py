from django.shortcuts import render
from .models import Product


# Create your views here.
def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()        # return all products

    context = {             # add our products to the context so they will be available in the template
        'products': products
    }

    return render(request, 'products/products.html', context)   # needs context as we'll need to send some things back to the template
