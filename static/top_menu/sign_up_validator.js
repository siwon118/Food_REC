// 아이디 중복 확인
function checkDuplicate() {
    var userid = document.getElementById("userid").value;
    // 여기에 중복 확인하는 로직을 추가

    // 임시로 아이디가 중복되었다고 가정 : true로
    var isDuplicate = false; // 중복 여부를 확인하는 로직을 추가하여 결정

    // 중복되는 아이디가 있으면 메시지 표시
    if (isDuplicate) {
        document.getElementById("duplicateMessage").innerText = "이미 사용 중인 아이디입니다. 다른 아이디를 입력해주세요.";
    } else {
        document.getElementById("duplicateMessage").innerText = "사용 가능한 아이디니다.";
    }
}

// 생년월일 선택을 위한 JavaScript 코드
// 페이지가 로드될 때 실행되는 함수
window.onload = function() {
    // 년도 선택
    var yearSelect = document.getElementById("year");
    var currentYear = new Date().getFullYear();
    for (var i = currentYear; i >= 1900; i--) {
        var option = document.createElement("option");
        option.text = i + "년";
        option.value = i;
        yearSelect.add(option);
    }

    // 월 선택
    var monthSelect = document.getElementById("month");
    for (var i = 1; i <= 12; i++) {
        var option = document.createElement("option");
        option.text = i + "월";
        option.value = i;
        monthSelect.add(option);
    }

    // 일 선택 (1일부터 31일까지)
    var daySelect = document.getElementById("day");
    for (var i = 1; i <= 31; i++) {
        var option = document.createElement("option");
        option.text = i + "일";
        option.value = i;
        daySelect.add(option);
    }
};

// 이메일 직접 입력하기
function selectEmail(select) {
    var email2 = document.getElementById("email2");
    
    if (select.value === 'manual') {
        email2.value = '';
        email2.readOnly = false;
        email2.focus();
    } else {
        email2.value = select.value;
        email2.readOnly = true;
    }
}


// next 버튼을 눌러 선호도 조사 페이지로 넘어가기
function submit_preference() {
    // 다음 페이지의 URL
    const nextPageUrl = "submit_preference.html";
    // 페이지 이동
    window.location.href = nextPageUrl;
}

//회원가입 유효성검사


