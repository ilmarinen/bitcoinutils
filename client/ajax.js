// Code taken from https://www.djangoproject.com/weblog/2011/feb/08/security/
// Adds Djangos CSRF token to the AJAX request header.
$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

function makeGetCall(url) {

    return $.ajax({
        type: "GET",
        url: url,
        data: null,
        dataType: "json",
        contentType: "application/json;charset=utf-8"
    });
};

function makePostCall(url, data) {
   var json_data = JSON.stringify(data);

    return $.ajax({
        type: "POST",
        url: url,
        data: json_data,
        dataType: "json",
        contentType: "application/json;charset=utf-8"
    });
};

function makePutCall(url, data) {
   var json_data = JSON.stringify(data);

    return $.ajax({
        type: "PUT",
        url: url,
        data: json_data,
        dataType: "json",
        contentType: "application/json;charset=utf-8"
    });
};

function makeDeleteCall(url) {

    return $.ajax({
        type: "DELETE",
        url: url,
        data: null,
        dataType: "json",
        contentType: "application/json;charset=utf-8"
    });
};

export {makePostCall, makeGetCall, makePutCall, makeDeleteCall};
