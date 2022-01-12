function signIn() {
    alert('start signIn function for login');

    let username = $('.input-userID').val();
    let password = $('.input-userPW').val();

    if (username == '') {
        $('#help-id-login').text('아이디를 입력해주세요.');
        $('.input-userID').focus();
        return;
    } else {
        $('#help-id-login').text('');
    }

    if (password == '') {
        $('#help-password-login').text('비밀번호를 입력해주세요.');
        $('.input-userPW').focus();
        return;
    } else {
        $('#help-password-login').text('');
    }

    alert('start ajax for login');

    $.ajax({
        type: 'POST',
        url: '/api/login',
        data: {
            username_give: username,
            password_give: password,
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                alert('로그인 완료!');
                window.location.href = '/';
            } else {
                alert(response['msg']);
            }
        },
    });
}