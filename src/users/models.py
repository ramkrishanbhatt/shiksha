from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# class User(AbstractBaseUser, PermissionsMixin):


class User(AbstractUser, PermissionsMixin):
    username = None  # Remove username field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("Email address"), unique=True)
    first_name = models.CharField(_("First name"), max_length=30, blank=True)
    last_name = models.CharField(_("Last name"), max_length=30, blank=True)
    address = models.CharField(_("address"), max_length=200, blank=True)
    phone = models.CharField(_("Contact Number"), max_length=100, blank=True)
    language = models.CharField(_("Language Preferred"), max_length=100, blank=True)
    area = models.CharField(_("area"), max_length=100, blank=True)
    city = models.CharField(_("city"), max_length=100, blank=True)
    state = models.CharField(_("state"), max_length=100, blank=True)
    zip = models.IntegerField(_("zip Code"), default=0)

    # Permissions
    is_active = models.BooleanField(_("Is active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_superuser = models.BooleanField(_("Is admin"), default=False)

    # Meta
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class TeacherSchedule(models.Model):
    schedule_date = models.DateTimeField(_("Schedule Date"))
    language = models.CharField(_("Language Preferred"), max_length=100, blank=True)
    area = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.IntegerField(_("Zip Code"), default=0)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # hjkk

    def __str__(self):
        return self.language


class TeacherInform(models.Model):
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    contact = models.CharField(_("Contact Number"), max_length=100, blank=True)
    informed_on = models.DateField(_("Informed On"), auto_now_add=True)

    def __str__(self):
        return self.name


class Donation(models.Model):
    donor_name = models.CharField(_("Donor Name"), max_length=100, blank=True)
    donation_date = models.DateField(_("Donation date"))
    donation_item = models.CharField(_("Donation Item"), max_length=100, blank=True)
    donation_amount = models.CharField(_("Donation Amount"), max_length=100, blank=True)
    donated_to = models.CharField(_("Donated To"), max_length=100, blank=True)
    donated_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # hhggh

    def __str__(self):
        return self.donor_name


class Page(models.Model):
    title = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # ghgsd

    def __str__(self):
        return self.title


class Comment(models.Model):
    page_id = models.ForeignKey(Page, null=True, on_delete=models.SET_NULL)
    experience = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(_("created_on"), auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.experience
