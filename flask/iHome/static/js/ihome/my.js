function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){

    $.ajax({
        url:'/user/show_my/',
        type: 'GET',
        dataType:'json',
        success:function (msg) {
            if(msg.code == 200){
                $('#user-avatar').attr('src', '/static/'+msg.data.avatar);
                $('#user-name').text(msg.data.name);
                $('#user-mobile').text(msg.data.phone)
            }
        },
        error:function () {
            console.log('请求失败');
        }
    });

});