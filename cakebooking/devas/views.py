
from pyexpat.errors import messages
from django.shortcuts import render,redirect

from .forms import checkoutform 
# Create your views here.
from.models import *

def index(request):
    userviewcake=cake_details.objects.all() 
    bday=cake_details.objects.filter(type='Birthday')
    wedding=cake_details.objects.filter(type='Wedding')
    cus=cake_details.objects.filter(type='Custom')
    reviewsee=revieww.objects.all()
    # evde ella vannu print aakum , but venam enkil filter aayitt cheyyam particular user nde table visible cheyyan. adhu 
    ucv={'birthday': bday ,'wed': wedding, 'customs': cus, 'seenreview':reviewsee}
    return render(request, 'devas/index.html',ucv)

def wedding(request):
    wedding=cake_details.objects.filter(type='Wedding')
    return render(request, 'devas/wedding.html',{'wedding':wedding})
def about(request):
    return render(request, 'devas/about.html')

def cakedetails(request):
    userviewcake=cake_details.objects.all() 
    wedding=cake_details.objects.filter(type='Wedding')
    Birthday=cake_details.objects.filter(type='Birthday')
    cus=cake_details.objects.filter(type='Custom')
    ucv={'details':userviewcake,
         'wedding':wedding, 'b':  Birthday,'customs':cus}
    return render(request, 'devas/cake_details.html',ucv)
def login(request):
    
    if request.method == 'POST':
        uname = request.POST.get('email')
        passwd = request.POST.get('passwd')

        ul = registration.objects.filter(email=uname, passwd=passwd)
        # ua = user_login.objects.filter(uname=uname, passwd=passwd, u_type='admin')
        print(len(ul))
        if len(ul) == 1:
          #1 user=1email so cross check then models check length 1 allel 0
            request.session['user_name'] = ul[0].email
            request.session['id'] = ul[0].user_id
            # request.session['cart_id']
            next_url = request.session.get('next_url')
            if next_url is not None:
                del request.session['next_url']
                return redirect(next_url)

            return redirect(user_cake_details)
        
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, './devas/login.html', context)
    else:
        return render(request, './devas/login.html')
    # 1 st  edhu work

# user login cheytitt kerunna login page
def userhome(request):
    up = registration.objects.get(email= request.session['user_name'])
    userviewcake=cake_details.objects.all() 
    bday=cake_details.objects.filter(type='Birthday')
    wedding=cake_details.objects.filter(type='Wedding')
    cus=cake_details.objects.filter(type='Custom')
    
    context = {'birthday': bday ,'wed': wedding,'customs': cus,'uname': request.session['user_name']}

    return render(request,'devas/user_cake_detai.html', context)

def Registration(request):
        if request.method == 'POST':

            fname = request.POST.get('fname') #name is from signup page
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            address = request.POST.get('address')
            pin = request.POST.get('pin')
            passwd = request.POST.get('passwd')
            confirmpasswd = request.POST.get('confirmpasswd')
            variable= registration(fname=fname,lname=lname,email=email,contact=contact,pin=pin,passwd=passwd,confirmpasswd=confirmpasswd,address=address)
            if passwd!=confirmpasswd:
                msg="Password do not match.Please try again!"
                # return render(request, 'devas/Registration.html',{'msg':msg})
                return redirect(login)
            else:
                variable.save()
                msg="User created successfully"
                return render(request, 'devas/Registration.html',{'msg':msg})
              
        


        return render(request, 'devas/Registration.html')
def review(request):
    id = request.GET.get('id')
    item_details = cake_details.objects.get(id=int(id))
    user = request.session['email']
    cake_details = cake_details.objects.get(email=user)
    if request.method == 'POST':
        star_rating = request.POST.get('rating')
        item_review = request.POST.get('item_review')

        item_reviews = review(user=user, item=item_details, rating=star_rating, review_desp = item_review)
        item_reviews.save()

        rating_details = review.objects.filter(item=cake_details)
        context = {'reviews': rating_details}
        return render(request, './devas/review_page.html', context)

    rating_details = review.objects.filter(item=cake_details)
    context = {'reviews': rating_details}
    return render(request, './devas/review_page.html', context)



