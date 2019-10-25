function getUserOrders(){
    // These names have to match the keys expected by Python
    // This is the json object that is passed to the `/temperature`
    // route.
    console.log('test');

    const user_order_request = {
        'user_id': parseInt($('#user_id input').val()),
    };

    // const features = {
    //   'temperature': parseFloat($('#temp').val()),
    //   'unit': $('#unit').val()
    // };
  
    /*
     * url: where we send the request
     * data: the JSON/"dictionary" object that Flask sees in request.json
     * contentType: mandatory. Let's us know that we are passing JSON data
     * success: the function that is called if the call is successful (i.e. response code is 2XX)
     * error: the function that is called if the call is unsuccessful (i.e. response code is not 2XX)
     *
     * Note: whatever flask returns from the "convert_temps()" function is passed back as an
     * argument to the success/error functions.
     */

    $.ajax({
        url: '/get_user_order',
        type: 'GET',
        data: {'user_id': user_order_request.user_id},
        dataType: 'text',
        success: (result) => user_order_get_success(result),
        error: (result) => user_order_get_fail(result)
    });

  }

function user_order_get_success(result){
    console.log('Success!');
    $("#user_order").html(result)
  }
  
  // Function called on error
  // You can decide what you'd like
function user_order_get_fail(result){
    console.log('There was an error! Our application returned');
    console.log(result.toString().slice(-400,0));
  }


/*
 * This is called whenever the number or the unit are changed
 */
function doConversion(){
    // These names have to match the keys expected by Python
    // This is the json object that is passed to the `/temperature`
    // route.
    console.log('test')

    const features = {
      'temperature': parseFloat($('#temp').val()),
      'unit': $('#unit').val()
    };
  
    /*
     * url: where we send the request
     * data: the JSON/"dictionary" object that Flask sees in request.json
     * contentType: mandatory. Let's us know that we are passing JSON data
     * success: the function that is called if the call is successful (i.e. response code is 2XX)
     * error: the function that is called if the call is unsuccessful (i.e. response code is not 2XX)
     *
     * Note: whatever flask returns from the "convert_temps()" function is passed back as an
     * argument to the success/error functions.
     */

    $.ajax({
        url: '/convert_temperature',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(features),
        success: (result) => metis_success(result),
        error: (result) => metis_error(result)
    });

  }
  
  // Function called on success.
  // Your job: instead of printing result to the console, make it print to
  //           the div with id "result".
  function metis_success(result){
    const msg = `This temperature is ${result['F']} in Farenheight, ${result['C']} in Centigrade and ${result['K']} in Kelvin`; 
    $('#result').html(msg);
  }
  
  // Function called on error
  // You can decide what you'd like
  function metis_error(result){
    console.log('There was an error! Our application returned');
    console.log(result.responseJSON);
  }