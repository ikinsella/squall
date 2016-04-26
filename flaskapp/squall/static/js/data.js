$(document).ready(function() {
    $("#collections").change(function() {
        var coll = Number($('#collections').val());
        var data = {data: JSON.stringify({"collid":coll})};
        if (coll == 0) {
            $('#coll_info').hide();
            $('#set_info').hide();
            $('.coll_val').empty();
            $('.set_val').empty();
            $('#sets').html('<option value="0">Select Data Set</option>');
        } else {
            $('#set_info').hide();
            $('.set_val').empty();
            $('#coll_info').show();
            $.post("show_sets", data, function(response) {
            $('#sets').html(response.sets);
            $('#coll_name').html(response.name);
            $('#coll_descr').html(response.descr);
            $('#coll_tags').html(response.tags);
        
            });
        }
        
    });
});

$(document).ready(function() {
    $("#sets").change(function() {
        var set = Number($('#sets').val());
        var data = {data: JSON.stringify({"setid":set})};
        if (set == 0) {
            $('#set_info').hide();
            $('.set_val').empty();
        } else {
            $('#set_info').show();
           $.post("select_set", data, function(response) {
            $('#set_name').html(response.name);
            $('#set_coll').html(response.coll);
            $('#set_urls').html(response.urls);
            $('#set_descr').html(response.descr);
            $('#set_tags').html(response.tags);
        
            });
        }
        
    });
});

$(document).ready(function() {
    $("#coll_button").click(function() {
        if ($("#coll_button").html() == "Add New Data Collection") {
            $("#coll_button").html("Hide Data Collection Form");
            $("#coll_form").show();
        } else {
            $("#coll_button").html("Add New Data Collection");
            $("#coll_form").hide();
        }
                           
    });
});

$(document).ready(function() {
    $("#set_button").click(function() {
        if ($("#set_button").html() == "Add New Data Set") {
            $("#set_button").html("Hide Data Set Form");
            $("#set_form").show();
        } else {
            $("#set_button").html("Add New Data Set");
            $("#set_form").hide();
        }
                           
    });
});