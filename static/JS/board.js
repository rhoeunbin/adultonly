const kor = document.querySelector("#kor");
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
kor.addEventListener('click', function () {
    console.log(kor)
    console.log(kor.value)
    $.ajax({
        type: "post",
        url: "/articles/board/",
        data: {
            'csrfmiddlewaretoken': csrftoken,
            "code": kor.value,
        },
        success: (response) => {
            console.log(response.restaurants)
            // for (let i = 0; i < response.restaurants.length; i++) {

            // }
        }
    })
})