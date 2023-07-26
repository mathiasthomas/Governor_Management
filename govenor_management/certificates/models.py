from django.db import models
from datetime import timedelta, date
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    physical_location = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name


class SpeedGovernorCertificate(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='certificates')
    vehicle_registration_number = models.CharField(max_length=20)
    brand = models.CharField(max_length=100)
    chassis_number = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=100)
    certificate_number = models.CharField(max_length=50)
    date_fitted = models.DateField()
    expiry_date = models.DateField(editable=False)  # Make the field read-only in admin
    certificate_status = models.BooleanField(default=True)

    def __str__(self):
        return f"Speed Governor Certificate for {self.vehicle_registration_number}"

    @property
    def calculate_expiry_date(self):
        return self.date_fitted + timedelta(days=365)


@receiver(pre_save, sender=SpeedGovernorCertificate)
def pre_save_expiry_date(sender, instance, **kwargs):
    instance.expiry_date = instance.calculate_expiry_date
    # Update certificate_status based on expiry_date
    if date.today() > instance.expiry_date:
        instance.certificate_status = False  # Certificate is expired
    else:
        instance.certificate_status = True  # Certificate is active
