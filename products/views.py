from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product


# Create your views here.

# All products view
def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()        # return all products
    # start with query set to none:
    query = None

    # Search:
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            # if the query is blank
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # if the query is not blank
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # add our products to the context so they will be available in the template
    # add query to the context for search functionality
    context = {
        'products': products,
        'search_term': query
    }

    return render(request, 'products/products.html', context)
    # needs context as we'll need to send some things back to the template


# Single Product Details view
def product_detail(request, product_id):
    """ A view to show an individual products' details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)
