// User Slider - Update Tables
function userSlider() {

    getUserCartActual();
    getUserCartPrediction();
    
}

// Get Actual User Cart
function getUserCartActual() {

    const user_id = parseInt($('#user_id').val());

    console.log(user_id);

    $("#viewing_user").html(user_id);

    $.ajax({
        url: '/get_user_order_actual',
        type: 'GET',
        data: { 'user_id': user_id },
        dataType: 'text',
        success: (result) => getUserCartActual_Success(result),
        error: (result) => getUserCartActual_Fail(result)
    });

}

// ADD USER ORDER TABLE TO DIV
function getUserCartActual_Success(result) {
    console.log('Success!');
    $("#user_order_actual").html(result)
}

function getUserCartActual_Fail(result) {
    console.log('There was an error! Our application returned');
    console.log(result.toString().slice(-400, 0));
}

function getUserCartPrediction() {

    const user_order_request = {
        'user_id': parseInt($('#user_id').val()),
        'thresh': parseInt($("#thresh-slider").val()) / 100.0
    };

    $.ajax({
        url: '/get_cart_prediction',
        type: 'GET',
        data: { 'user_id': user_order_request.user_id,
        'thresh': user_order_request.thresh},
        dataType: 'text',
        success: (html_output) => getUserCartPrediction_Success(html_output),
        error: (html_output) => getUserCartPrediction_Fail(html_output)
    });
}

// ADD USER PREDICTIONS TO DIV
function getUserCartPrediction_Success(html_output) {
    console.log('Success!');
    $("#user_order_prediction").html(html_output);
}

function getUserCartPrediction_Fail(table) {
    console.log('There was an error! Our application returned');
    console.log(table.toString().slice(-400, 0));
}































/*
 * This is called whenever the number or the unit are changed
 */
function doConversion() {
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
function metis_success(result) {
    const msg = `This temperature is ${result['F']} in Farenheight, ${result['C']} in Centigrade and ${result['K']} in Kelvin`;
    $('#result').html(msg);
}

// Function called on error
// You can decide what you'd like
function metis_error(result) {
    console.log('There was an error! Our application returned');
    console.log(result.responseJSON);
}