def cake_detail_page(request):
    cake_id = request.GET.get('id')
    cake_name =  cake_details.objects.filter(id=cake_id)
    
    context = {'details': cake_name}
    
    return render(request, './devas/cake_detail_page.html', context)
    
    
 

def addtocart(request):
    try:
        # Check if user is logged in
        if 'user_name' not in request.session:
            # If user is not logged in, store the product ID in session and redirect to login page
            request.session['next_url'] = '/addtocart?id={}'.format(request.GET.get('id'))
            return redirect('/login')

        # If user is logged in, retrieve the product and cart objects
        product_obj = cake_details.objects.get(id=int(request.GET.get('id')))
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_obj = cart.objects.get(id=cart_id)
            product_in_cart = cart_obj.cartproduct_set.filter(cake=product_obj)
            # item already exists in cart
            if product_in_cart.exists():
                cartproduct = product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, cake=product_obj, rate=product_obj.price,
                                                         quantity=1, subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()
        else:
            up = registration.objects.get(email=request.session['user_name'])
            cart_obj = cart(customer=up, total='0')
            cart_obj.save()
            request.session['cart_id'] = cart_obj.id
            print("new cart")
            cp = CartProduct.objects.create(cart=cart_obj, cake=product_obj, rate=product_obj.price, quantity=1,
                                            subtotal=product_obj.price)
            cart_obj.total = float(cart_obj.total) + float(product_obj.price)
            cart_obj.save()

        return redirect('mycart')
    except:
        request.session['next_url'] = '/mycart'
        return redirect('/login')

   
def mycart(request):
    user_id = request.session['id']
    up = registration.objects.get(user_id=user_id)
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart1 = cart.objects.get(id=cart_id)
    else:
        cart1 = None
    # cart1=cart.objects.filter(customer=user_id)
    context = {'cart': cart1, 'u': up}
    return render(request, 'devas/mycart.html', context)



def managecart(request, id):
    print("im in manage cart")
    action = request.GET.get("action")
    cp_obj = CartProduct.objects.get(id=id)

    cart_obj = cp_obj.cart
    if action == "inc":
        cp_obj.quantity += 1
        if cp_obj.quantity > cp_obj.cake.quantity:
            # messages.error(request, "Out of Stock")
            return redirect('/mycart')
        cp_obj.subtotal += cp_obj.rate
        cp_obj.save()
        cart_obj.total += cp_obj.rate
        cart_obj.save()
    elif action == "dcr":
        cp_obj.quantity -= 1
        cp_obj.subtotal -= cp_obj.rate
        cp_obj.save()
        cart_obj.total -= cp_obj.rate
        cart_obj.save()
        if cp_obj.quantity == 0:
            cp_obj.delete()
    elif action == 'rmv':
        cart_obj.total -= cp_obj.subtotal
        cart_obj.save()
        cp_obj.delete()
    else:
        pass

    return redirect('/mycart')


def emptycart(request):
    cart_id = request.session.get("cart_id", None)
    cart1 = cart.objects.get(id=cart_id)
    cart1.cartproduct_set.all().delete()
    cart1.total = 0
    cart1.save()
    return redirect('/my-cart')


def user_cake_details(request):
    userviewcake=cake_details.objects.all() 
    wedding=cake_details.objects.filter(type='Wedding')
    Birthday=cake_details.objects.filter(type='Birthday')
    cus=cake_details.objects.filter(type='Custom')
    user_id = request.session['user_name']
    up = registration.objects.filter(email=user_id)
    ucv={'details':userviewcake,
         'wedding':wedding, 'b':  Birthday,'customs':cus,'userde':up}
    return render(request, './devas/user_cake_details.html', ucv)

