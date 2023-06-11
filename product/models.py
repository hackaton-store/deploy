from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator




User = get_user_model()

class Brand(models.TextChoices):
    another = 'Another'
    toyota = 'Toyota'
    mercedes = 'Mercedes'
    bmw = 'BMW'
    audi = 'Audi'

class Color(models.TextChoices):
    another = 'Another'
    RED = 'R', 'Red'
    BLUE = 'B', 'Blue'
    GREEN = 'G', 'Green'
    YELLOW = 'Y', 'Yellow'
    BLACK = 'BK', 'Black'
    WHITE = 'WH', 'White'
    SILVER = 'SV', 'Silver'
    GRAY = 'GR', 'Gray'

def get_default_image():
    return 'cars/image.png'


class StatusChoices(models.TextChoices):
    processing = "processing"
    published = "published"


class Car(models.Model):
    title = models.CharField(max_length=20, default='Untitled')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    brand = models.CharField(max_length=100, choices=Brand.choices)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    color = models.CharField(max_length=40, choices=Color.choices)
    release = models.IntegerField(
        validators=[
            MaxValueValidator(2023, 'Date cannot be above 2023'), 
            MinValueValidator(1900, 'Date cannot be below 1900')
        ]
    )
    image = models.ImageField(upload_to='cars', default=get_default_image)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self) -> str:
        return f'{self.title} | {self.brand} {str(self.release)} year'
    
    