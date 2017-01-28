

$(document).ready(function(){
//type="text/javascript" src="/static/jquery-dateFormat.js"
//type="text/javascript" src="/static/dateFormat.min.js"
    $('#fdate').datepicker();	
    $("#ttable").hide();
	$("#fform").hide();
    $("#fnew").click(function(){
        $("#fform").show(100);
        $("#fnew").hide(); 
    });
    $("#fcancel").click(function(){
        $("#fform").hide(100);
        $("#fnew").show();
        
    });

    $( "#ftime" ).timepicker({ timeFormat: 'H:i' });
    
    
    $("#bsearch").click(function(){
        var searchString = $("#tsearch").val();

        //get csrf token
 		var csrftoken = getCookie('csrftoken');
        //alert("search str="+searchString+"\n"+csrftoken +" =? "+ '{{ csrf_token }}' +"\n"+ JSON.stringify({csrfmiddlewaretoken : csrftoken, search : searchString}));
        $.ajaxSetup({
            headers: { "X-CSRFToken": csrftoken }
        });       
        $.ajax({
        	//alert("Searching for ="+searchString);
            type: 'GET',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            url: '/app/',
            //send data to server+++++++++++++++++++++++++++++++++++++++++++++=
            //data: JSON.stringify({csrfmiddlewaretoken : csrftoken, search : searchString}),
            //data: {csrfmiddlewaretoken : csrftoken, search : searchString},
            data: {'search' : searchString},
            //data: JSON.stringify({search : searchString}),
            // handle a successful response from server
            success : function(json) {
                //console.log(json); // another sanity check
                //On success show the data posted to server as a message
                result = JSON.parse(json);
                if (result.error) { 
                    alert(result.error_text);
                } else {  // Success
                	//alert("Success: "+result+" length="+result.length); 
                	$("#ftable").hide();
                	//$("#tbody").find("tr:gt(0)").remove();
                	//$("#tbody").children( 'tr:not(:first)' ).remove();
                	$("#tbody").children( 'tr' ).remove();
                	var tr;
                    for (var i = 0; i < result.length; i++) {
                    	//alert(JSON.stringify(result[i]))
                    	//alert(result[i].fields.appointment_text+" -> "+result[i].fields.appointment_date)
                    	//var date = new Date(result[i].fields.appointment_date.replace("T", " "));
                    	var date = new Date(result[i].fields.appointment_date);
                    	//var formatted = $.datepicker.formatDate("M d, yy", new Date());
                    	//$.format(new Date(), "dd M yy");
                        //$.format.parseDate('1982-10-15T01:10:20Z')
                    //alert(DateFormat.format(new Date(), "dd M yy"));
          	//alert(result[i].fields.appointment_date+" -> "+date); //+" -> "+time);
                        tr = $('<tr/>');
                        tr.append("<td>" + date + "</td>");
                        tr.append("<td>" + result[i].fields.appointment_date + "</td>");
                        tr.append("<td>" + result[i].fields.appointment_text + "</td>");
                       // tr.append("<td>" + json[i].team + "</td>");
                        $("#tbody").append(tr);
                        $("#ttable").show();
                    }
                    //$('#output').show();
                    //document.getElementById('output-ans').innerHTML=result;
                }
                //alert('Hi   '+json['searchString'] +'!.' + '  csrftoken:'+ json['password']);
                //$('body').append("<p>"+JSON.stringify(json)+"</p>");
            },
                // handle a unsuccessful response
            error : function(xhr,errmsg,err) {
            	alert(errmsg+": "+err);
                console.log(xhr.status + ": " + xhr.responseText); // provide info about the error to the console
            }
        });
        
     });   
    
    //Gets cookie value for given cookie name (for CSRF token)
    function getCookie(name) {
              var cookieValue = null;
              if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    //alert(cookies[0])
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

});
//


function getAppointments() {
	
};



