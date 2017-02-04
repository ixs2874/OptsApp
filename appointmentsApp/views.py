"""
Created on Sep 2, 2016

@author: Igor Dean
"""

import logging
from datetime import datetime

from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.db import connection
from django.core import serializers

from .models import Appointment
   
log = logging.getLogger(__name__)


def index(request):
    """Process both HTML Form and AJAX requests

    :param request: HTTP request to be processed.
    :return: HTTP or JSON Response.
    """
    log.info("Processing {} request.".format(request.method))
    
    if request.method == 'POST':

        date = _reformat_date(request.POST.get('date', ''))
        time = request.POST.get('time', '')
        desc = request.POST.get('desc', '')
        dup = False

        if date is None:
            log.info("DATE is Missing")
        if not time:
            log.info("TIME is Missing")
        if not desc:
            log.info("DESCRIPTION is Missing")
        else:  # workaround for duplicate form submission on page reload
            dt = datetime.strptime("{} {}:00".format(date, time), "%Y-%m-%d %H:%M:%S")
            if _is_duplicate(desc.strip(), dt):
                dup = True
                log.info("DUPLICATE ENTRY")

        if date and time and desc and not dup:
            date_time = datetime.strptime("{} {}:00".format(date, time), "%Y-%m-%d %H:%M:%S")
            log.info("Saving Record: Datetime: '{}' Description: {}".format(date_time, desc.strip()))
            appointment_obj = Appointment(appointment_text=desc.strip(), appointment_date=date_time)
            appointment_obj.save()
        else:
            log.info("Record is Not saved!")
    else:      
        if request.is_ajax():
            log.info("++++++AJAX Call++++++")
            # Always use get on request.POST. Correct way of querying a QueryDict.
            search_str = request.GET.get('search')
            if search_str is not None:
                search_str = search_str.strip()
                log.info("Searching for '{}'".format(search_str))

            data = _get_appointments_data(search_str)
            # Returning same data back to browser. It is not possible with Normal submit
            return JsonResponse(data, safe=False)

    # Get first 50 appointments sorted by Date.
    applist = Appointment.objects.order_by('appointment_date')[:50]
    template = loader.get_template('appointmentsApp/index.html')
    context = {'apt_list': applist, }
        
    return HttpResponse(template.render(context, request))    


def _get_appointments_data(searchStr):
    """Gets first 50 records of the search result ordered by appointment date.

    Retrieves data from database via Django model and returns it as JSON doc.
    :param searchStr: String to search for.
    :return: Serialized result set in json format.
    """

    if searchStr is not None:
        log.info("Select appointments WHERE description contains '{}'".format(searchStr))
        data = Appointment.objects.filter(appointment_text__icontains=searchStr).order_by('appointment_date')[:50]
    else:
        log.info("Select all appointments and sort by appointment date")
        data = Appointment.objects.all().order_by('appointment_date')[:50]

    # convert data into JSON format
    json_data = serializers.serialize("json", data)
    return json_data


def _reformat_date(date):
    """Formats the date string.

    Move year from end of the string to front and replace '/' delimiters with '-' char.
    :param date: The date to be formatted.
    :return: The date as string.
    """

    if not date:
        return None
    temp = date.split("/")
    temp.insert(0, temp.pop(2))
    return '-'.join(temp)  


def _is_duplicate(searchStr, datetime):
    """Performs search of the appointment text in the appointments table by given string.

    Retrieves data thru Django DB connection object. Note: not used in this program.
    :param searchStr: String to be serched for.
    :param datetime: Date to be searched by.
    :return: List of records containing the search string.
    """
    query = "SELECT appointment_text FROM appointmentsApp_appointment " \
            "WHERE appointment_text LIKE '%{}%' " \
            "AND appointment_date = '{}'".format(searchStr, datetime)

    cursor = connection.cursor()
    cursor.execute(query)
    return bool(len(cursor.fetchall()) > 0)
