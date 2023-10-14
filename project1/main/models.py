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
 

class SigninUser(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/', default="% static {'img/profile_default_img.jpg'} %")

    def __str__(self):
        return self.username


class Contact(models.Model):  # Rename the model class to Contact
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=700, default='Your default message here')

    # message = models.CharField(max_length=700)  # Rename this field to 'message'

    def __str__(self):
        return self.name
