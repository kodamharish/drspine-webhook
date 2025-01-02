from django.db import models

# Create your models here.




from datetime import timezone
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class SuperAdmin(models.Model):
    sa_full_name = models.CharField(max_length=25)
    sa_email = models.EmailField()
    sa_username = models.CharField(max_length=25, unique=True, primary_key=True)
    sa_password = models.CharField(max_length=255)  # Ensure length to accommodate hashed password

    def __str__(self):
        return self.sa_username

    def save(self, *args, **kwargs):
        if not self.pk or not self._is_password_hashed():
            self.sa_password = make_password(self.sa_password)
        super().save(*args, **kwargs)

    def _is_password_hashed(self):
        current_password = self._get_current_password()
        if current_password:
            return check_password(self.sa_password, current_password)
        return False

    def _get_current_password(self):
        if self.pk:
            try:
                return SuperAdmin.objects.get(pk=self.pk).sa_password
            except SuperAdmin.DoesNotExist:
                return None
        return None


class Company(models.Model):
    company_id = models.CharField(max_length=10, primary_key=True, editable=False)
    company_name = models.CharField(max_length=50)
    company_email = models.EmailField(unique=True)
    company_wa_number = models.CharField(max_length=15, unique=True)
    company_address = models.TextField()
    company_logo = models.ImageField(upload_to='Company_Logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook_link = models.TextField(blank=True, null=True)
    industry_type = models.CharField(max_length=255, blank=True, null=True)
    number_of_employees = models.PositiveIntegerField(blank=True, null=True)
    gst_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.company_name

    def generate_company_id(self):
        prefix = "iQ"
        latest_company = Company.objects.all().order_by('company_id').last()
        if not latest_company:
            new_id = f"{prefix}001"
        else:
            latest_id = latest_company.company_id
            latest_number = int(latest_id.replace(prefix, ''))
            new_number = latest_number + 1
            new_id = f"{prefix}{new_number:03d}"
        return new_id

    def save(self, *args, **kwargs):
        if not self.company_id:
            self.company_id = self.generate_company_id()
        super().save(*args, **kwargs)

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    USER_ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User')
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email_id = models.EmailField()
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=255)
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='Admin')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk or not self._is_password_hashed():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def _is_password_hashed(self):
        current_password = self._get_current_password()
        if current_password:
            return check_password(self.password, current_password)
        return False

    def _get_current_password(self):
        try:
            return User.objects.get(pk=self.pk).password
        except User.DoesNotExist:
            return None


class Template(models.Model):
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, primary_key=True)
    language = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    template_type = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name


class WhatsApp_Group(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=200, unique=True)
    group_description = models.TextField()

    def __str__(self):
        return self.group_name



class Group_Contacts(models.Model):
    group = models.ForeignKey(WhatsApp_Group, related_name='numbers', on_delete=models.CASCADE)
    number = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=25, null=True)
    email = models.EmailField(null=True)
    company_name = models.CharField(max_length=50, null=True)

    class Meta:
        unique_together = ('group','number', 'email')
    
    def __str__(self):
        return self.number


class MessageLog(models.Model):
    template_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Sent', 'Sent'), ('Delivered', 'Delivered'), ('Read', 'Read'), ('Failed', 'Failed')])
    response_received = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mobile_number} - {self.status} - {self.timestamp}"

    

