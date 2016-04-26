$(document).ready(function() {
    $("#experiments").change(function() {
        var exp = Number($('#experiments').val());
        var data = {data: JSON.stringify({"expid":exp})};
        if (exp == 0) {
            $('#exp_info').hide();
            $('#batch_info').hide();
            $('.exp_val').empty();
            $('.batch_val').empty();
            $('#batches').html('<option value="0">Select Batch</option>');
        } else {
            $('#batch_info').hide();
            $('.batch_val').empty();
            $('#exp_info').show();
            $.post("select_experiment", data, function(response) {
            $('#exp_name').html(response.name);
            $('#exp_descr').html(response.descr);
            $('#exp_tags').html(response.tags);
            $('#exp_colls').html(response.colls);
            $('#exp_algs').html(response.algs);
            $('#batches').html(response.batches);
            });
        }
        
    });
});

$(document).ready(function() {
    $("#batches").change(function() {
        var batch = Number($('#batches').val());
        var data = {data: JSON.stringify({"batchid":batch})};
        if (batch == 0) {
            $('#batch_info').hide();
            $('.batch_val').empty();
        } else {
            $('#batch_info').show();
            $.post("select_batch", data, function(response) {
            $('#batch_name').html(response.name);
            $('#batch_exp').html(response.exp);
            $('#batch_set').html(response.set);
            $('#batch_imp').html(response.imp);
            $('#batch_param').html(response.param);
            $('#batch_mem').html(response.mem);
            $('#batch_disk').html(response.disk);
            $('#batch_flock').html(response.flock);
            $('#batch_glide').html(response.glide);
            $('#batch_descr').html(response.descr);
            $('#batch_tags').html(response.tags);
        
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

$(document).ready(function() {
    $("#batch_button").click(function() {
        if ($("#batch_button").html() == "Create New Batch") {
            $("#batch_button").html("Hide Batch Form");
            $("#batch_form").show();
        } else {
            $("#batch_button").html("Create New Batch");
            $("#batch_form").hide();
        }
                           
    });
});

$(document).ready(function() {
    $("#launch_files_button").click(function() {
        if ($("#launch_files_button").html() == "Download Launch Files") {
            $("#launch_files_button").html("Hide Launch Files Form");
            $("#launch_files_form").show();
        } else {
            $("#launch_files_button").html("Download Launch Files");
            $("#launch_files_form").hide();
        }
                           
    });
});

$(document).ready(function() {
    $("#results_button").click(function() {
        if ($("#results_button").html() == "Upload Results") {
            $("#results_button").html("Hide Results Form");
            $("#results_form").show();
        } else {
            $("#results_button").html("Upload Results");
            $("#results_form").hide();
        }
                           
    });
});

$(document).ready(function() {
    var batch = Number($('#batch').val());
    var data = {data: JSON.stringify({"batchid":batch})};
    $.post("select_upload", data, function(response) {
        $('#batch_status').html("Batch completed? " + response.status);
    });
    $("#batch").change(function() {
        var b = Number($('#batch').val());
        var d = {data: JSON.stringify({"batchid":b})};
        $.post("select_upload", d, function(boop) {
            $('#batch_status').html("Batch completed? " + boop.status);
        });
        
    });
                  
});

$(document).ready(function() {
    $("#param_button").click(function() {
        if ($("#param_button").html() == "Show") {
            $("#param_button").html("Hide");
            $("#batch_param").show();
        } else {
            $("#param_button").html("Show");
            $("#batch_param").hide();
        }
        return false;
    });
});