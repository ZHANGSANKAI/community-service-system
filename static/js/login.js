$(function () {
    //点击去注册账号的链接
    $('#link_reg').on('click', function(){
        // Redirect to the registration page
        console.log("niahao")
        window.location.href = '/register/';
    });

        // 获取layui中的form对象
    var form = layui.form;

    // 通过form.verify()函数定义校验规则
    form.verify({
        // 自定义了pwd校验规则
        pwd: [/^[\S]{6,12}$/, '密码必须6到12位且不能出现空格'],
        // 检验两次密码是否一致
        repwd: function (value) {
            // 形参拿到确认密码框中的内容，再与密码框中的内容比较判断
            var pwd = $('.reg-box [name=password]').val();
            if (pwd !== value) {
                return '两次密码不一致！';
            }
        }
    });


});
