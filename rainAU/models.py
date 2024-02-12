from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid

# Location choices
LOCATION_CHOICES = (
    ('0', 'Unknown'),
    ('1', 'Albury'), 
    ('2', 'BadgerysCreek'), 
    ('3', 'Cobar'), ('4', 'CoffsHarbour'), 
    ('5', 'Moree'), 
    ('6', 'Newcastle'), 
    ('7', 'NorahHead'), 
    ('8', 'NorfolkIsland'), 
    ('9', 'Penrith'), 
    ('10', 'Richmond'), 
    ('11', 'Sydney'), 
    ('12', 'SydneyAirport'), 
    ('13', 'WaggaWagga'), 
    ('14', 'Williamtown'), 
    ('15', 'Wollongong'), 
    ('16', 'Canberra'), 
    ('17', 'Tuggeranong'), 
    ('18', 'MountGinini'), 
    ('19', 'Ballarat'), 
    ('20', 'Bendigo'), 
    ('21', 'Sale'), 
    ('22', 'MelbourneAirport'), 
    ('23', 'Melbourne'), 
    ('24', 'Mildura'), 
    ('25', 'Nhil'), 
    ('26', 'Portland'), 
    ('27', 'Watsonia'), 
    ('28', 'Dartmoor'), 
    ('29', 'Brisbane'), 
    ('30', 'Cairns'), 
    ('31', 'GoldCoast'), 
    ('32', 'Townsville'), 
    ('33', 'Adelaide'), 
    ('34', 'MountGambier'), 
    ('35', 'Nuriootpa'),
    ('36', 'Woomera'), 
    ('37', 'Albany'), 
    ('38', 'Witchcliffe'), 
    ('39', 'PearceRAAF'), 
    ('40', 'PerthAirport'), 
    ('41', 'Perth'), 
    ('42', 'SalmonGums'), 
    ('43', 'Walpole'), 
    ('44', 'Hobart'), 
    ('45', 'Launceston'), 
    ('46', 'AliceSprings'), 
    ('47', 'Darwin'), 
    ('48', 'Katherine'), 
    ('49', 'Uluru'),
)

class RainInAu(models.Model):
    id = models.UUIDField(
        primary_key = True, 
        default=uuid.uuid4, 
        editable=False
    )
    location = models.CharField(
        verbose_name='location',
        max_length = 20,
        choices = LOCATION_CHOICES,
        default = '0'
    )
    record_date = models.CharField(verbose_name='recordDate', max_length=200, null=True)
    MinTemp = models.DecimalField(verbose_name='mintemp', max_digits=20, decimal_places=1, null=True)
    MaxTemp = models.DecimalField(verbose_name='maxtemp', max_digits=20, decimal_places=1, null=True)
    Rainfall = models.DecimalField(verbose_name='rainfall', max_digits=20, decimal_places=1, null=True)
    Evaporation = models.CharField(verbose_name='evaporation',max_length=200, null=True)
    Sunshine = models.CharField(verbose_name='sunshine',max_length=200, null=True)
    WindGustDir = models.CharField(verbose_name='windGustDir',max_length=200, null=True)
    WindGustSpeed= models.DecimalField(verbose_name='windGustSpeed', max_digits=20, decimal_places=1, null=True)
    WindDir9am= models.CharField(verbose_name='windDir9am',max_length=200, null=True)
    WindDir3pm= models.CharField(verbose_name='windDir3pm',max_length=200, null=True)
    WindSpeed9am= models.DecimalField(verbose_name='windSpeed9am', max_digits=20, decimal_places=1, null=True)
    WindSpeed3pm= models.DecimalField(verbose_name='windSpeed3pm', max_digits=20, decimal_places=1, null=True)
    Humidity9am= models.DecimalField(verbose_name='humidity9am', max_digits=20, decimal_places=1, null=True)
    Humidity3pm= models.DecimalField(verbose_name='Humidity3pm', max_digits=20, decimal_places=1, null=True)
    Pressure9am= models.DecimalField(verbose_name='pressure9am', max_digits=20, decimal_places=1, null=True)
    Pressure3pm= models.DecimalField(verbose_name='Pressure3pm', max_digits=20, decimal_places=1, null=True)
    Cloud9am= models.DecimalField(verbose_name='cloud9am', max_digits=20, decimal_places=1, null=True)
    Cloud3pm= models.DecimalField(verbose_name='cloud3pm', max_digits=20, decimal_places=1, null=True)
    Temp9am= models.DecimalField(verbose_name='temp9am', max_digits=20, decimal_places=1, null=True)
    Temp3pm= models.DecimalField(verbose_name='temp3pm', max_digits=20, decimal_places=1, null=True)
    RainToday = models.BooleanField(verbose_name='rainToday', null=True)
    RainTomorrow = models.BooleanField(verbose_name='rainTomorrow', null=True)

    class Meta:
        indexes = [models.Index(fields=['location',]),]

    def __str__(self):
        """String for representing the Model object."""
        return self.location + ' ' + self.record_date

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])
