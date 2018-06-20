function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {

    $.get('/house/area_facility/', function (msg) {
            var area_list = '';
            console.log(msg.area);
            for (var i = 0; i < msg.area.length; i++) {
                area_option = '<option value="' + msg.area[i].id + '">' + msg.area[i].name + '</option>';
                area_list += area_option;
            }
            $('#area-id').html(area_list);
            var facility_list = '';
            for (var j = 0; j < msg.facility.length; j++) {
                facility_li = '<li><div class="checkbox"><label>';
                facility_li += '<input type="checkbox" name="facility" value="' + msg.facility[j].id + '">' + msg.facility[j].name;
                facility_li += '</label></div></li>';
                facility_list += facility_li
            }
            $('.house-facility-list').html(facility_list);
        }
    );


    $('#form-house-info').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/house/new_house/',
            type: 'Post',
            dataType: 'json',
            success: function (msg) {
                if (msg.code == 200) {
                    $('.popup_con').fadeIn('slow');
                    $('.popup_con').fadeOut('fast');
                    location.href = '/house/my_house/';
                }
            },

        });


    });
});