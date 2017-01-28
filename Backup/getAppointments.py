'''
Created on Sep 3, 2016

@author: Igor Dean
This class is not currently used. For relevant code look into views.py
'''
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.db import connection   
from django.core import serializers
from .models import Appointment

class AppointmentsHandler(object):
     
    def __init__(self):
        self.searches = []
        
    def __str__(self):
        return self.data
    
    def getAppointmets(self, request):
        if(request.method == 'POST'):
            format_date = getattr(self, "_reformat_date") 
            date = format_date(request.POST.get('date', ''))
            if(date is None): 
                print("DATE is Missing")
            
            time = request.POST.get('time', '')
            if(not time): 
                print("TIME is Missing")
            
            desc = request.POST.get('desc', '')
            if(not desc): 
                print("DESCRIPTION is Missing")
            
            if(date and time and desc):
                print ("Saving Record: " + date +' '+ time +' '+ desc)
                cost_obj = Appointment(appointment_text=desc, appointment_date=(date +' '+ time))
                cost_obj.save()
            else:
                print("Record is Not saved!")  
                       
        else:
            
            if request.is_ajax():
                print ("++++++AJAX Call++++++")
                #Always use get on request.POST. Correct way of querying a QueryDict.
                searchStr = request.GET.get('search','')  
                print ("=>Searching for "+searchStr)  
                getAppointmentsData = getattr(self, "getAppointmentsData")   
                data = getAppointmentsData(searchStr)    
                #Returning same data back to browser.It is not possible with Normal submit
                return JsonResponse(data, safe=False)
            
        #Sort Appointments by Date    
        applist = Appointment.objects.order_by('appointment_date')[:50]
        template = loader.get_template('appointmentsApp/index.html')
        context = { 'apt_list': applist, }
            
        return HttpResponse(template.render(context, request))    
    #        form = AddAptForm()

    # Retrieves data from database via DJango model and returns it as JSON doc.
    def getAppointmentsData(self, searchStr):
    
        if( not(searchStr is None)):
            print("=> getting appointments where description field contains \""+searchStr+"\"")
            getDataViaDbConnection = getattr(self, "getDataViaDbConnection")
            data = getDataViaDbConnection(searchStr)
            data = Appointment.objects.filter(appointment_text__icontains=searchStr)
    
            print(data.values("appointment_date", "appointment_text"))
        else:
            print("=> search string is empty. getting all appointments")
            data = Appointment.objects.all()
        #convert data into JSON format
        json_data = serializers.serialize("json", data)
        return json_data
    
    #Move year from end of the string to front and replace '/' delimiters with '-' char
    def _reformat_date(self, date):
        if(not date):
            return None
        temp = date.split("/")
        temp.insert(0, temp.pop(2))
        return '-'.join(temp)  
    
    # Retrieves data thru DJango DB connection object. Note: not used in this program.
 
    def getDataViaDbConnection(self, searchStr):
        query = "SELECT appointment_date, appointment_text FROM appointmentsApp_appointment WHERE appointment_text LIKE '%"+searchStr+"%'"
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()            

    def _saveSearch(self, searchString):
        if(searchString is None):
            print ("Empty String")
        else:
            self.searches.append(searchString)
            print ("searchString="+searchString)

