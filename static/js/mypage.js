var mypagePwValidate = false;
var mypagePwCheckValidate = false;
var mypageAddressValidate = true;

// var zipnumValidate = $('#userZipcode').val();

function updateInfo() {
    if (mypagePwValidate == false) {
        $("#mypagepw").focus();
        return;
    } else if (mypagePwCheckValidate == false) {
        $("#mypagepw2").focus();
        return;
    } else if (mypageAddressValidate == false) {
        $("#mypageDetailAddress").focus();
        return;
    } else {
        $.ajax({
            type: "POST",
            url: "/api/updateMember",
            data: {
                pw_give: $('#mypagepw').val(),
                zipcode_give: $('#mypageZipcode').val(),
                address_give: $('#mypageAddress').val(),
                detail_give: $('#mypageDetailAddress').val(),
            },
            success: function (response) {
                if (response['result'] == 'success') {
                    alert('회원정보가 수정되었습니다.')
                    $.removeCookie('mytoken')
                    window.location.href = '/login'
                }
            }
        })
    }

}

function mypagePwValidation() {
    var pwRegExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    _pw = $('#mypagepw').val()
    if (_pw === '') {
        $('#messageMypagePW').text('비밀번호를 입력해주세요').removeClass("is-safe").addClass("is-danger");
        mypagePwValidate = false;
        return;
    }

    if (!pwRegExp.test(_pw)) {
        $('#messageMypagePW').text('영문과 숫자 조합의 8-20자의 비밀번호를 설정해주세요. 특수문자(!@#$%^&*)도 사용 가능합니다.').removeClass("is-safe").addClass("is-danger");
        $("#mypagepw").focus();
        mypagePwValidate = false;
        return;
    } else {
        $('#messageMypagePW').text('사용가능한 비밀번호입니다.').addClass("is-safe").removeClass("is-danger");
        mypagePwValidate = true;
    }
}

function mypagePwCheck() {
    var _pw = $('#mypagepw').val();
    var _pwCheck = $('#mypagepw2').val();
    if (_pwCheck === '') {
        $('#messageMypagePW2').text('비밀번호확인은 필수입니다').removeClass("is-safe").addClass("is-danger");
        mypagePwCheckValidate = false;
        return;
    }
    if (_pw === _pwCheck) {
        $('#messageMypagePW2').text('비밀번호가 일치합니다').addClass("is-safe").removeClass("is-danger");
        mypagePwCheckValidate = true;
    } else {
        $('#messageMypagePW2').text('비밀번호가 일치하지 않습니다').removeClass("is-safe").addClass("is-danger");
        mypagePwCheckValidate = false;
        return;
    }
}

function findAddress2() {
    daum.postcode.load(function () {
        new daum.Postcode({
            oncomplete: function (data) {
                var addr = '';

                if (data.userSelectedType == 'R') {
                    addr = data.roadAddress;
                } else {
                    addr = data.jibunAddress;
                }

                document.getElementById('mypageZipcode').value = data.zonecode;
                document.getElementById('mypageAddress').value = addr;

                document.getElementById('mypageDetailAddress').focus();
            }
        }).open();
    });
}

function detailAddressCheck() {
    var _detailAddress = $('#mypageDetailAddress').val();
    if (_detailAddress == '') {
        $('#messageMypageDetailAddress').text("상세주소 입력은 필수입니다.").addClass("is-danger").removeClass("is-safe");
        mypageAddressValidate = false;
    } else {
        mypageAddressValidate = true;
        $('#messageMypageDetailAddress').text("");
    }
}