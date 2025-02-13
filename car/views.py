
from django.shortcuts import render,redirect ,  get_object_or_404
from django.http import HttpResponse
from .models import Product
from car import views
from car.views import *
from django.views import View
from django .contrib import messages
from .forms import RegisterForm 
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from .forms import CustomerProfileForm
from .models import Customer , Payment
from django.contrib.auth import logout


# views.py
from django.shortcuts import render
from .models import Product, Booking

def home(request):
    products = Product.objects.all()  # Querying all products
    booking = None
    
    if request.user.is_authenticated:
        # Attempt to get the first booking of the logged-in user
        booking = Booking.objects.filter(user=request.user).first()  # Get the first booking or None

    return render(request, 'home.html', {'products': products, 'booking': booking})



def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')





class CategoryView(View):
    def get(self , request , val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'category.html' , locals())


class CategoryTittle(View):
    def get(self , request , val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'category.html' , locals())


class Registerview(View):
    def get(self, request):
        form = RegisterForm()  # Create an empty form
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)  # Bind the form with POST data
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, "Congratulations! Registration successful.")
            return render(request, 'register.html', {'form': form})
        else:
            messages.error(request, "Registration failed. Please check the form for errors.")
            return render(request, 'register.html', {'form': form})
        





from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import CustomerProfileForm
from .models import Customer

