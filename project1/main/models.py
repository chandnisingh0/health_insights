from django.db import models


class HealthData(models.Model):
    CurrentTime = models.DateTimeField()
    Temperature = models.FloatField()
    Heartbeat = models.IntegerField()
    SpO2 = models.IntegerField()
    RBC = models.FloatField()
    WBC = models.FloatField()
    Platelets = models.FloatField()
    BloodGlucose = models.FloatField()
    HbConcentration = models.FloatField()
    RespirationRate = models.IntegerField()
    SleepMonitoring = models.CharField(max_length=50)
    StepCount = models.IntegerField()
    MovementData = models.CharField(max_length=50)

    def __str__(self):
        return self.CurrentTime

# class SigninUser(models.Model):
#     username = models.CharField(max_length=50)
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     password = models.CharField(max_length=128)
#     image = models.ImageField(upload_to='images/', default="% static {'img/profile_default_img.jpg'} %")


class SigninUser(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    VEG_NONVEG_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
    ]

    STATE_CHOICES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
    ]
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128, null=True, blank=True)
    gender = models.CharField(
        max_length=100, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    veg_nonveg = models.CharField(
        max_length=100, choices=VEG_NONVEG_CHOICES, null=True, blank=True)
    state = models.CharField(
        max_length=200, choices=STATE_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    uploaded_image = models.ImageField(
        upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.username


class Contact(models.Model):  # Rename the model class to Contact
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(
        max_length=700, default='Your default message here')

    # message = models.CharField(max_length=700)  # Rename this field to 'message'

    def __str__(self):
        return self.name


class NutritionModel(models.Model):
    age_group = models.CharField(max_length=500)
    calories_per_kg = models.CharField(max_length=500)
    protein = models.CharField(max_length=500)
    fat = models.CharField(max_length=500)
    carbohydrates = models.CharField(max_length=500)
    calcium = models.CharField(max_length=500)
    vitamin_d_iu = models.CharField(max_length=500)
    fiber = models.CharField(max_length=500)
    iron = models.CharField(max_length=500)
    minerals = models.CharField(max_length=500)
    nutrient_ratios = models.CharField(max_length=500)
    meal_frequency_level = models.CharField(max_length=500)
    adjustments_for_physical_activity = models.CharField(max_length=500)
    dynamic_updates = models.CharField(max_length=500)
    water_consumption = models.CharField(max_length=500)

    def __str__(self):
        return self.age_group


class MealInstructionModel(models.Model):
    required_meal_age = models.CharField(max_length=50)
    meal_instructions = models.TextField()

    def __str__(self):
        return f'{self.required_meal_age} Meal Instructions'