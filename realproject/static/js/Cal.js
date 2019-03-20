
var eventInfo = [];
 var arr=[];
 var info=[];
//$("#addDates").click(function () {
//
function myfunction(my_list){
    // is main kerday copy ok
    var a=true;

    for( var i = 0, len = my_list.length; i < len; i++ ){
        for( var j = 0, len1 = arr.length; j < len1; j++ )
        {
            a=true;
            if(arr[j]==my_list[i].event_date)
            {
                info[j] += my_list[i].event_slot + "  " + my_list[i].event_hall + "\n";
                a=false;
                break;
            }

        }
        if(a)
        {
        arr[i]=my_list[i].event_date;

        info[i]= my_list[i].event_slot + "  " + my_list[i].event_hall + "\n";
        }
//        info.push(in);
    }
//        for( var i = 0, len = my_list.length; i < len; i++ ){
//        var in= my_list[i].event_slot + "  " + my_list[i].event_hall;
//        info.push(in);
//    }

};
//    function unavailable(date) {
//  dmy = (date.getMonth()+1) + "/" + date.getDate() + "/" + date.getFullYear();
//  alert(dmy)
//  if ($.inArray(date, arr) < 0) {
//    return [true,"event","Book Now"];
//  } else {
//    return [true, '', ''];
//  }
//}
//
//$('#datepicker2').datepicker({ beforeShowDay: unavailable });

$( function() {
    var eventDates = {};
    var eventInfo ={};


    // datepicker
    $('#datepicker2').datepicker(    {
        beforeShowDay: function( date ) {
               for( var i = 0, len = arr.length; i < len; i++ ){
//        eventDates[ new Date (arr[i] ) ]=  new Date( arr[i] );
//           if(eventInfo[date]==date)
//           {
//              eventInfo[date]=eventInfo[date] + info[i];
//           }
//           else
//           {
            eventInfo[ new Date (arr[i] ) ] =  info[i];

    }
            var highlight = eventInfo[date];
            if( highlight ) {
                 return [true, "event", eventInfo[date]];

            } else {
                 return [true, '', ''];
            }
        }
    });
});
//
//function Test()
//{
//    var data = {};
//        var date = $("#datepicker2").val();
//        var hall = $("#hall").val();
//        var slot = $("#slot").val();
//
////        alert(date  + " " + slot + " " + hall );
//
//        data.Date = date;
//        data.Hall = hall;
//        data.Slot = slot;
//
//        eventInfo.push(data);
//        alert(eventInfo[0].Date);
//
//}