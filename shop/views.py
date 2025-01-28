from django.shortcuts import render
from django.http import HttpResponse
from .models import Products, Contact, Order, OrderUpdate
from math import ceil
import json
from datetime import datetime

# Create your views here.
def index(request):
    products = Products.objects.all()
    allProds=[]
    catProds = Products.objects.values('category','id')
    categories = {item['category'] for item in catProds}
    for icategory in categories:
        prod = Products.objects.filter(category = icategory)
        n = len(prod)
        no_of_slides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, no_of_slides), no_of_slides])
    params = {"allProds": allProds}
    return render(request, 'shop/index.html', params)
    # return HttpResponse("SHOPPPPPPP")

def about(request):
    return render(request, 'shop/about.html')
    return HttpResponse("We are at about")

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name','PPPPPP')
        email = request.POST.get('email', 'PPPPPP@yopmail.com')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        cont = Contact(name=name,email=email,phone=phone,desc=desc)
        cont.save()
    return render(request, 'shop/contact.html')
#           if(cart[item] == 0){
#              document.getElementById('div' + item).innerHTML = "<button id='"+item+"' class='btn btn-primary cart'> Add to cart</button>";
#            }

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', 8)
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    formatted_time = item.timestamp.strftime("%Y-%m-%d %I:%M:%S %p")
                    updates.append({'text': item.update_desc, 'time': formatted_time})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    return render(request, 'shop/tracker.html')
    return HttpResponse("We are at tracker")

def search(request):
    return HttpResponse("We are at search")

def productview(request, myid):
    #fetch the product using the id
    product = Products.objects.filter(id = myid)
    print("myid", product)
    params = {"product": product[0]}
    return render(request, 'shop/prodView.html', params)

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Order(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                       zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')
    return HttpResponse("We are at checkout")