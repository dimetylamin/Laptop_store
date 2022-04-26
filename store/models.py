from django.db import models

# Create your models here.


class Base(models.Model):
    class Meta:
        abstract = True
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Brand(Base):
    name = models.CharField(max_length=50, null=False)


class Product(Base):
    name = models.CharField(max_length=100, null=False, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='media/image/', null=False)
    description = models.TextField()
    cpu = models.CharField(max_length=300, null=True)
    ram = models.CharField(max_length=300, null=True)
    disk = models.CharField(max_length=300, null=True)
    vga = models.CharField(max_length=300, null=True)
    display = models.CharField(max_length=300, null=True)
    port = models.CharField(max_length=300, null=True)
    audio = models.CharField(max_length=300, null=True)
    keyboard = models.CharField(max_length=300, null=True)
    lan = models.CharField(max_length=300, null=True)
    webcam = models.CharField(max_length=300, null=True)
    wifi = models.CharField(max_length=300, null=True)
    sd = models.CharField(max_length=300, null=True)
    cd = models.CharField(max_length=300, null=True)
    bluetooth = models.CharField(max_length=300, null=True)
    os = models.CharField(max_length=300, null=True)
    battery = models.CharField(max_length=300, null=True)
    weight = models.CharField(max_length=300, null=True)
    color = models.CharField(max_length=300, null=True)
    dimension = models.CharField(max_length=300, null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    newprice = models.IntegerField(null=True)


class Order(Base):
    name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=10, null=False)
    email = models.EmailField()
    address = models.CharField(max_length=300, null=False)
    payment = models.IntegerField()
    list_order = models.JSONField(null=True)
    order_status=models.BooleanField(default=True)
