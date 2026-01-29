
#ALL THE IMPORT COMMANDS
from django.shortcuts import render, redirect
from django.http import HttpRequest
from datetime import datetime
from database.models import Billing
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

    
 #HOME PAGE FUNCTION   
def homepg(request):
    return render(request, "home.html")
    
#ADMIN PANEL FUNCTION
def adminpanel(request):
    return render(request, 'admin_panel.html')

#ABOUT US PAGE
def about(request):
    return render(request, 'about.html')

#OUTLETS PAGE
def outlets(request):
    return render(request, 'outlets.html')

#GRAPH AND DATA SHOWING SECTION
def adminstats(request):
    filter_type = request.GET.get('filter', 'day')
    today = timezone.now().date()

    if filter_type == 'day':
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())

    elif filter_type == 'week':
        start_date = today - timedelta(days=6)
        end_date = today
    else:
        start_date = today
        end_date = today

    # ✅ Category-wise data (for bar chart)
    category_data = Billing.objects.filter(date__range=[start_date, end_date]) \
        .values('category') \
        .annotate(total_sold=Sum('qty')) \
        .order_by('category')

    categories = [item['category'] for item in category_data]
    totals = [item['total_sold'] for item in category_data]

    # ✅ Day-wise total data (for line chart)
    daily_data = (
        Billing.objects.filter(date__range=[start_date, end_date])
        .values('date')
        .annotate(total_sold=Sum('qty'))
        .order_by('date')
    )

    dates = [item['date'].strftime('%d %b') for item in daily_data]  # Format e.g. "19 Oct"
    daily_totals = [item['total_sold'] for item in daily_data]

    return render(request, 'graphs.html', {
        'categories': categories,
        'totals': totals,
        'dates': dates,
        'daily_totals': daily_totals,
        'filter_type': filter_type,
    })



#SHOING DATABASE IN TABLE 
def adminpreviousdata(request):
    # Fetch data from DB, e.g. Billing.objects.all()
    bills = Billing.objects.all().order_by('-date')  
    return render(request, 'data.html', {'bills': bills})



#MAIN BILLING FUNCTION
###THIS CONTAINS : ALL THE MENUS , FUNCTION TO FETCH VALUES , FUNCTION TO MAKE CART AND ADD VALUES IN THAT , FUNCTION TO STORE DATA IN DATABASE AND SENDING VALUES IN FRONTEND ###
def startbill(request):
    # Menu dictionaries
    north_menu = {1:"Paneer Butter Masala",2:"Palak Paneer",3:"Chole Bhature",4:"Dal Makhani",5:"Rajma Chawal",
                  6:"Aloo Paratha",7:"Paneer Tikka",8:"Kadhi Pakora",9:"Malai Kofta",10:"Baingan Bharta"}
    north_price = {1:220,2:200,3:180,4:90,5:170,6:120,7:210,8:160,9:230,10:150}

    south_menu = {1:"Masala Dosa",2:"Idli Sambar",3:"Medu Vada",4:"Upma",5:"Vegetable Uttapam",
                  6:"Lemon Rice",7:"Curd Rice",8:"Pongal",9:"Rasam with Rice",10:"Tomato Rice"}
    south_price = {1:100,2:80,3:90,4:70,5:110,6:90,7:85,8:100,9:95,10:90}

    chinese_menu = {1:"Veg Manchurian",2:"Hakka Noodles",3:"Veg Fried Rice",4:"Chilli Paneer",5:"Spring Rolls",
                    6:"Veg Schezwan Noodles",7:"Honey Chilli Potatoes",8:"Paneer Fried Rice",9:"Veg Momos",10:"Hot & Sour Soup"}
    chinese_price = {1:150,2:140,3:130,4:180,5:120,6:150,7:130,8:160,9:100,10:110}

    # Initialize session cart
    if "cart" not in request.session:
        request.session["cart"] = []

    if request.method == "POST":
         # Initialize defaults
        category = None
        dish = None
        price = 0
        total = 0


        # Remove item from cart
        if "remove_index" in request.POST:
            index = int(request.POST.get("remove_index"))
            cart = request.session.get("cart", [])
            if 0 <= index < len(cart):
                cart.pop(index)  # remove the selected item
                request.session["cart"] = cart
            return redirect('startbill')  # reload page to show updated cart
       # Check if user clicked "Finalize Bill"
        if "clear_cart" in request.POST:
            request.session["cart"] = []
            return redirect('startbill')  # reload empty billing page

       

       # Taking input of values (category,dishcode,quantity)
        category = request.POST.get("category")
        dishcode = int(request.POST.get("dishcode",0))
        qty = int(request.POST.get("qty",1))

        print(category,dishcode,qty)

        # Determine dish and price
        if category == "north":
            dish = north_menu[dishcode]
            price = north_price[dishcode]
        elif category == "south":
            dish = south_menu[dishcode]
            price = south_price[dishcode]
        else:
            dish = chinese_menu[dishcode]
            price = chinese_price[dishcode]

        # ✅ Only process if dish found
        if dish:
            total = price * qty

            # Add item to cart
            cart = request.session["cart"]
            cart.append({
                "category": category.capitalize(),
                "dish": dish,
                "qty": qty,
                "price": price,
                "total": total
            })
            request.session["cart"] = cart

            # Save in database
            Billing.objects.create(
                category=category,
                dish=dish,
                qty=qty,
                price=price,
                total=total,
                date=datetime.now()
            )

    # Calculate grand total
    grand_total = sum(item["total"] for item in request.session["cart"])

    context = {
        'north_menu': north_menu,
        'south_menu': south_menu,
        'chinese_menu': chinese_menu,
        'cart': request.session["cart"],
        'grand_total': grand_total
    }
    return render(request, 'billing.html', context)
