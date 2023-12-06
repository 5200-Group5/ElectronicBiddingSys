from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User  # Import Django's built-in user model
from django.conf import settings
# Create your models here.


# class CustomUser(AbstractUser):
#     first_name = models.CharField(max_length=30, blank=False)
#     last_name = models.CharField(max_length=30, blank=False)
#     email = models.EmailField(unique=True, blank=False)

#     groups = models.ManyToManyField(
#         'auth.Group',
#         blank=True,
#         related_name='customuser_set',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         blank=True,
#         related_name='customuser_set', 
#     )

#     def __str__(self):
#         return self.username


# class MyUserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password):
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class MyUser(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = MyUserManager()

#     USERNAME_FIELD = 'email'

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True

#     @property
#     def is_staff(self):
#         return self.is_admin


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


# class Item(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     description = models.TextField()
#     price = models.FloatField()
#     image = models.ImageField(upload_to="item_images")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "item"
#         verbose_name_plural = "items"

class Item(models.Model):
    name = models.CharField(max_length=255, default="Default Name") #RL ADD
    item_id = models.AutoField(primary_key=True, db_column='ItemID')  # Ensure this matches your database column name for the primary key
    description = models.TextField()
    picture = models.CharField(max_length=255, blank=True, null=True)  # Assuming a file path is stored
    category = models.CharField(max_length=255)
    condition = models.CharField(max_length=255, db_column='Cond')  # Align field name with SQL
    starting_price = models.IntegerField()
    end_date = models.DateTimeField()
    start_date = models.DateTimeField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_items'
        # No null=True and blank=True, ensuring a creator is always specified
    )

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

    class Meta:
        db_table = 'Bid'

    def __str__(self):
        return f"Bid by {self.user.username} on {self.item.name}"

    