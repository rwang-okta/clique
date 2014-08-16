function changeClass(isAddCreds, isCheckOutCreds){
    if (isAddCreds == true) {
        $(".back").html("");
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