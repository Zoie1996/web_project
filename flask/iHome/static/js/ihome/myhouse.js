$(document).ready(function () {
    $(".auth-warn").show();

    $.get('/house/show_my_house/', function (msg) {
        if (msg.code == 200) {
            house_li = '';
            for (var i = 0; i < msg.houses.length; i++) {
                house_li += '<li><a href="/house/detail/?house_id=' + msg.houses[i].id + '">';
                house_li += '<div class="house-title"><h3>房屋ID:' + msg.houses[i].id + '——' + msg.houses[i].title + '</h3></div>';
                house_li += '<div class="house-content"><img src="/static/' + msg.houses[i].image + '">';
                house_li += '<div class="house-text"><ul><li>' + msg.houses[i].address + '</li>';
                house_li += '<li>价格:￥' + msg.houses[i].price + '/晚</li>';
                house_li += '<li>发布时间：' + msg.houses[i].create_time + '</li></ul></div></div></a></li>';
            }
            $('#houses-list').append(house_li);
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








