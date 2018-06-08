$(function () {

    $("#all_types").click(function () {

        $("#all_types_container").show();
        $("#all_type_logo").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
        $("#sort_container").hide();
        $("#sort_rule_logo").addClass("glyphicon-chevron-down").removeClass("glyphicon-chevron-up");
    })


    $("#all_types_container").click(function () {
        $(this).hide();
        $("#all_type_logo").addClass("glyphicon-chevron-down").removeClass("glyphicon-chevron-up");

    })


    $("#sort_rule").click(function () {
        $("#sort_container").show();
        $("#sort_rule_logo").addClass("glyphicon-chevron-up").removeClass("glyphicon-chevron-down");
        $("#all_types_container").hide();
        $("#all_type_logo").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    })

    $("#sort_container").click(function () {
        $(this).hide();
        $("#sort_rule_logo").addClass("glyphicon-chevron-down").removeClass("glyphicon-chevron-up");
    })




});