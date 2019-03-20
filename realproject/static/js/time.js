 $( document ).ready(function() {
    $('#other_time').hide();

});


function otherTime(that) {
    if (that.value == "3" )
    {
         $('#other_time').show();
    }
    else
    {
            $('#other_time').hide();
    }



}