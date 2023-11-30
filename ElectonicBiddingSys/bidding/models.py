from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in user model

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # In a real-world scenario, use Django's built-in user model for password handling
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Assuming image handling is set up
    payment_details = models.CharField(max_length=255, blank=True)
    USER_TYPE_CHOICES = [
        ('Seller', 'Seller'),
        ('Buyer', 'Buyer'),
    ]
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_messages', db_column='ReceiverID')
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages', db_column='SenderID')
    context = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.name} to {self.receiver.name}"
    
class Item(models.Model):
    item_id = models.AutoField(primary_key=True, db_column='ItemID')  # Ensure this matches your database column name for the primary key
    description = models.TextField()
    picture = models.CharField(max_length=255, blank=True, null=True)  # Assuming a file path is stored
    category = models.CharField(max_length=255)
    condition = models.CharField(max_length=255, db_column='Cond')  # Align field name with SQL
    starting_price = models.IntegerField()
    end_date = models.DateTimeField()
    start_date = models.DateTimeField()

    class Meta:
        db_table = 'Item'  # Use the existing table name

    def __str__(self):
        return f"Item in {self.category} - {self.condition}"


    
class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True, db_column='BidID')  # Explicit primary key
    item = models.ForeignKey('Item', on_delete=models.CASCADE, db_column='ItemID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserID')  # Reference to Django's User model
    price = models.IntegerField(db_column='Price')
    status = models.CharField(max_length=255, db_column='Status')

    def __str__(self):
        return f"Bid by {self.user.username} on {self.item.name}"
    
class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='UserID')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, db_column='ItemID')
    order_date = models.DateField()
    status = models.CharField(max_length=255)
    total_amount = models.IntegerField()

    def __str__(self):
        return f"Order {self.id} by {self.user.name} for {self.item.name}"
    
class Admin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # In a real-world scenario, use Django's built-in user model for password handling
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='admin_pics/', blank=True, null=True)  # Assuming image handling is set up

    def __str__(self):
        return self.email
    
class Delivery(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='OrderID')
    delivery_status = models.CharField(max_length=255)
    estimated_delivery_date = models.DateField()

    def __str__(self):
        return f"Delivery for Order {self.order.id}"
    
class ViewHistory(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='UserID')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, db_column='ItemID')
    date = models.DateField()

    def __str__(self):
        return f"ViewHistory for {self.user.name} on {self.item.name}"
    
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
        ('Card', 'Card'),
    ]
    TRANSACTION_STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Cancelled', 'Cancelled'),
    ]

    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPE_CHOICES)
    transaction_date = models.DateField()
    transaction_status = models.CharField(max_length=15, choices=TRANSACTION_STATUS_CHOICES)

    def __str__(self):
        return f"Transaction {self.id} - {self.transaction_type}"
    
class Review(models.Model):
    reviewee = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_reviews', db_column='RevieweeID')
    reviewer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='given_reviews', db_column='ReviewerID')
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, db_column='TransactionID')
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    content = models.TextField()

    def __str__(self):
        return f"Review by {self.reviewer.name} for {self.reviewee.name}"