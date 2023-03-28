from django.db import models
from auths.models import *
from datetime import date
from django.utils import timezone
# Create your models here.

GENDER_CHOICES = {
    ('Man', 'Man'),
    ('Kvinna', 'Kvinna')
}

STATUS_CHOICES = [
    ('Föredrar att inte säga', 'prefer_not_to_say'),
    ('Singel', 'single'),
    ('Gift', 'married'),
    ('Skild', 'divorced'),
    ('Separerat', 'separated'),
    ('Änka', 'widowed'),
    ('Komplicerat', 'complicated'),
    ('Sambo', 'cohabitant'),
    ('Särbo', 'separate'),
]

# COUNTY_CHOICES = [
#     ('Blekinges', 'Blekinges'),
#     ('Dalarnas', 'Dalarnas'),
#     ('Gotlands', 'Gotlands'),
#     ('Gävleborgs', 'Gävleborgs'),
#     ('Hallands', 'Hallands'),
#     ('Jämtlands', 'Jämtlands'),
#     ('Kalmar', 'Kalmar'),
#     ('Kronobergs', 'Kronobergs'),
# ]

HAIR_COLOR_CHOICES = [
    ('Ej angivet', 'Ej angivet'),
    ('Mörkbrun', 'Mörkbrun'),
    ('Ljusbrun', 'Ljusbrun'),
    ('Svart', 'Svart'),
    ('Blond', 'Blond'),
    ('Grå', 'Grå'),
    ('Röd', 'Röd'),
    ('Inte angivet', 'Inte angivet'),
]

EYE_COLOR_CHOICES = [
    ('Ej angivet', 'Ej angivet'),
    ('Brun', 'Brun'),
    ('Svart', 'Svart'),
    ('Grå', 'Grå'),
    ('Annat', 'Annat'),
]


class Girl(models.Model):
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, default='Kvinna', max_length=10)
    seeking = models.CharField(choices=GENDER_CHOICES, default='Man', max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, default='Föredrar att inte säga', max_length=30)
    county = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    hair_color = models.CharField(max_length=30, default='Ej angivet')
    eye_color = models.CharField(max_length=30, default='Ej angivet')
    smoking_habit = models.CharField(max_length=30, default='Ej angivet')
    drinking_habit = models.CharField(max_length=30, default='Ej angivet')
    sexual_position = models.CharField(max_length=30, default='Ej angivet')
    ethnicity = models.CharField(max_length=30, default='Ej angivet')
    children = models.CharField(max_length=30, default='Ej angivet')
    body_type = models.CharField(max_length=30, default='Ej angivet')
    height = models.CharField(max_length=10, blank=True, null=True)
    about_me = models.TextField()
    online = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    def photo(self):
        first_photo = GirlPhoto.objects.filter(girl=self, private=False).first()
        return first_photo

    def age(self):
        today = date.today()
        return  self.birthday

    def matches(self):
        query = GirlLike.objects.filter(girl=self, user_like=1, girl_like=1).all()
        return len(query)


class GirlPhoto(models.Model):
    girl = models.ForeignKey(Girl, on_delete=models.CASCADE, related_name='profile_photos', blank=True, null=True)
    photo = models.FileField(upload_to='model')
    private = models.BooleanField(default=False)


class GirlLike(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='likedGirls')
    girl = models.ForeignKey(Girl, on_delete=models.CASCADE, related_name='likedUsers')
    user_like = models.BooleanField(default=False)
    girl_like = models.BooleanField(default=False)


class Notification(models.Model):
    receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='notification', null=True, blank=True)
    type = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)
