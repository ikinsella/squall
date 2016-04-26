$(document).ready(function() {
    $("#algorithms").change(function() {
        var alg = Number($('#algorithms').val());
        var data = {data: JSON.stringify({"algid":alg})};
        if (alg == 0) {
            $('#alg_info').hide();
            $('#imp_info').hide();
            $('.alg_val').empty();
            $('.imp_val').empty();
            $('#implementations').html('<option value="0">Select Implementation</option>');
        } else {
            $('#imp_info').hide();
            $('.imp_val').empty();
            $('#alg_info').show();
            $.post("narrow", data, function(response) {
            $('#implementations').html(response.imps);
            $('#alg_name').html(response.name);
            $('#alg_descr').html(response.descr);
            $('#alg_tags').html(response.tags);
        
            });
        }
        
    });
});

$(document).ready(function() {
    $("#implementations").change(function() {
        var imp = Number($('#implementations').val());
        var data = {data: JSON.stringify({"impid":imp})};
        if (imp == 0) {
            $('#imp_info').hide();
            $('.imp_val').empty();
        } else {
            $('#imp_info').show();
           $.post("select_imp", data, function(response) {
            $('#imp_name').html(response.name);
            $('#imp_alg').html(response.alg);
            $('#imp_urls').html(response.urls);
            $('#imp_scripts').html(response.scripts);
            $('#imp_exe').html(response.exe);
            $('#imp_descr').html(response.descr);
            $('#imp_tags').html(response.tags);
        
            });
        }
        
    });
});

$(document).ready(function() {
    $("#alg_button").click(function() {
        if ($("#alg_button").html() == "Add New Algorithm") {
            $("#alg_button").html("Hide Algorithm Form");
            $("#alg_form").show();
        } else {
            $("#alg_button").html("Add New Algorithm");
            $("#alg_form").hide();
        }
                           
    });
});

$(document).ready(function() {
    $("#imp_button").click(function() {
        if ($("#imp_button").html() == "Add New Implementation") {
            $("#imp_button").html("Hide Implementation Form");
            $("#imp_form").show();
        } else {
            $("#imp_button").html("Add New Implementation");
            $("#imp_form").hide();
        }
                           
    });
});