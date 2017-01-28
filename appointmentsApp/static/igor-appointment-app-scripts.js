/** 
Created on Sep 3, 2016
@author: Igor Dean
*/

//Retrieves appointments via AJAX call
function getAppointments(searchString){
	
    //-----get csrf token from cookies----
		var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        headers: { "X-CSRFToken": csrftoken }
    });   
    //------AJAX Call-------
    $.ajax({
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        url: '/app/',
        //-------send data to server---------------
        data: {'search' : searchString},

        //-------handle successful response--------
        success : function(json) {
            //----get data from server posted as a message
            json_data = JSON.parse(json);
            if (json_data.error) { 
                alert(json_data.error_text);
            } else {  // Success - populate HTML table with json data
            	populateTable( json_data );
            }
            //$('body').append("<p>"+JSON.stringify(json_data)+"</p>");
        },
        //-------handle a unsuccessful response----------
        error : function(xhr,errmsg,err) {
        	alert(errmsg+": "+err);  //show Error message
            console.log(xhr.status + ": " + xhr.responseText); // log error to the console
        }
    });//-------end of AJAX call-----------
 } 

//Populates JSON data into HTML table
function populateTable( json_data ) {
	//----removes old rows----
	$("#tbody").children( 'tr' ).remove();
	var tr;
	//----add new rows--------
    for (var i = 0; i < json_data.length; i++) {
    	var date = new Date(json_data[i].fields.appointment_date);
        tr = $('<tr/>');
        tr.append("<td>" + date.format('M jS, Y') + "</td>");
        tr.append("<td>" + date.format('H:i') + "</td>");
        tr.append("<td>" + json_data[i].fields.appointment_text + "</td>");
        $("#tbody").append(tr);
    }
}

//Gets cookie value for given cookie name (for CSRF token)
function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
              
          for (var i = 0; i < cookies.length; i++) {
               var cookie = jQuery.trim(cookies[i]);
           
          		// check if this cookie name matches the searched cookie?
          	   if (cookie.substring(0, name.length + 1) == (name + '=')) {
            		cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            		//alert(cookieValue)
              		break;
               }
          }
      }
 return cookieValue;
}


