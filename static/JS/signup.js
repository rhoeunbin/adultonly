function doOpenCheck(chk) {
    var obj_pos = document.getElementsByName("job_pos");
    var obj = document.getElementsByName("job");
    for (var i = 0; i < obj.length; i++) {
        if (obj[i] != chk) {
            obj[i].checked = false;
            obj[i].required = "";
            obj_pos[i].style.backgroundColor = "";
            obj_pos[i].style.color = "gray";
        }
        else {
            obj_pos[i].style.backgroundColor = "#4b0e66";
            obj_pos[i].style.color = "white";
        }
    }
}

// 도메인 직접 입력 or domain option 선택
const domainListEl = document.querySelector('#domain-list')
const domainInputEl = document.querySelector('#domain-txt')
// select 옵션 변경 시
domainListEl.addEventListener('change', (event) => {
    // option에 있는 도메인 선택 시
    if (event.target.value !== "type") {
        // 선택한 도메인을 input에 입력하고 disabled
        domainInputEl.value = event.target.value
        domainInputEl.readOnly = true
        domainInputEl.style.backgroundColor = "white"
    } else { // 직접 입력 시
        // input 내용 초기화 & 입력 가능하도록 변경
        domainInputEl.value = ""
        domainInputEl.readOnly = false
    }
})

const idValidation = document.querySelector("#id-check");
// const idVal = document.querySelector("#info__id");
const p = document.querySelector("#id-error");
idValidation.addEventListener('click', function () {
    const checkId = document.querySelector("#check_id");
    const regExp = /^[a-z0-9]{4,20}$/;
    if (!regExp.test(checkId.value)) {
        p.innerText = "아이디는 4~20자 영어 소문자, 숫자를 사용하세요.";
        p.style.color = "red";
    } else {
        p.innerText = "";
        axios({
            method: 'get',
            url: "/accounts/signup/",
            params: {
                'userId': `${checkId.value}`
            }
        })
            .then((response) => {
                console.log(response.data.check)
                if (response.data.check) {
                    p.innerText = "이미 등록된 아이디 입니다.";
                }
                else {
                    p.innerText = "사용 가능한 아이디 입니다.";
                    p.style.color = 'green';
                }
            })
            .catch((response) => {
                console.log('경고')
            })
    }
})