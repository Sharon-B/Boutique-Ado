from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


# Create your views here.

# All products view
def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()        # return all products

    # start with query & other variables set to none:
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        # Sorting:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'      # rename sortkey to lower_name
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)   # sort the products

        # Filter by category:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Search:
        if 'q' in request.GET:
            query = request.GET['q']
            # if the query is blank
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # Otherwise if the query is not blank
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    # add our products to the context so they will be available in the template
    # add query to the context for search functionality
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting
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


# Add Product view
def add_product(request):
    """
    Add a product to the store
    """
    if request.method == 'POST':
        # Instantiate the submitted form
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid')

    else:
        # Otherwise Instatiate an empty form
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
