var idValidate = false;
var pwValidate = false;
var pwCheckValidate = false;
var nicknameValidate = false;
var emailValidate = false;
var addressValidate = false;

// var zipnumValidate = $('#userZipcode').val();

function register() {
    if (idValidate == false) {
        $('#userid').focus();
        return;
    } else if (pwValidate == false) {
        $('#userpw').focus();
        return;
    } else if (pwCheckValidate == false) {
        $('#userpw2').focus();
        return;
    } else if (nicknameValidate == false) {
        $('#usernickname').focus();
        return;
    } else if (emailValidate == false) {
        $('#userEmail').focus();
        return;
    }
        // else if (zipnumValidate == '') {
        //     $("#messageZipcode").text('주소를 입력해주세요').removeClass('is-safe').addClass('is-danger')
    // }
    else if (addressValidate == false) {
        $('#userDetailAddress').focus();
        return;
    } else {
        $.ajax({
            type: 'POST',
            url: '/api/register',
            data: {
                id_give: $('#userid').val(),
                pw_give: $('#userpw').val(),
                nickname_give: $('#usernickname').val(),
                email_give: $('#userEmail').val(),
                zipcode_give: $('#userZipcode').val(),
                address_give: $('#userAddress').val(),
                detail_give: $('#userDetailAddress').val(),
            },
            success: function (response) {
                if (response['result'] == 'success') {
                    alert('회원가입이 완료되었습니다.');
                    window.location.href = '/login';
                }
            },
        });
    }
}

//아이디 중복검사
function idCheck() {
    var idRegExp = /^[a-zA-Z0-9]{4,12}$/;
    var _id = $('#userid').val();
    if (_id === '') {
        $('#messageID')
            .text('아이디를 입력해주세요')
            .removeClass('is-safe')
            .addClass('is-danger');
        idValidate = false;
        return;
    }
    if (!idRegExp.test(_id)) {
        $('#messageID')
            .text('아이디는 4-12자의 영문과 숫자만 입력 가능합니다.')
            .removeClass('is-safe')
            .addClass('is-danger');
        $('#userid').focus();
        idValidate = false;
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/api/idCheck',
        data: {
            id_give: $('#userid').val(),
        },
        success: function (response) {
            if (response['exists']) {
                $('#messageID')
                    .text('이미 존재하는 아이디입니다')
                    .removeClass('is-safe')
                    .addClass('is-danger');
                $('#userid').focus();
                idValidate = false;
            } else {
                $('#messageID')
                    .text('사용가능한 아이디 입니다')
                    .addClass('is-safe')
                    .removeClass('is-danger');
                idValidate = true;
            }
        },
    });
}

function pwValidation() {
    var pwRegExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    var _pw = $('#userpw').val();
    if (_pw === '') {
        $('#messagePW')
            .text('비밀번호를 입력해주세요')
            .removeClass('is-safe')
            .addClass('is-danger');
        pwValidate = false;
        return;
    }
    if (!pwRegExp.test(_pw)) {
        $('#messagePW')
            .text('영문과 숫자 조합의 8-20자의 비밀번호를 설정해주세요.\n' +
                '            특수문자(!@#$%^&*)도 사용 가능합니다.')
            .removeClass('is-safe')
            .addClass('is-danger');
        $('#userpw').focus();
        pwValidate = false;
        return;
    } else {
        $('#messagePW')
            .text('사용가능한 비밀번호입니다.')
            .addClass('is-safe')
            .removeClass('is-danger');
        pwValidate = true;
    }
}

function pwCheck() {
    var _pw = $('#userpw').val();
    var _pwCheck = $('#userpw2').val();
    if (_pwCheck === '') {
        $('#messagePW2')
            .text('비밀번호확인은 필수입니다')
            .removeClass('is-safe')
            .addClass('is-danger');
        pwCheckValidate = false;
        return;
    }
    if (_pw === _pwCheck) {
        $('#messagePW2')
            .text('비밀번호가 일치합니다')
            .addClass('is-safe')
            .removeClass('is-danger');
        pwCheckValidate = true;
    } else {
        $('#messagePW2')
            .text('비밀번호가 일치하지 않습니다')
            .removeClass('is-safe')
            .addClass('is-danger');
        pwCheckValidate = false;
        return;
    }
}

//닉네임 중복검사
function nicknameCheck() {
    var _nickname = $('#usernickname').val();
    if (_nickname === '') {
        $('#messageNickName')
            .text('닉네임을 입력해주세요')
            .removeClass('is-safe')
            .addClass('is-danger');
        nicknameValidate = false;
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/api/nicknameCheck',
        data: {
            nickname_give: $('#usernickname').val(),
        },
        success: function (response) {
            if (response['exists']) {
                $('#messageNickName')
                    .text('이미 존재하는 닉네임입니다')
                    .removeClass('is-safe')
                    .addClass('is-danger');
                $('#usernickname').focus();
                nicknameValidate = false;
            } else {
                $('#messageNickName')
                    .text('사용가능한 닉네임 입니다')
                    .addClass('is-safe')
                    .removeClass('is-danger');
                nicknameValidate = true;
            }
        },
    });
}

//이메일 유효성검사
function emailCheck() {
    var _email = $('#userEmail').val();
    var emailRegExp =
        /^[A-Za-z0-9_]+[A-Za-z0-9]*[@]{1}[A-Za-z0-9]+[A-Za-z0-9]*[.]{1}[A-Za-z]{1,3}$/;
    if (_email == '') {
        $('#messageEmail')
            .text('이메일 입력은 필수입니다.')
            .addClass('is-danger')
            .removeClass('is-safe');
        emailValidate = false;
        return;
    }
    if (!emailRegExp.test(_email)) {
        $('#messageEmail')
            .text('올바르지 않는 입력방식입니다.')
            .addClass('is-danger')
            .removeClass('is-safe');
        emailValidate = false;
    } else {
        $('#messageEmail').text('');
        emailValidate = true;
    }
}

function findAddress() {
    daum.postcode.load(function () {
        new daum.Postcode({
            oncomplete: function (data) {
                var addr = '';

                if (data.userSelectedType == 'R') {
                    addr = data.roadAddress;
                } else {
                    addr = data.jibunAddress;
                }

                document.getElementById('userZipcode').value = data.zonecode;
                document.getElementById('userAddress').value = addr;

                document.getElementById('userDetailAddress').focus();
            },
        }).open();
    });
}

function detailAddressCheck() {
    var _detailAddress = $('#userDetailAddress').val();
    if (_detailAddress == '') {
        $('#messageDetailAddress')
            .text('상세주소 입력은 필수입니다.')
            .addClass('is-danger')
            .removeClass('is-safe');
        addressValidate = false;
    } else {
        addressValidate = true;
        $('#messageDetailAddress').text('');
    }
}