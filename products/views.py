from django.shortcuts import render, get_object_or_404
from .models import Product


# Create your views here.

# All products view
def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()        # return all products

    context = {             # add our products to the context so they will be available in the template
        'products': products
    }

    return render(request, 'products/products.html', context)   # needs context as we'll need to send some things back to the template


# Single Product Details view
def product_detail(request, product_id):
    """ A view to show an individual products' details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)
