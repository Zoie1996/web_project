$(document).ready(function () {
    $(".auth-warn").show();


    $.get('/house/show_my_house/', function (msg) {
        if (msg.code == 200) {
            console.log(msg);
            house_li = '';
            for (var i = 0; i < msg.houses.length; i++) {
                house_li += '<li><a href="#"> <div class="house-title"><h3>房屋ID:' + msg.houses[i].id + '——' + msg.houses[i].title + '</h3></div>';
                house_li += '<div class="house-content"><img src="/static/images/home01.jpg"><div class="house-text">';
                house_li += '<ul><li>' + msg.houses[i].address + '</li><li>价格:￥' + msg.houses[i].price + '/晚</li><li>发布时间：' + msg.houses[i].create_time + '</li></ul></div></div></a></li>'
            }
            $('#houses-list').html(house_li);
        }
    });
});

$.get('/user/auths/', function (msg) {
    if (msg.code == 200) {
        if (msg.data.id_card) {
            $(".auth-warn").hide();
        } else {
            $('#houses-list').hide()
        }
    }
});





