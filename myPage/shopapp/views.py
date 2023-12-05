import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def shop_index(request: HttpRequest) -> HttpResponse:
    context = {
        'list': [random.randint(x, 50) for x in range(9)],
        'name': 'blanditiis',
    }
    return render(request, 'shopapp/index.html', context=context)
