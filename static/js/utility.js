function changeClass(isAddCreds, isCheckOutCreds){
    if (isAddCreds == true) {
        $(".back").html("
        
        ")
    }

    if(document.getElementById("block").className == "block"){
        document.getElementById("block").className += " rotated";
    }
    else{
        document.getElementById("block").className = "block";
    }
}