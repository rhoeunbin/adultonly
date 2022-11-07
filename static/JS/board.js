// const kor = document.querySelector("#kor");
// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
// kor.addEventListener('click', function () {
//     console.log(kor)
//     console.log(kor.value)
//     $.ajax({
//         type: "post",
//         url: "/articles/board/",
//         data: {
//             'csrfmiddlewaretoken': csrftoken,
//             "code": kor.value,
//         },
//         success: (response) => {
//             console.log(response.restaurants)
//             $('#masterdiv').empty();
//             // for (let i = 0; i < response.restaurants.length; i++) {

//             // }
//         }
//     })
// })

const all = document.querySelector("#all");
const kor = document.querySelector("#kor");
const cha = document.querySelector("#cha");
const jap = document.querySelector("#jap");
const yang = document.querySelector("#yang");
const world = document.querySelector("#world");
const caf = document.querySelector("#caf");
const pub = document.querySelector("#pub");
all.addEventListener("click", function () {
    window.location = `/articles/board/`
})
kor.addEventListener("click", function () {
    window.location = `/articles/board/${kor.value}`
})
cha.addEventListener("click", function () {
    window.location = `/articles/board/${cha.value}`
})
jap.addEventListener("click", function () {
    window.location = `/articles/board/${jap.value}`
})
yang.addEventListener("click", function () {
    window.location = `/articles/board/${yang.value}`
})
world.addEventListener("click", function () {
    window.location = `/articles/board/${world.value}`
})
caf.addEventListener("click", function () {
    window.location = `/articles/board/${caf.value}`
})
pub.addEventListener("click", function () {
    window.location = `/articles/board/${pub.value}`
})