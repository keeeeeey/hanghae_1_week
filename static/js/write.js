let image_checker = false

$(document).ready(function () {
});

function posting() {

    let id = $('#user_id').text();
    let title = $('#title').val();
    let title_check = title.trim();
    if (title_check == null || title_check == "") {
        alert('title 을 입력하세요!')
        return;
    }
    let content = $('#contents').val();

    if (image_checker) {
        let fileInput = document.getElementsByClassName("file");

        let file = $('#file')[0].files[0]
        let filename = file['name']

        let form_data = new FormData()

        form_data.append('id_give', id)
        form_data.append('title_give', title)
        form_data.append('content_give', content)
        form_data.append('image', file)
        form_data.append('image_name', filename)
        form_data.append('image_checker', image_checker)

        $.ajax({
            type: "POST",
            url: "/api/posting",
            processData: false,
            contentType: false,
            data: form_data,
            success: function (response) {
                if (response["result"] == "success") {
                    alert("질문이 등록되었습니다.");
                    window.location.reload();
                    location.replace("/");
                    //main page move
                }
            },
            error: function (e) {
                alert('fail');
            }
        })

    } else {

        let form_data = new FormData()

        form_data.append('id_give', id)
        form_data.append('title_give', title)
        form_data.append('content_give', content)
        form_data.append('image_checker', image_checker)
        console.log('check posting: ' + id)

        $.ajax({
            type: "POST",
            url: "/api/posting",
            processData: false,
            contentType: false,
            data: form_data,
            success: function (response) {
                if (response["result"] == "success") {
                    alert("질문등록!!");
                    window.location.reload();
                    location.replace("/");
                    //main page move
                }
            },
            error: function (e) {
                alert('fail');
            }
        })

    }

}

function cancel() {
    if (!confirm("정말로 취소하시겠습니까?")) {
        return;
    } else {
        location.replace("/"); //main page local address
    }
}

$('#btnUpload').on('click', function (event) {
    event.preventDefault();

    var form = $('#uploadForm')[0]
    var data = new FormData(form);

    $('#btnUpload').prop('disabled', true);

    $.ajax({
        type: "POST",
        enctype: 'multipart/form-data',
        url: "/upload",
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
        success: function (data) {
            $('#btnUpload').prop('disabled', false);
            alert('success')
        },
        error: function (e) {
            $('#btnUpload').prop('disabled', false);
            alert('fail');
        }
    });
})

function loadFile(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.querySelector('.file-name').textContent = input.files[0].name;
            document.getElementById('preview').src = e.target.result;
            $('#preview').toggleClass('is-hidden')
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function toMypage() {

    window.location.href = "/api/mypage";

}

function toLogout() {

    $.removeCookie('mytoken');
    window.location.href = '/'

}