from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404
from .models import Item
import random

def index(request):
    # get different categories and retrieve one item from each category
    categories = list(Item.objects.values_list('category', flat=True).distinct())
    random.shuffle(categories)
    selected_categories = categories[:9]

    items = []
    
    for selected_category in selected_categories:
        item = Item.objects.filter(category=selected_category)[8]
        if item:
            items.append(item)
    
    context = {
        'items': items
    }

    return render(request, 'index.html', context)


def shop_items(request):
    # Retrieve all unique categories
    unique_categories = Item.objects.values_list('category', flat=True).distinct()

    # Retrieve the search query and selected categories from the URL (if any)
    query = request.GET.get('search', '')
    selected_categories = request.GET.getlist('category')

    # Retrieve sorting parameters, provide defaults
    sort_by = request.GET.get('sort_by', 'price')    # default sort by price
    order = request.GET.get('order', 'asc')           # default ascending order

    # Start with all items
    items = Item.objects.all()

    # Apply search filter
    if query:
        items = items.filter(name__icontains=query)

    # Apply category filter
    if selected_categories:
        items = items.filter(category__in=selected_categories)

    # Determine sorting field, prefix with '-' if descending
    sort_field = sort_by if order == 'asc' else f'-{sort_by}'

    # Apply ordering
    items = items.order_by(sort_field)

    # Set up paginator
    paginator = Paginator(items, 6)
    page = request.GET.get('page')

    try:
        paged_items = paginator.get_page(page)
    except PageNotAnInteger:
        paged_items = paginator.get_page(1)
    except EmptyPage:
        paged_items = paginator.get_page(paginator.num_pages)

    # Save current query params to pass when paginating (exclude page to avoid duplication)
    query_dict = request.GET.copy()
    if 'page' in query_dict:
        query_dict.pop('page')
    query_string = query_dict.urlencode()

    context = {
        'items': paged_items,
        'categories': unique_categories,
        'selected_categories': selected_categories,
        'query_string': query_string,
    }

    return render(request, 'shop.html', context)


def item_detail(request, slug):
    '''
    view to return a single item
    '''
    item = get_object_or_404(Item, slug=slug)
    return render(request, 'shop/detail.html', {'item':item})

