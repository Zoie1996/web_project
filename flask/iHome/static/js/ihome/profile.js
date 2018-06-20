function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // $('#form-avatar').submit(function (e) {
    //     e.preventDefault();
    //     var file = document.getElementById('avatar').files[0];
    //     var formdata = new FormData();
    //     formdata.append('avatar', file);
    //     console.log(formdata.get('avatar'));
    //     $.ajax({
    //         url: '/user/profile/',
    //         type: 'POST',
    //         data: formdata,
    //         //dataType: 'json',
    //         processData: false,
    //         contentType: false,
    //         success: function (msg) {
    //             if (msg.code == 200) {
    //                 $('#user-avatar').attr('src', '/static/' + msg.image_url);
    //             }
    //         },
    //         error: function () {
    //             alert('头像上传失败');
    //         }
    //     });
    // });
    $("#user-name").focus(function () {
        $(".error-msg").hide();
    });
    $('#form-avatar').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/user/profile/',
            type: 'PATCH',
            dataType: 'json',
            success: function (msg) {
                if (msg.code == 200) {
                    $('#user-avatar').attr('src', '/static/' + msg.image_url);
                }
            },
            error: function () {
                alert('头像上传失败');
            }
        });
        // 阻止表单自动提交
        // return false;
    });


    $('#form-name').submit(function (e) {
        e.preventDefault();
        var name = $('#user-name').val();
        $.ajax({
            url: '/user/change_name/',
            type: 'POST',
            dataType: 'json',
            data: {'name': name},
            success: function (msg) {
                if (msg.code == 200) {
                    location.href = '/user/my/';
                }
                if (msg.code == 1008) {
                    $('.error-msg span').html(msg.msg);
                    $('.error-msg').show();
                }
            }
        });
    });


});

