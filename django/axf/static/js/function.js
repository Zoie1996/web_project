// 添加购物车商品数量
function addCart(goods_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: '/axf/addCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if (msg.code == 200) {
                $('#num_' + goods_id).text(msg.c_num);
            }
            totalPrice();
        },
        error: function () {
            location.href = '/user/login/';
        },
    });
}

// 减少购物车商品数量
function subCart(goods_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/subCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if (msg.code == 200) {
                $('#num_' + goods_id).text(msg.c_num);
            }
            if (msg.c_num == 0) {
                // console.log($('#num_' + goods_id).parents('li'));
                $('#num_' + goods_id).parents('li').remove();
            }
            totalPrice();
        },
        error: function (msg) {
            alert('请求失败');
            location.href = '/user/login/';
        },
    });
}


// 显示闪购页面商品数量


// 改变购物车单个商品数量状态
function change_cart_status(cart_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/change_cart_status/',
        type: 'POST',
        data: {'cart_id': cart_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            if (data.code == 200) {
                if (data.is_select) {
                    $('#cart_id_' + cart_id).html('√');
                } else {
                    $('#cart_id_' + cart_id).html('✘');
                }
                totalPrice();
            }
        },
        error: function () {
            location.href = '/user/login/';
        },

    });
}

// 改变购物车中所有商品数量状态
$("#all_select").click(function () {

    //    如果有未选中的，应该执行操作是全部选中
    //    并且让自己的按钮变成选中状态
    //    如果全都是选中的，全部取消选中
    var not_selects = [];
    var selects = [];

    $(".is_choose").each(function () {
        if ($(this).attr("is_select").toLowerCase() == "false") {
            // 将未选中添加到指定集合中
            not_selects.push($(this).parents("li").attr("cartid"));
        } else {
            selects.push($(this).parents("li").attr("cartid"));
        }
    });

    if (not_selects.length == 0) {
        // 全部未选中
        $.getJSON("/axf/select_all/", {'action': "unselect"}, function (data) {
            if (data.code == 200) {
                $(".is_choose").each(function () {
                    $(this).find("span").html("✘");
                    $(this).attr("is_select", "false");
                });
                $("#all_select").find("span").html("<span></span>");
                $('#total_price').html('0');
            }
        });
    } else {
        // 全选
        $.getJSON("/axf/select_all/", {'action': "select"}, function (data) {
            if (data.code == 200) {
                $(".is_choose").each(function () {
                    $(this).find("span").html("√");
                    $(this).attr("is_select", "true");
                });
                $("#all_select").find("span").html("<span>√</span>");
                totalPrice();
            }
        });
    }
});

// 订单状态
function change_order(order_id) {
    alert(order_id);
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/change_order_status/',
        type: 'POST',
        data: {'order_id': order_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            if (data.code == 200) {
                // 修改成功, 跳转到个人中心
                location.href = '/axf/mine/';
            }
        },
        error: function () {
            location.href = '/user/login/';
        },

    });
}

$(document).ready(function () {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    // 闪购页面显示选择商品数量
    $.ajax({
        url: '/axf/goods_num/',
        type: 'GET',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            if (data.code == '200') {
                result = data.data;
                for (var i = 0; i < result.length; i++) {
                    $.each(result[i], function (goods_id, goods_num) {
                        $('#num_' + goods_id).html(goods_num);
                    });
                }
            }
        },
        error: function () {
            location.href = '/user/login/';
        },

    });
    totalPrice();
});

// 计算购物车商品总价
function totalPrice() {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/total_price/',
        method: 'GET',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            if (data.code == '200') {
                result = data.data;
                total_price = 0;
                for (var i = 0; i < result.length; i++) {
                    $.each(result[i], function () {
                        price = result[i].goods_price;
                        num = result[i].goods_num;
                        total_price += price * num
                    });
                }
                $('#total_price').html('总价: ' + total_price.toFixed(2));
            }
        },
        error: function () {
            location.href = '/user/login/';
        },
    });
}

