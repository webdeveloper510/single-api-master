from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date
from Admin.models import Setting

from datetime import datetime
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


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, default='user')

    county = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)

    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, default='Kvinna', max_length=10)
    seeking = models.CharField(choices=GENDER_CHOICES, default='Man', max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, default='Föredrar att inte säga', max_length=30)
    hair_color = models.CharField(max_length=30, default='Ej angivet')
    eye_color = models.CharField(max_length=30, default='Ej angivet')
    smoking_habit = models.CharField(max_length=30, default='Ej angivet')
    drinking_habit = models.CharField(max_length=30, default='Ej angivet')
    sexual_position = models.CharField(max_length=30, default='Ej angivet')
    ethnicity = models.CharField(max_length=30, default='Ej angivet')
    children = models.CharField(max_length=30, default='Ej angivet')
    body_type = models.CharField(max_length=30, default='Ej angivet')
    height = models.CharField(max_length=10, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    objects = UserAccountManager()

    registered_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    online_s = models.BooleanField(default=False)
    online = models.IntegerField(default=0)

    avatar = models.FileField(upload_to='customer', default='default_avatar.png')
    coins = models.IntegerField(null=True, blank=True)
    ip_address = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-registered_at']
        verbose_name = 'Account'

    def age(self):
        today = date.today()
        if self.birthday:
            return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        else:
            ''

    def save(self, *args, **kwargs):
        print('self._state.adding', self._state.adding)
        if self._state.adding:
            admin_setting = Setting.objects.first()
            if not admin_setting:
                admin_setting = Setting()
                admin_setting.save()
            self.coins = admin_setting.start_coins
        super(UserAccount, self).save(*args, **kwargs)

    def affiliated_customers(self):
        affiliated_customers = []
        for item in self.affiliate_customer.all():
            affiliated_customers.append(item.customer)
        return affiliated_customers


class Affiliate(models.Model):
    customer = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='affiliate_moderator')
    moderator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='affiliate_customer')


class ModeratorSetting(models.Model):
    moderator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='moderator_setting')
    message = models.DecimalField(max_digits=5, decimal_places=2, default='0.16')
    affiliate = models.IntegerField(default=35)

    # def messages_today(self):
    #     messages = len(Message.objects.filter(senderType='model', sender=self.moderator, timestamp__year=today.year,
    #                                           timestamp__month=today.month).all())


class Transactions(models.Model):
    customer = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

 