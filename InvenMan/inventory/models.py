from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Books', 'Books'),
        ('Electronics', 'Electronics'),
        ('Stationary', 'Stationary'),
    ]

    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='item_images/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

from django.db import models
from django.utils.timezone import now  # Import to handle timezone-aware timestamps

class Borrower(models.Model):
    id_number = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    branch = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)  # New field for return timestamp

    def __str__(self):
        return f"{self.name} - {self.item.name} ({self.quantity})"
"{self.name} - {self.item.name} ({self.quantity})"