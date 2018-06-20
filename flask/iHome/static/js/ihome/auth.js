function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$(document).ready(function () {
    $('#form-auth').submit(function (e) {
        e.preventDefault();
        real_name = $('#real-name').val();
        id_card = $('#id-card').val();
        $.ajax({
            url: '/user/auth/',
            type: 'POST',
            dataType: 'json',
            data: {'real_name': real_name, 'id_card': id_card},
            success: function (msg) {
                if (msg.code == 200) {
                    $('.popup_con').show();
                    showSuccessMsg()
                }
                if (msg.code == 1001) {
                    $('.error-msg span').html(msg.msg);
                    $('.error-msg').show()
                }
                if (msg.code == 1009) {
                    $('.error-msg span').html(msg.msg);
                    $('.error-msg').show()
                }
            },
            error: function () {
                alert('保存失败');
            }
        });
    });


});

