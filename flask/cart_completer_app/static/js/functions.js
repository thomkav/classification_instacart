// User Slider - Update Tables
function updateModel() {

    getUserCartActual();
    getUserCartPrediction();
    
}

// Select a Model
function selectModel() {

    const model_ind = parseInt($('#modelSlider').val());

    // console.log(user);

    $.ajax({
        url: '/select-model',
        type: 'GET',
        data: { 'model_ind': model_ind },
        dataType: 'text',
        success: (model_name) => selectModel_Success(model_name),
        error: (result) => selectModel_Fail(result)
    });

}

// Update Model
function selectModel_Success(model_name) {
    $("#modelSliderOutput").html(model_name);
    updateModel();
}

function selectModel_Fail(result) {
    console.log('selectModel Error... Our application returned');
    console.log(result.toString().slice(-400, 0));
}


// Get Actual User Cart
function getUserCartActual() {

    const user = parseInt($('#userSlider').val());

    // console.log(user);

    $.ajax({
        url: '/get_user_order_actual',
        type: 'GET',
        data: { 'user_ind': user },
        dataType: 'text',
        success: (response) => getUserCartActual_Success(response),
        error: (response) => getUserCartActual_Fail(response)
    });

}

// ADD USER ORDER TABLE TO DIV
function getUserCartActual_Success(response) {
    json = JSON.parse(response)
    console.log(json["user_id"])
    console.log('User Cart Actual Success!');
    $("#user_order_actual").html(json["html_output"]);
    $("#viewing_user").html(json["user_id"]);
}

function getUserCartActual_Fail(result) {
    console.log('User Cart Actual Error... Our application returned');
    console.log(result.toString().slice(-400, 0));
}

function getUserCartPrediction() {

    const user_order_request = {
        'user': parseInt($('#userSlider').val()),
        'rec_count': parseInt($("#recSlider").val())
    };

    $.ajax({
        url: '/get_cart_prediction',
        type: 'GET',
        data: { 'user_ind': user_order_request.user,
        'rec_count': user_order_request.rec_count},
        dataType: 'text',
        success: (response) => getUserCartPrediction_Success(response),
        error: (response) => getUserCartPrediction_Fail(response)
    });
}

// ADD USER PREDICTIONS TO DIV
function getUserCartPrediction_Success(response) {
    console.log('User Prediction Ajax Success!');
    json = JSON.parse(response)
    html_output = json['html_output'];
    cart_metrics = json['cart_metrics']
    $("#user_order_prediction").html(html_output);
    $("#cart_metrics").html(cart_metrics);
}

function getUserCartPrediction_Fail(response) {
    console.log('There was an error! Our application returned');
    console.log(response.toString().slice(-400, 0));
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