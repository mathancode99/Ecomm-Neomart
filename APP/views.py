
from django.shortcuts import render,redirect,get_object_or_404
from .form import *
from django.contrib.auth import authenticate,login
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from datetime import datetime
from django.db.models import Sum
# from datetime import datetime



# -----------------------------------------sign_up------------------------

def sign_up(request):
    # print(request.POST)
    if request.method=='POST':
        print(request.POST.get('role'))
        character=request.POST.get('role')
        
        search=Roles.objects.filter(name=character).first()
        # s_id=search.id
        # print(search.id)
        
        form=UserForm(request.POST)
        if form.is_valid():
            # print("hi000")
            user_id=form.save()
            # u_id=user_id.id
            print(user_id.id)
            
            # User_roles.objects.create(user_id=user_id, role_id=search)
            User_roles.objects.create(user=user_id, role=search)

            return redirect('/sign_in')
        else:
            print("error")
    return render(request,'sign_up.html')


# -----------------------------------------sign_in------------------------

def sign_in(request):
    print(request.POST)
    if request.method=='POST':
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        print(name)
        print(pwd)
        try:
            user=authenticate(request,username=name,password=pwd)
            # print(request.user.id)
            print(user)
            if user is not None:
                # print('hi')
                login(request, user)
                
                # Check if the user is a superuser (admin)------------
                
                if user.is_superuser:
                    return redirect('/admin_panel') 
                               
                # Get the user ID---------------------
                user_ids = request.user.id
                print(user_ids)

                # Get the user's role from User_Roles-------
                # print('hi1')
                value = User_roles.objects.filter(user=user).first()
                print(value)
                # print('hi2')
                if value:
                    role_id = value.role.id  
                    if role_id == 1:  # Customer
                        return redirect('/user_panel')
                    elif role_id == 2:  # Seller
                        print('hi3')
                        seller = Seller.objects.filter(user=user).first()
                        if seller:
                            return redirect('/seller_panel')
                        else:
                            return redirect('/seller_account')
                               
                else:
                    print('signin error')
                    return redirect('/sign_in')
            else:
                print('sign22')
                return redirect('/sign_in')
        
        except:
            pass
    
    return render(request,'sign_in.html')


# -----------------------------------------user_panel------------------------

def user_panel(request):
    cartdata=Product.objects.all()
    return render(request,'user_panel.html',{'cart':cartdata})

# -----------------------------------------admin_panel------------------------

def admin_panel(request):
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    # Total Orders
    total_orders = Order.objects.count()

    # Total Revenue
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Total Users
    total_users = User.objects.count()

    # Total Sellers
    total_sellers = Seller.objects.count()

    # Sales This Month
    monthly_sales = Order.objects.filter(order_date__month=current_month, order_date__year=current_year).aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Sales This Year
    yearly_sales = Order.objects.filter(order_date__year=current_year).aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Monthly Sales Data (Last 12 Months)
    monthly_data = []
    for month in range(1, 13):
        sales = Order.objects.filter(order_date__month=month, order_date__year=current_year).aggregate(Sum('total_price'))['total_price__sum'] or 0
        monthly_data.append({"month": month, "sales": sales})

    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_users": total_users,
        "total_sellers": total_sellers,
        "monthly_sales": monthly_sales,
        "yearly_sales": yearly_sales,
        "monthly_data": monthly_data
    }

    return render(request,'admin_panel.html',context)

# -----------------------------------------seller_panel------------------------


def seller_panel(request):
    # Fetch the logged-in seller
    vendor = Seller.objects.filter(user=request.user).first()
    
    # If seller exists, get their products; otherwise, set an empty list
    all_products = Product.objects.filter(seller=vendor) 
    username = request.user.username
    # Pass data to the template
    return render(request, 'seller_panel.html', {'data': all_products,'username': username})


# -----------------------------------------seller_account_creation------------------------

@login_required
def seller_account(request):
        
    if request.method == "POST":
        business_name= request.POST.get("business_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        Seller.objects.create(
            user=request.user,
            business_name=business_name,
            phone=phone,
            address=address
        )

        return redirect("/seller_panel")


    return render(request, 'seller_account.html') 

# -----------------------------------------product_adding------------------------


