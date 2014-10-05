$(document).ready(function(){
    var val =  ["Andy", "Andrew", "Bob", "Bobby", "Chuck", "Charles", "David"];
    $("#name_input").autocomplete({
        source: val;
    });
});
