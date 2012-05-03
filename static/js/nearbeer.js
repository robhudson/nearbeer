$.getCurrentPosition(
    function(pos){
    // success
        alert('GOT IT: ' + pos.coords.latitude + ', ' + pos.coords.longitude);
    },
    function(e){
        alert('FAIL :( ' + e.message);
    }
);
