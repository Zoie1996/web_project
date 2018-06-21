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
            type: 'POST',
            dataType: 'json',
            success: function (msg) {
                if (msg.code == 200) {
                    console.log(msg.house_id);
                    $('.popup_con').fadeIn('fast');
                    $('.popup_con').fadeOut('fast');
                    $('#form-house-info').hide();
                    $('#form-house-image').show();
                    $('#house-id').val(msg.house_id)
                }
            },
        });

    });


    $('#form-house-image').submit(function (e) {
        e.preventDefault();
        house_id = $('#house-id').val();
        $(this).ajaxSubmit({
            url: '/house/new_house_image/'+house_id+'/',
            type: 'POST',
            dataType: 'json',
            success: function (msg) {
                if (msg.code == 200) {
                    var img_html = '<img src="/static/'+msg.image_url+'">';
                    $('.house-image-cons').append(img_html);
                }
            },
        });

    });
});