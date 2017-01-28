from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Appointment, AddAptForm
#from .models import Genre 

from .getAppointments import AppointmentsHandler 
from django.http import JsonResponse
import json
from django.http.request import QueryDict


def _reformat_date(date):
    if(not date):
        return None
    temp = date.split("/")
    temp.insert(0, temp.pop(2))
    return '-'.join(temp)  
        
def index(request):
    print ("Processing " + request.method)
    if(request.method == 'POST'):
#        form = AddAptForm(request.POST)
#        if form.is_valid():
#        AppointmentsHandler.getAppointmets("werere")
#----------------------------------------  
        if request.is_ajax():
            print ("++++++'%AJAX Call%'++++++")
            #Always use get on request.POST. Correct way of querying a QueryDict.
            searchStr = request.POST.get('search','') 
            #searchStr2 = QueryDict((request.body).get('search')) 
            print ("--+"+searchStr +"+--"+searchStr+"++++++")       
#            password = request.POST.get('password')    
            data = getAppointmentsData(request, searchStr)       
            #data = {"searchString":searchStr , "password" : "dinocat"}
            #Returning same data back to browser.It is not possible with Normal submit
            #Appointment.objects.values('appointment_date','appointment_text')
            #return HttpResponse(data, content_type='application/json') 
            return JsonResponse(data, safe=False)
#----------------------------------------    
        date = _reformat_date(request.POST.get('date', ''))
        if(date is None):
            print("DATE is Missing")
        time = request.POST.get('time', '')
        if(not time):
            print("TIME is Missing")
        desc = request.POST.get('desc', '')
        if(not desc):
            print("DESCRIPTION is Missing")
        if(date != None and time != None and desc != None):
            print ("Saving Record: " + date +' '+ time +' '+ desc)
            cost_obj = Appointment(appointment_text=desc, appointment_date=(date +' '+ time))
            cost_obj.save()
        else:
            print("Record is Not saved!")  
                   
        applist = Appointment.objects.order_by('appointment_date')[:50]
        template = loader.get_template('appointmentsApp/index.html')
        context = { 'apt_list': applist, }
        
        return HttpResponse(template.render(context, request))    
    else:
        print ("----"+request.GET.get('search', '')+"======")
        if request.is_ajax():
            print ("++++++AJAX Call++++++")
            #Always use get on request.POST. Correct way of querying a QueryDict.
            searchStr = request.GET.get('search')           
            password = request.POST.get('password')           
            data = {"searchString":"Igor" , "password" : "dinocat"}
            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse(data, safe=False)
        
        
        applist = Appointment.objects.order_by('appointment_date')[:50]
        template = loader.get_template('appointmentsApp/index.html')
        context = { 'apt_list': applist, }
        
        return HttpResponse(template.render(context, request))    
#        form = AddAptForm()


def ajax(request):
    data = {}
    data['something'] = 'useful'
    return HttpResponse(json.dumps(data), content_type = "application/json")
#--------------------------------------------------
from django.core import serializers
from django.db import connection
import logging
#--------------------------------------------------
def getAppointmentsData(request, searchDesc):
    print("in ** getAppointmentsData  searchFor "+searchDesc)
    logger = logging.getLogger(__name__)
    cdata = request.body
    logger.debug('json data received(%s)' % cdata)
    if( not(searchDesc is None)):
        print("getting appointments where description field contains \""+searchDesc+"\"")
        cursor = connection.cursor()
        #print("1 "+cursor)
        #cursor.execute("select appointment_date, appointment_text from Appointment where appointment_text LIKE %"+searchDesc+"%")
        cursor.execute("select appointment_date, appointment_text from appointmentsApp_appointment where appointment_text LIKE '%"+searchDesc+"%'")
        print("2")
        data = cursor.fetchall()
        print(data)
        data = Appointment.objects.filter(appointment_text__icontains="Dentis")
        print("2.5")
        datax = data.values("appointment_date", "appointment_text")
        print(datax)
        print("3")
    else:
        print("getting all appointments data")
        data = Appointment.objects.all()
     
    print("4")   
    json_data = serializers.serialize("json", data)
    print("json_data="+json_data)
    print("5")
    return json_data
    #return HttpResponse(json_data, content_type='application/json')

#class PostForm(forms.ModelForm):
#    class Meta:
#        model = Post
        # exclude = ['author', 'updated', 'created', ]
#        fields = ['text']
#        widgets = {
#            'text': forms.TextInput(
#                attrs={'id': 'post-text', 'required': True, 'placeholder': 'Say something...'}
#            ),
#        }
