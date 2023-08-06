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
