$(document).ready(function () {
});

function posting() {
    let id = $('#user_id').val();
    let title = $('#title').val();
    let content = $('#contents').val();
    //let form_data = new FormData()
    let images = localStorage.getItem('imgs')

    //form_data.append("title_give", title)
    //form_data.append("content_give", content)

    $.ajax({
        type: "POST",
        url: "/api/posting",
        data: {
            'id_give': id,
            'title_give': title,
            'content_give': content,
            'image_give': images
        },
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"]);
                window.location.reload();
                location.replace("/");
                //main page move
            }
        }
    })
}

function cancel() {
    if (!confirm("정말로 취소하시겠습니까?")) {
        return;
    } else {
        location.replace("/"); //main page local address
    }
}

// image uploade
function loadFile(input) {
    let imageArray = [];
    const imageFiles = input.files;
    const imageNames = $('.image-list')
    const images = $('.show-uploaded')

    imageFiles.innerText = ''
    images.innerText = ''

    for (let i = 0; i < imageFiles.length; i++) {
        const nameTemplates = `<li class="image-name">'${imageFiles[i].name}'</li>`
        imageNames.append(nameTemplates)

        const imageTemplates = `<img src="${URL.createObjectURL(imageFiles[i])}" class="img">`
        images.append(imageTemplates)

        imageArray.push(URL.createObjectURL(imageFiles[i]))
    }
    localStorage.setItem('imgs', JSON.stringify(imageArray))
}