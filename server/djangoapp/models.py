from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 1000)

    def __str__(self):
        return "Name: " + self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete = models.CASCADE)
    name = models.CharField(max_length = 300)
    dealer_id = models.IntegerField()
    HATCHBACK = "hatchback"
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    PICKUP = "pickup"
    CAR_TYPES = [
        (HATCHBACK, "Hatchback"),
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (PICKUP, "Pickup")
    ]
    car_type = models.CharField(max_length = 30, choices=CAR_TYPES, default=SEDAN)
    year = models.DateField()

    def __str__(self):
        return "Car: " + str(self.year) + " " + self.make.name + " " + self.name + "\n" + \
            "Car type: " + self.car_type

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, state, st, full_name, id, lat, long, short_name, zip):
        self.address = address
        self.city = city
        self.state = state
        self.st = st
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long,
        self.short_name = short_name
        self.zip = zip

    def __str__(self):
        return "Dealer Name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, name, dealership, review, purchase, purchase_date=None, car_make=None, car_model=None, car_year=None):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        if self.purchase:
            self.purchase_date = purchase_date
            self.car_make = car_make
            self.car_model = car_model
            self.car_year = car_year

    def __str__(self):
        return "Review: " + self.review


