Application was written in Eclipse IDE using PyDev plug-in. 
I used Django for web application framework and SQLite for database.
Application is packaged into AppointmentsApp.zip. Database table with some test data is included.

Application home: 
   SimpleAppointmentWebApp/appointmentsApp/

Main code files:

  Server side files:
  1. SimpleAppointmentWebApp/appointmentsApp/views.py
  2. SimpleAppointmentWebApp/appointmentsApp/models.py

  Client side files:
  1. SimpleAppointmentWebApp/appointmentsApp/static/igor-appointment-app-scripts.js
  2. SimpleAppointmentWebApp/appointmentsApp/templates/appointmentsApp/index.html
  
How to use:
1. Install Python (latest Anaconda is recommended), Sqlite DB, and Django. Set PATH env.
2. Unzip  Igor_AppointmentsApp.zip to local directory. Changed to unzipped directory.
3. Startup the server: 
     $ python manage.py runserver
4. Open new browser window and navigate to:  
     http://localhost:8000/app/
5. Also you can navigate to server admin page
     http://localhost:8000/admin/         appadmin/welcome1
     http://localhost:8000/admin/appointmentsApp/appointment/   <--- you can delete records from db here 

QUESTIONS/ANSWERS
1. Did you follow directions?
Yes, I followed directions and requirements described in Job_Application_ Std Dev_Python_Sqllite.txt

2. Did you test out the code? 
Application was tested. All the requirements are met. I attached the snapshots of the application views. 
  AppointmentApp_Snap1.png  1 thru 6

3. How much effort is put into the project?
Overall development and testing took around 9 hours including environment setup.  

Encountered issues:
1. Timezone issues storing DateTime field into SQLIte DB and then displaying it in the Form - resolved
2. CSRF token verification at form submission and AJAX call                                 - resolved
3. Formating date in javascript. Date.format function is not native method in javascript. 
   Several date/time plug-ins were used before finding the one that works.                  - resolved
4. A few issue with correct formation and parsing JSON data.                                - resolved
5. Issue with resubmitting the latest form at page reload. 
   Initially page loads correctly using GET method. 
   But after Forms POST if page reload is clicked, the browser submits latest POST request, 
   while it should use GET. The work around was done on server side by querying relevant 
   DB table and preventing submissions with the same Appointment Text.                      - workaround

Initially application used static table populated by Django server and Search used AJAX dynamic table. 
The tables where displayed by hide/show trigger one at the time.
Later, static table was removed; it is quoted out in HTML file. 
Currently, only AJAX, JSON, and Javascript are used to display data in table format on HTML page.  

  