def user_cake_detail_page(request):
    cake_id = request.GET.get('id')
    cake_name =  cake_details.objects.filter(id=cake_id)
    product_obj = cake_details.objects.get(id=int(cake_id))
    user_id = request.session['user_name']
    up = registration.objects.get(email=user_id)
    if request.method == 'POST':
        feed= request.POST.get('mesgsavingname')
        back=revieww(review_decp=feed, cake=product_obj, user_id= up )
        back.save()
    context = {'details': cake_name}
    
    return render(request, './devas/user_cake_detail_page.html', context)

def cakedetailpage(request):
    cake_id = request.GET.get('id')
    cake_name =  cake_details.objects.filter(id=cake_id)
    
    context = {'details': cake_name}
    
    return render(request, './devas/cake_detail_page.html', context)
    
def logout(request):
    try:
        del request.session['user_name']
    except:
        return index(request)  
    else:  
        return index(request)
    
# def review(request):
    

def checkout(request):
    user_id = request.session['user_name']
    user = registration.objects.get(email=user_id)
    cart_id = request.session.get("cart_id")
    cart_obj = cart.objects.get(id=cart_id)
    form = checkoutform(request.POST)

    if request.method == "POST":
        # order_status = "Order recived"
        address = request.POST.get("address")
        mobile = request.POST.get("Contact")
        total = request.POST.get("total")

        new_order = Orders.objects.create(cart=cart_obj, customer=user, address=address, mobile=mobile,
                                          total=total, order_status='order processing')
        new_order.save()
        cart_products = cart_obj.cartproduct_set.all()
        for cart_product in cart_products:
            item = cart_product.cake
            item.quantity -= cart_product.quantity
            item.save()
        return redirect(confirm_payment)
    else:
        context = {'cart': cart_obj, 'form': form, 'user': user}
        return render(request, './devas/checkout.html', context)


def confirm_payment(request):
    user_id = request.session['user_name']
    user = registration.objects.get(email=user_id)
    cart_id = request.session['cart_id']
    cart_obj = cart.objects.get(id=cart_id)
    print(cart_obj.total)

    context = {'cart': cart_obj, 'user': user}
    return render(request, './devas/confirm_payment.html', context)


import stripe

stripe.api_key = 'sk_test_51MzR0qSDsHoB6h4XS89hryuFO2ZLs4EGe6bs44P45Pq1pYzw1FbxRGwfHU1kcz13dX9qi9RFj2PDlFn56vF51rOe00Stz4HfFt'


#
# @app.route('checkout_session', methods=['POST'])
def checkout_session(request):
    cart_id = request.session['cart_id']
    cart_obj = cart.objects.get(id=cart_id)
    print(cart_obj.customer)

    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': cart_obj.customer,
                },
                'unit_amount': cart_obj.total * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/pay_success',
        cancel_url='http://127.0.0.1:8000/pay_cancel',
    )
    del request.session['cart_id']
    return redirect(session.url, code=303)


def pay_success(request):
    return render(request, './devas/pay_success.html')


# cancel
def pay_cancel(request):
    return render(request, './devas/pay_cancel.html')

def user_order_status(request):
    up = registration.objects.get(email=request.session['user_name'])
    u = registration.objects.filter(email=request.session['user_name'])
    print(up.email)
    user_d = Orders.objects.filter(customer=up).order_by('-id')
    for i in user_d:
        print(i.customer)
        print(i.total)

    context = {'order_status': user_d, 'uname': u}
    return render(request, './devas/user_order_status.html', context)

from django.shortcuts import render

def contact(request):
    if request.method == 'POST':
        # Process the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Perform any necessary actions with the form data
        
        # Render the success page after processing the form
        return render(request, 'index.html')
    
    # Render the contact page for GET requests
    return render(request, './devas/contact.html')

def usercontact(request):
    user_id = request.session['user_name']
    user = registration.objects.get(email=user_id)
    if request.method=='POST':
       cake = request.POST.get('cake')
       message = request.POST.get('review_decp')
       ul=revieww(review_decp=message,cake=cake,user_id=user)
       ul.save()
    #    context={'userdetail':user}
       return render(request,  'devas/usercontact.html')
    #    return redirect(user_cake_details)
    return render(request,  'devas/usercontact.html')
    # return redirect(usercontact)
