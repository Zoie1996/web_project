function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$(document).ready(function () {
    var house_id = decodeQuery()['house_id'];
    $.get('/house/detail/' + house_id, function (msg) {
        if (msg.code == 200) {
            console.log(msg);
            data = msg.house_info;
            $('.house-info img').attr('src', '/static/' + data.images[0]);
            $('.house-text h3').text(data.title);
            $('.house-text>p>span').html(data.price);
        }
    });

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function () {
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd) / (1000 * 3600 * 24) + 1;
            var price = $(".house-text>p>span").text();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共" + days + "晚)");
        }
    });

});

$('.submit-btn').on('click', function () {
    var house_id = decodeQuery()['house_id'];
    start_date = $('#start-date').val();
    end_date = $('#end-date').val();
    $.post('/order/create_order/',
        {'start_date': start_date, 'end_date': end_date, 'house_id': house_id},
        function (msg) {
            if (msg.code == 200) {
                location.href = '/order/orders/';
            }

        });
});
