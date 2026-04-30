import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    items = Item.objects.all()
    return render(request, "home.html", {"items": items})


def item_page(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, "item.html", {
        "item": item,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    })


def buy(request, id):
    item = get_object_or_404(Item, id=id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': item.price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri("/success/"),
        cancel_url=request.build_absolute_uri("/cancel/"),
    )

    return JsonResponse({'id': session.id})

def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")