def add_product(request):
    if request.method == 'POST':
        # Fetch seller object for the logged-in user
        vendor = Seller.objects.filter(user=request.user).first()
        print(vendor)
     
        
        # Get form data
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')  
        stock = request.POST.get('stock')
        category = request.POST.get('category')  
        description = request.POST.get('description')  

       

        # Create the product
        create = Product.objects.create(
            seller=vendor,  # Assigning the Seller instance correctly
            product_name=name,
            category=category,  # Assigning the actual Category instance
            price=price,
            stock=stock,
            description=description,
            image=image
        )
        
        return redirect("/seller_panel")
    return redirect("/seller_panel")

# -----------------------------------------Delete_product------------------------

def delete_product(request,pk):
    a =Product.objects.filter(id=pk).first()
    a.delete()
    return redirect('/seller_panel')

# -----------------------------------------update_product------------------------

def update_product(request, pk):
    obj = Product.objects.all() 
    product = get_object_or_404(Product, id=pk) 

    if request.method == "POST":
        new_image = request.FILES.get('image')
        if new_image:
            if product.image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            product.image = new_image  # Assign new image

        product.product_name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.category = request.POST.get('category')
        product.description = request.POST.get('description')

        product.updated_date = datetime.now().date()
        product.updated_by = request.user

        product.save()
        return redirect('/seller_panel')

    return render(request, 'update_product.html', {'data': obj, 'product': product})

# ------------------------serach---------------------
def search_product(request):
    # obj = Product.objects.all()  
    # print(obj)
    if request.method == 'POST':
        name = request.POST.get('search')  
        print(name) 
        if name:  # Search input not empty
            obj = Product.objects.filter(product_name__icontains=name) 

    return render(request, 'user_panel.html', {'cart': obj}) 

def search_category(request):
    if request.method == 'GET':
        category_name = request.GET.get('category')  # Get category from URL
        if category_name:
            products = Product.objects.filter(category=category_name)  # Filter products
            return render(request, 'user_panel.html', {'cart': products})  # Send data to template
        else:
            return HttpResponse("No category selected.")  # Handle missing category
    return HttpResponse("Invalid request method.")

# ----------------------------buy product------
def checkout(request):
    if request.method == "POST":
        print(request.POST)
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        total_price = float(request.POST.get("total_price"))

        product = Product.objects.get(id=product_id)
        addresses = ShippingAddress.objects.filter(user=request.user)

        return render(request, "checkout.html", {
            "product": product,
            "quantity": quantity,
            "total_price": total_price,
            "addresses": addresses
        })

    return redirect("/user_panel")  
# -------------------------------place_order--------------------
def order_success(request):
    return render(request, "order_succes.html")

def place_order(request):
    if request.method == "POST":
        print(request.POST)  # Debugging: Check what data is received

        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        selected_address = request.POST.get("selected_address")

        # Validate product existence
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return HttpResponse("Invalid product selected", status=400)

        # Handle shipping address
        if selected_address == "new":  # If user selects "Add a New Address"
            address = ShippingAddress.objects.create(

                user=request.user,
                full_name=request.POST.get("full_name"),
                phone=request.POST.get("phone"),
                address=request.POST.get("address"),
                city=request.POST.get("city"),
                state=request.POST.get("state"),
                zip_code=request.POST.get("zip_code"),
                country=request.POST.get("country")
            )
        else:
            # Ensure selected_address is a valid number
            if selected_address.isdigit():
                try:
                    address = ShippingAddress.objects.get(id=int(selected_address))
                except ObjectDoesNotExist:
                    return HttpResponse("Selected address does not exist", status=400)
            else:
                return HttpResponse("Invalid address selection", status=400)

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=product.price * quantity,
            shipping_address=address  # store full address object (not string)
        )

        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        return redirect("order_success")  # Redirect to order success page

    return redirect("checkout")  # Redirect back if error

# --------------------------------listing _orders---------------

def show_order(request):
    if request.user.is_authenticated:
        # Get all orders placed by the logged-in user
        user_orders = Order.objects.filter(user=request.user)
        
        # Get all order items from those orders
        order_items = OrderItem.objects.filter(order__in=user_orders)
        
        return render(request, 'order_show.html', {'order_items': order_items})
    else:
        return redirect('login')  # Redirect if the user is not logged in