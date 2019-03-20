
function Calculate() {
    
    var chkArray = [];
	var cost = 0;
    var i =0;
	$(".arr:checked").each(function() {
        chkArray.push($(this).attr('data-price')) ;
	});
    for ( i ; i< chkArray.length; i++) {
         cost = cost + parseInt(chkArray[i]);
    }
    $("#cost_arr").val(cost);
    

}
function Calculate2(){
    var chkArray = [];
    $(".menu:checked").each(function() {
        chkArray.push($(this).attr('data-menu'));
    });
    $("#cost_menu").val(parseInt(chkArray[0]));

}
function Calculate3(){
    var totalGuest = $("#guests").val();
    var cost_arr = $("#cost_arr").val();
    var cost_menu = $("#cost_menu").val();
    var additional_cph = $("#adch").val();
    var additional_oc = $("#adoc").val();
    var disc          = $("#disc").val();
    disc = disc / 100;
    var totalDisc = $("#tdisc").val();

    var temp = parseInt(cost_arr) + parseInt(totalGuest) * parseInt(cost_menu);
    var totalPayableAmount =  temp;   // Computing general cost

    temp = parseInt(totalGuest) * parseInt(additional_cph); // Adding additional cost per head
    totalPayableAmount = totalPayableAmount + temp; 

    totalPayableAmount = totalPayableAmount + parseInt(additional_oc); //Adding overall cost

    temp = totalPayableAmount * disc; // Discount
    totalPayableAmount = totalPayableAmount - temp;

    totalPayableAmount = totalPayableAmount - parseInt(totalDisc);

    $('#tpa').val(totalPayableAmount);

}

