from django.shortcuts import render
from .models import SpeedGovernorCertificate


def certificates_list(request):
    certificates = SpeedGovernorCertificate.objects.all()
    return render(request, 'certificates_list.html', {'certificates': certificates})
