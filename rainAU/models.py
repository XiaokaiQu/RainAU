from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

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
    id = models.UUIDField(primary_key = True)
    location = models.CharField(
        max_length = 20,
        choices = LOCATION_CHOICES,
        default = '0'
    )
    record_date = models.CharField(max_length=200)
    MinTemp = models.CharField(max_length=200)
    MaxTemp = models.CharField(max_length=200)
    Rainfall = models.CharField(max_length=200)
    RainToday = models.BooleanField()
    RainTomorrow = models.BooleanField()

    def __str__(self):
        """String for representing the Model object."""
        return self.location + ' ' + self.record_date

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])
