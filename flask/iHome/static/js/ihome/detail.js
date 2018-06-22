function hrefBack() {
    history.go(-1);
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {

    var house_id = decodeQuery()['house_id'];
    $.get('/house/detail/' + house_id, function (msg) {

        if (msg.code == 200) {
            data = msg.house_info;
            image_li = '';
            for (var i = 0; i < data.images.length; i++) {
                image_li += '<li class="swiper-slide"><img src="/static/' + data.images[i] + '"></li>'
            }
            $('.swiper-wrapper').html(image_li);
            $('.house-price span').html(data.price);
            $('.house-title').html(data.title);
            $('.landlord-pic img').attr('src', '/static/' + data.user_avatar);
            $('.landlord-name span').html(data.user_name);
            $('.house_address li').html('地址:' + data.address);
            $('.house_info').html('<h3>出租' + data.room_count + '间</h3>\n' +
                '<p>房屋面积:' + data.acreage + '平米</p>\n' +
                '<p>房屋户型:' + data.unit + '</p>');
            $('.user_info').html('<h3>宜住' + data.capacity + '人</h3>');
            $('.bed_info').append('<p>' + data.beds + '</p>');
            $('.house_infos').html(' <li>收取押金<span>' + data.deposit + '</span></li>\n' +
                '<li>最少入住天数<span>' + data.min_days + '</span></li>\n' +
                '<li>最多入住天数<span>' + (data.max_days == 0 ? "无限制" : data.max_days) + '</span></li>');

            facility_li = '';
            for (var j = 0; j < data.facilities.length; j++) {
                facility_li += '<li><span class=' + data.facilities[j].css + '></span>' + data.facilities[j].name + '</li>';
            }

            $('.house-facility-list').html(facility_li);
            $('.book-house').attr('href', '/house/booking/?house_id=' + house_id)
        }


        var mySwiper = new Swiper('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationType: 'fraction'
        });

        $(".book-house").show();
    });
});