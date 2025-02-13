from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone


# Create your models here.


CATEGORY_CHOICES = [
    ('LX','luxury'),
    ('SD','sedan'),
    ('HC' , 'hatchback '),
    ('CM', 'compact'),
    ('SV', 'suv'),

]






class Product(models.Model):
    title = models.CharField(max_length=100)
    rent_price = models.IntegerField(default=1000)
    model = models.IntegerField(default=2025)
    category = models.CharField(choices=CATEGORY_CHOICES , max_length=2)
    product_image = models.ImageField(upload_to='product')
    seats = models.IntegerField(default=4)  # Number of seats in the car
    fuel_type = models.CharField(max_length=20)  
    transmission = models.CharField(max_length=20)  
    

    def __str__(self):
      return self.title
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    











class Customer(models.Model):
    # States choices
    STATES = [
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CG', 'Chhattisgarh'),
    ('DN', 'Dadra and Nagar Haveli'),
    ('DD', 'Daman and Diu'),
    ('DE', 'Delhi'),
    ('DL', 'Delhi'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JK', 'Jammu and Kashmir'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
]
    
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=STATES)
    city = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=10)
    locality = models.CharField(max_length=100)

    def __str__(self):
        return self.name


    

# models.py

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rental_duration = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2 , default=1000)  # Add total price
    address = models.TextField(default="company")  # Store address as text
   
    def __str__(self):
        return f"Booking by {self.user.username} for {self.product.title}"
    
    @staticmethod
    def get_all():
        return Booking.objects.all()


