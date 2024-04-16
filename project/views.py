from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from datetime import date
from .utils import item_sales
from .utils import calculate_items_sold_last_7_days



# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home_wilogin.html')
    else:
        return redirect('/login')

def add(request):
    if request.user.is_authenticated:
        if(request.method=="POST"):
            itype = request.POST['itype']
            vtype = request.POST['vtype']
            manufacturer = request.POST['manufacturer']
            quantity = request.POST['quantity']
            price = request.POST['price']
            address = request.POST['address']
            item_id = f"{itype}_{vtype}"
            item = Item(i_type=itype, v_type=vtype, manufacturer=manufacturer, quantity=quantity, price=price, address = address)
            item.save()
            msg = "Item Added Successfully"
            return render(request, 'add.html', {'msg':msg})
        else:
            msg = ""
            return render(request, 'add.html', {'msg':msg})
    else:
        return redirect('/login')

def view_login(request):
    msg=""
    if(request.method=="POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            msg="Invald ID or Password"
    return render(request, 'login.html',{'msg':msg})

def signup(request):
    if(request.method=='POST'):
        username = request.POST['username']
        cnf_pwd = request.POST['cnf_password']
        pwd = request.POST['password']
        if(pwd==cnf_pwd):
            # form.save()
            # form.save()
            user = User(username=username, password=pwd)
            user.set_password(pwd)
            user.save()
            print(username)
            return redirect('/login')
        else:
            msg = "The password doesn't match"
            # form = signupForm()
            return render(request, 'signup.html', {'msg':msg})
    else:
        # form = signupForm()
        msg = ""
        return render(request, 'signup.html', {'msg':msg})
    
def do_logout(request):
    logout(request)
    return redirect('/login')

def list(request):
    if request.user.is_authenticated:
        
        '''if request.method == 'POST':
            if 'function1' in request.POST:
            # Code for function 1
                if(request.method=="POST"):
                    item = Item.objects.get(id=id)
                    item.i_type = request.POST.get('itype')
                    item.v_type = request.POST.get('vtype')
                    item.manufacturer = request.POST.get('manufacturer')
                    item.quantity = request.POST.get('quantity')
                    item.price = request.POST.get('price')
                    item.save()
                    return redirect('/list')
                else:
                    items = Item.objects.filter(id=id)
                    return render(request, 'edit.html', {'items':items})'''
            
        '''if 'function2' in request.POST:
                item = Item.objects.filter(id=id)
                item.delete()
                return redirect('/view_delete')
            #return render(request, 'your_template.html')'''
        #calculate_items_sold_last_7_days()
        items = Item.objects.all()
        return render(request, 'list.html', {'items':items})
    
def delete(request, id):
    item = Item.objects.filter(id=id)
    item.delete()
    return redirect('/view_delete')

def view_delete(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items':items})

def edit(request, id):
    if(request.method=="POST"):
        item = Item.objects.get(id=id)
        item.i_type = request.POST.get('itype')
        item.v_type = request.POST.get('vtype')
        item.manufacturer = request.POST.get('manufacturer')
        item.quantity = request.POST.get('quantity')
        item.price = request.POST.get('price')
        item.address = request.POST.get('address')
        item.save()
        return redirect('/list')
    else:
        items = Item.objects.filter(id=id)
        return render(request, 'edit.html', {'items':items})
    
def sale(request):
    if(request.method=="POST"):
        item_combined = request.POST['item_itype']
        itype, vtype = item_combined.split('-')
        #itype, vtype = item_combined.split('-')
        quantity = int(request.POST['quantity'])
        #item = Item.objects.filter(i_type=itype)[0]
        #item = Item.objects.filter(i_type=itype, v_type=vtype).first()
        item = Item.objects.filter(i_type=itype, v_type=vtype)[0]
        items = Item.objects.all()
        if(quantity<=int(item.quantity)):
            #item.items_sold = quantity 
            item.quantity = item.quantity - quantity
            q = item.quantity
            item.save()
            cost = item.price
            sale_date = date.today()
            sale = Sale(i_type = item.i_type, manufacturer = item.manufacturer, v_type = item.v_type, quantity = q ,items_sold = quantity , cost=cost , totalcost = quantity * cost , sale_date = sale_date)
            sale.save()
            calculate_items_sold_last_7_days()
            msg = "Bill Made Successfully!"
            return render(request, 'sale.html', {'msg':msg, 'items':items})
        else:
            msg = "Insufficient inventory!"
            return render(request, 'sale.html', {'msg':msg, 'items':items})
    else:
        items = Item.objects.all()
        msg=""
        return render(request, 'sale.html', {'msg':msg, 'items':items})
    
def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'sale_list.html', {'sales':sales})

def reorder(request):
    items = Item.objects.all()
    insufficients = []
#calculate_items_sold_last_7_days()
   # if request.method == 'POST':
    #flag = 0  
    
    for item in items:
        if(item.quantity<item.threshold):
            insufficients.append(item) 

    #if request.method == 'POST' and flag ==1 :
    #   for item in items:
    #    item.quantity = item.threshold+10
    #    item.save()

    return render(request, 'reorder.html', {'insufficients':insufficients})



# views.py

#from django.shortcuts import render
#from .models import Sale
from .utils import generate_line_plot, generate_bar_plot, generate_pie_chart , calculate_totals

def plot_sales(request):
    # Query data from the Sale model
    sales = Sale.objects.all()

    # Generate plots
    line_plot = generate_line_plot(sales)
    bar_plot = generate_bar_plot(sales)
    pie_chart = generate_pie_chart(sales)
    sales = Sale.objects.all()

    # Calculate totals
    totals = calculate_totals(sales)

    # Pass plot images to the template
    context = {
        'line_plot': line_plot,
        'bar_plot': bar_plot,
        'revenue_past_month': totals['revenue_past_month'],
        'items_sold_past_month': totals['items_sold_past_month'],
        'revenue_past_week': totals['revenue_past_week'],
        'items_sold_past_week': totals['items_sold_past_week'],
        #'pie_chart': pie_chart,
    }


    #return render(request, 'all_plots.html', context)
    return render(request, 'home.html', context)

def refill(request):
    items = Item.objects.all()
    for item in items:
        if(item.quantity<item.threshold):
            if(item.threshold<=50):
                item.quantity = 50
                item.save()
            if(item.threshold>50 and item.threshold<=100):
                item.quantity = 100
                item.save()  
            else:
                item.quantity = 150
                item.save() 
            #item.quantity = 150
            #item.save()
    return redirect('/reorder')

