$(function(){

$.getCurrentPosition(
    function(pos){
    // success
/*        $('#beers').load('/beers/' +
                         pos.coords.latitude + ',' +
                         pos.coords.longitude);*/
    },
    function(e){
    // fail
        //alert('FAIL :( ' + e.message);
    }
);

});
