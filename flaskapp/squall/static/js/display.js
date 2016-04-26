//$(document).ready(function() {
//$("#algorithms").change(function() {
//    $.ajax({
//        type: "POST",
//        url: "narrow",
//        data: {
//            //algorithm: $("#algorithms").val()
//           func:'narrow'
//        },
//        error: function(xhr, status, error) {
//           $("#implementations").html("<option>failed request</option>");
//           var err = eval("(" + xhr.responseText + ")");
//           alert(err.Message);
//           
//        },
//        success: function(data) {
//            $("#implementations").html(data);
//        }
//    });
//});
//});

$(document).ready(function() {
    $("#algorithms").change(function() {
        $.ajax({
            type: "POST",
            url: "narrow",
            data: {
               //algorithm: $("#algorithms").val()
               func:'narrow'
            },
            error: function(xhr, status, error) {
               $("#implementations").html("<option>failed request</option>");
                var err = eval("(" + xhr.responseText + ")");
                alert(err.Message);
                                                 
            },
            success: function(data) {
                $("#implementations").html(data);
            }
        });
    });
});