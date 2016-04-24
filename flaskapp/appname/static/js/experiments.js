$(document).ready(function() {
    $("#experiments").change(function() {
        var exp = Number($('#experiments').val());
        var data = {data: JSON.stringify({"expid":exp})};
        if (exp == 0) {
            $('#exp_info').hide();
            $('.exp_val').empty();
        } else {
            $('#exp_info').show();
            $.post("select_experiment", data, function(response) {
            $('#exp_name').html(response.name);
            $('#exp_descr').html(response.descr);
            $('#exp_tags').html(response.tags);
            $('#exp_colls').html(response.colls);
            $('#exp_algs').html(response.algs);
        
            });
        }
        
    });
});

$(document).ready(function() {
    $("#exp_button").click(function() {
        if ($("#exp_button").html() == "Add New Experiment") {
            $("#exp_button").html("Hide Experiment Form");
            $("#exp_form").show();
        } else {
            $("#exp_button").html("Add New Experiment");
            $("#exp_form").hide();
        }
                           
    });
});