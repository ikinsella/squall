//$(document).ready(function() {
//                  $.post("get_curr_dir", function(response) {})
//});

$(document).ready(function() {
    $("#users").change(function() {
        var user = Number($('#users').val());
        var data = {data: JSON.stringify({"userid":user})};
        if (user == 0) {
            $('#user_info').hide();
            $('.user_val').empty();
        } else {
            $('#user_info').show();
            $.post("select_user", data, function(response) {
            $('#user_name').html(response.name);
            $('#user_dir').html(response.dir);
        
            });
        }
        
    });
});

$(document).ready(function() {
    $("#user_button").click(function() {
        if ($("#user_button").html() == "Create New User") {
            $("#user_button").html("Hide User Form");
            $("#user_form").show();
        } else {
            $("#user_button").html("Create New User");
            $("#user_form").hide();
        }
                           
    });
});

$(document).ready(function() {
    $("#edit_button").click(function() {
        if ($("#edit_button").html() == "Edit User Information") {
            $("#edit_button").html("Hide Edit Form");
            $("#edit_form").show();
        } else {
            $("#edit_button").html("Edit User Information");
            $("#edit_form").hide();
        }
                           
    });
});