class ProfileView(View):
    def get(self, request):
        # Try to get the customer or create an empty form
        customer = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(instance=customer) if customer else CustomerProfileForm()
        return render(request, "profile.html", {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            # Get the cleaned data from the form
            customer_data = form.cleaned_data
            # Try to get the existing customer or create a new one
            customer, created = Customer.objects.get_or_create(user=user)
            for field, value in customer_data.items():
                setattr(customer, field, value)
            customer.save()
            
            # Display success message and redirect to the homepage
            messages.success(request, f"Profile {'created' if created else 'updated'} successfully.")
            return redirect('home')  # Redirect to the homepage after saving changes

        # In case of form errors, show the form again with error messages
        messages.warning(request, "Invalid input data. Please check the form.")
        return render(request, "profile.html", {'form': form})



def get(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())
    




class UpdateAddress(View):
    def get(self, request, pk):
        # Safely retrieve the customer object or return a 404 error if not found
        add = get_object_or_404(Customer, pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, "updateaddress.html", {'form': form, 'add': add})

    def post(self, request, pk):
        # Safely retrieve the customer object or return a 404 error if not found
        add = get_object_or_404(Customer, pk=pk)
        form = CustomerProfileForm(request.POST, instance=add)  # Ensure form is bound to the existing instance
        
        if form.is_valid():
            form.save()  # Save the updated customer instance
            messages.success(request, "Congratulations! Profile updated successfully.")
            return redirect("address")  # Redirect to the address page (or wherever you want)
        else:
            messages.warning(request, "Invalid Input Data")
        
        return render(request, "updateaddress.html", {'form': form, 'add': add})
    


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  


import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Booking, Payment, Customer
from django.shortcuts import get_object_or_404

def rent_car(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        customer = Customer.objects.get(user=request.user)
        address = {
            "name": customer.name,
            "mobile": customer.mobile,
            "locality": customer.locality,
            "city": customer.city,
            "state": customer.state,
            "zipcode": customer.zipcode
        }
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found. Please create a profile first.")
        return redirect('profile')  # Redirect to profile creation if not found

    booking = None  # Initialize booking to None

    if request.method == "POST":
        rental_duration = request.POST.get("rental_duration")
        selected_address = request.POST.get("selected_address")
        
        if selected_address == "company_address":
            address = {
                "name": "Quick Drive Office",
                "mobile": "+91 1234567890",
                "locality": "Dwarka",
                "city": "New Delhi",
                "state": "Delhi",
                "zipcode": "10001"
            }

        total_price = int(rental_duration) * product.rent_price
        
        # Create the booking first (but don't finalize it yet)
        booking = Booking.objects.create(
            user=request.user,
            product=product,
            rental_duration=rental_duration,
            total_price=total_price,
            address=address
        )

        # Create a Razorpay order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(dict(amount=total_price * 100, currency='INR', payment_capture='1'))
        
        # Store the Razorpay order id in the Payment model
        payment = Payment.objects.create(
            user=request.user,
            amount=total_price,
            razorpay_order_id=razorpay_order['id'],
            paid=False
        )

        # Add the Razorpay order ID to the booking
        booking.razorpay_order_id = razorpay_order['id']
        booking.save()

        # Redirect the user to the Razorpay payment gateway
        return render(request, 'razorpay_payment.html', {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_payment_link': razorpay_order['payment_link'],
            'booking_id': booking.id,
        })

    # Render the rent_car page and pass the context including booking
    context = {
        'product': product,
        'address': address,
        'booking': booking,
    }

    return render(request, 'rent_car.html', context)


# Callback URL from Razorpay (for handling success or failure)
def payment_done(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Capture payment info and verify it
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }

    try:
        # Verify the payment signature
        client.utility.verify_payment_signature(params_dict)

        # Mark the payment as completed
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_payment_status = 'success'
        payment.paid = True
        payment.save()

        # Update booking status
        booking.status = 'Paid'
        booking.save()

        messages.success(request, "Payment successful! Your booking is confirmed.")
        return redirect('booking_detail', booking_id=booking.id)
    
    except razorpay.errors.SignatureVerificationError:
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect('home')


# Callback URL for payment failure
def razorpay_failure(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Update booking status in case of failure
    booking.status = 'Failed'
    booking.save()

    messages.error(request, "Payment failed. Please try again.")
    return redirect('home')





from django.shortcuts import render, get_object_or_404
from .models import Booking

def booking_detail(request, booking_id):
    # Fetch the booking with the specific booking_id
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Render the booking detail page with the booking in context
    context = {
        'booking': booking,
    }
    return render(request, 'booking_detail.html', context)

from django.shortcuts import render
from .models import Booking

from django.shortcuts import render
from .models import Booking

def some_view(request):
    # Fetch all bookings for the logged-in user
    bookings = Booking.get_all()
    # If bookings are found, render the appropriate template with bookings data
    return render(request, 'booking_detail.html', {'bookings': bookings})












from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Customer, Payment
from django.contrib import messages

def payment_done(request):
    booking_id = request.GET.get('booking_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    product_id = request.GET.get('product_id')  
    rental_duration = request.GET.get('rental_duration') 
    total_price = request.GET.get('total_price') 
    address = request.GET.get('address') 

    try:
       
        cust_id = int(cust_id)
        customer = Customer.objects.get(id=cust_id)  
    except (ValueError, Customer.DoesNotExist) as e:
      
        messages.error(request, "Invalid customer ID or customer not found.")
        return redirect('home')  
    try:
        # Update payment status
        payment = Payment.objects.get(razorpay_order_id=booking_id)
        payment.paid = True
        payment.razorpay_payment_id = payment_id
        payment.save()

        # Provide confirmation message
        messages.success(request, "Payment successful, your booking is confirmed.")

        # Now create the booking
        product = get_object_or_404(Product, id=product_id)  # Get the product object from the ID

        # Create a booking instance
        booking = Booking.objects.create(
            user=request.user,
            product=product,
            rental_duration=rental_duration,
            total_price=total_price,
            address=address
        )

        # Redirect to the booking detail page if the booking was created
        if booking.id:
            messages.success(request, f"Successfully rented {product.title} for {rental_duration} days at ₹ {total_price}.")
            return redirect('booking_detail', booking_id=booking.id)  # Redirect to the booking detail page
        else:
            messages.error(request, "There was an issue creating the booking.")
            return redirect('home')  # Redirect to the home page if booking creation fails
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found.")
        return redirect('home')  # Redirect to the home page if payment does not exist




# views.py

from django.shortcuts import render

def payment_failed(request):
    # You can pass any necessary context here if required
    return render(request, 'payment_failed.html')

  
