from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class LotteryUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_confirmed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)
    free_raffle = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = LotteryUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)

    TYPE_CHOICES = [
        ('success', 'Success'),
        ('fail', 'Fail'),
        ('info', 'Info')
    ]

    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    link = models.URLField()

    def __str__(self):
        return f"{self.user.email} - notification"


class DiscountPeriod(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='discount_periods')
    end_date = models.DateField()
    discount_percentage = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.email} - Discount Period (to {self.end_date})"


class LotteryType(models.Model):
    name = models.CharField(max_length=50)
    # refresh_date = models.DateField()
    number_of_digits = models.IntegerField()
    current_number = models.CharField(max_length=12)
    draw_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class OrderKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - OrderKey - {self.key}"


class WinningType(models.Model):
    STRAIGHT = 'straight'
    RUMBLE = 'rumble'
    NAME_CHOICES = [
        (STRAIGHT, 'Straight'),
        (RUMBLE, 'Rumble'),
    ]
    LABEL_CHOICES = [
        ('first', 'First Prize'),
        ('second', 'Second Prize'),
        ('normal', 'Normal Prize')
    ]

    lottery_type = models.ForeignKey(LotteryType, on_delete=models.CASCADE)
    # number_of_digits = models.PositiveIntegerField()
    name = models.CharField(max_length=10, choices=NAME_CHOICES)
    prize = models.DecimalField(max_digits=8, decimal_places=2)
    # weekly_increment_amount = models.DecimalField(
    #     max_digits=8, decimal_places=2, default=0)
    # limit_amount = models.DecimalField(
    #     max_digits=8, decimal_places=2, default=0)
    # overflow_amount = models.DecimalField(
    #     max_digits=8, decimal_places=2, default=0)
    # single_user_win = models.BooleanField(default=False)
    # label = models.CharField(max_length=10, choices=LABEL_CHOICES)

    def __str__(self):
        return f"{self.lottery_type} - {self.get_name_display()}"


class Order(models.Model):
    order_key = models.ForeignKey(OrderKey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lottery_type = models.ForeignKey(LotteryType, on_delete=models.CASCADE)
    bet_digits = models.CharField(max_length=50, default='00')
    won_prize_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    # won_prize_name = models.CharField(max_length=50, blank=True, null=True)
    winning_type = models.CharField(max_length=50, blank=True, null=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Order ({self.lottery_type.name})"


class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.email} - {self.phone}"


class TermAndCondition(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Term and Condition'


class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Privacy policy'


class AboutUs(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'About Us'


class SocialMediaLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name
