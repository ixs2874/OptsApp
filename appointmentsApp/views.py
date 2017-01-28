'''
Created on Sep 2, 2016

@author: Igor Dean
'''
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from .models import Appointment
#from .getAppointments import AppointmentsHandler 

   
#Process both HTML Form and AJAX requests         
def index(request):
    print ("Processing " + request.method + " request.")
    
    #handler = getattr(AppointmentsHandler(), "getAppointmets")
    #handler(request)
    
    if(request.method == 'POST'):
        
        date = _reformat_date(request.POST.get('date', ''))
        if(date is None): 
            print("DATE is Missing")
        
        time = request.POST.get('time', '')
        if(not time): 
            print("TIME is Missing")
        
        desc = request.POST.get('desc', '')
        dup = False
        if(not desc): 
            print("DESCRIPTION is Missing")
        else: #workaround of duplicated form submission on page reload
            dt = date +' '+ time  +':00'
            res = getDataViaDbConnection(desc, dt)
            if(len(res) > 0):
                dup = True
                print("DUPLICATE ENTRY")
            
        if(date and time and desc and not dup):
            date_time = date +'T'+ time  +'-04:00'
            print ("Saving Record: Datetime: '" + date_time +"' Description: " + desc)
            appointment_obj = Appointment(appointment_text=desc, appointment_date=date_time)
            appointment_obj.save()
        else:
            print("Record is Not saved!")  
                   
    else:      
        if request.is_ajax():
            print ("++++++AJAX Call++++++")
            #Always use get on request.POST. Correct way of querying a QueryDict.
            searchStr = request.GET.get('search','')  
            print ("=>Searching for ' "+searchStr+" '")     
            data = getAppointmentsData(searchStr)    
            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse(data, safe=False)
        
    #Sort Appointments by Date    
    applist = Appointment.objects.order_by('appointment_date')[:50]
    template = loader.get_template('appointmentsApp/index.html')
    context = { 'apt_list': applist, }
        
    return HttpResponse(template.render(context, request))    

# Retrieves data from database via DJango model and returns it as JSON doc.
from django.core import serializers
def getAppointmentsData(searchStr):

    if( not(searchStr is None)):
        print("=>Select appointments WHERE description contains \""+searchStr+"\"")
        #data = getDataViaDbConnection(searchStr)
        data = Appointment.objects.filter(appointment_text__icontains=searchStr).order_by('appointment_date')[:50]

        #print(data.values("appointment_date", "appointment_text"))
    else:
        print("=>Select all appointments and sort by appointment date")
        data = Appointment.objects.all().order_by('appointment_date')[:50]
    #convert data into JSON format
    json_data = serializers.serialize("json", data)
    return json_data

#Move year from end of the string to front and replace '/' delimiters with '-' char
def _reformat_date(date):
    if(not date):
        return None
    temp = date.split("/")
    temp.insert(0, temp.pop(2))
    return '-'.join(temp)  

# Retrieves data thru DJango DB connection object. Note: not used in this program.
from django.db import connection    
def getDataViaDbConnection(searchStr, datetime):
    query = "SELECT appointment_text FROM appointmentsApp_appointment WHERE appointment_text LIKE '%"+searchStr+"%'"
    # AND appointment_date = '"+datetime+"'"
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()
    

