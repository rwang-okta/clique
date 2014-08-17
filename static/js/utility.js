function changeClass(isAddCreds, isCheckOutCreds){
    if (isAddCreds == true) {
        $(".back").html("<form class='form-horizontal'><div class='control-group'><div class='controls'><input type='text' id='name' placeholder='Name'></div></div><div class='control-group'><div class='controls'><input type='text' id='notes' placeholder='Notes'></div></div><div class='control-group'><div class='controls'><input type='text' id='checkout' placeholder='Last checkout'></div></div><div class='control-group'><div class='controls'><input type='text' id='expireon' placeholder='Expires on'></div></div><div class='control-group'><div class='controls'><button type='button' class='btn btn-primary add-cred'>Add Test Cred</button></div></div></form>");
        $(".add-cred").attr("onclick", "addcred")
    }

    if (isCheckOutCreds != false) {
        $.get( "/cred/" + isCheckOutCreds, function( data ) {
            var json_obj = $.parseJSON(data);
            $("#login_url").html(json_obj.login_url);
            $("#username").html(json_obj.username);
            $("#password").html(json_obj.password);
        });
        $(".confirm-checkout").attr("onclick", "checkout(" + isCheckOutCreds + ")")
    }

    if(document.getElementById("block").className == "block"){
        document.getElementById("block").className += " rotated";
    }
    else{
        document.getElementById("block").className = "block";
    }
}

function checkout(credId) {
    $.post( "/cred/" + credId, function( data ) {

        });
    location.reload();
}

function addcred(name, notes, lastcheckout, expireon) {
    
}