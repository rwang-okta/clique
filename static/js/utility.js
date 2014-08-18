function changeClass(isAddCreds, isCheckOutCreds){
    if (isAddCreds == true) {
        $(".back").html("<form class='form-horizontal add-cred-form' role='form' action='/cred' method='post' style='color: black;'><div class='control-group' style='margin-bottom: 20px'><div class='controls'><input type='text' placeholder='Name' required autofocus name='name' style='width: 400px'></div></div><div class='control-group' style='margin-bottom: 20px'><div class='controls'><textarea rows='10' placeholder='Notes' name='notes' style='width: 400px'></textarea></div></div><div class='control-group' style='margin-bottom: 20px'><div class='controls'><input type='text' placeholder='Last checkout (mm-dd-yy)' name='checkout' style='width: 400px'></div></div><div class='control-group' style='margin-bottom: 20px'><div class='controls'><input type='text' placeholder='Expires on (mm-dd-yy)' name='expireon' style='width: 400px'></div></div><div class='control-group' style='margin-bottom: 20px'><div class='controls'><input type='submit' value='Add' class='btn btn-primary'/></div></div></form>");
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

function redirectRemove() {
    location.pathname="/cred-remove";
}

function redirectCreds() {
    location.pathname="/cred";
}

function removeCred(credId) {
    $.post( "/cred-remove/" + credId, function( data ) {

    });
}