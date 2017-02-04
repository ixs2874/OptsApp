'''
Created on Sep 2, 2016

@author: Igor Dean
'''

import datetime
from django.db import models
from django.utils import timezone
from django.forms.models import ModelForm

class Appointment(models.Model):
    
    appointment_text = models.CharField(max_length=200)
    appointment_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.appointment_text
    
    def time_to_appointment(self):
        return self.appointment_date >= timezone.now() - datetime.timedelta(days=1)
    
class AddAptForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_text']