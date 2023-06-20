odoo.define('programme.programme', function (require) {
    'use strict';
    
    var rpc = require('web.rpc');
    var model = 'programme.programme';
    function geoFindMe() {
      function success(position) {
        var latitude = position.coords.latitude.toString();
        var longitude = position.coords.longitude.toString();
    
          rpc.query({
            model: model,
            method: "find_me",
            args: [latitude, longitude]
          }).then(function () {
  
          })
      }
      function error() {console.alert('Unable to retrieve your location'); }
      if (!navigator.geolocation) {
       console.alert('Geolocation is not supported by your browser');
      }
      else {
        // status = 'Locating…'; 
        navigator.geolocation.getCurrentPosition(success, error);
      }
    }
  
    document.querySelector('.bt bt-primary').addEventListener('click', geoFindMe);
  })