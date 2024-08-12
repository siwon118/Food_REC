// next 버튼을 눌러 선호도 조사 페이지로 넘어가기
function sign_up_success() {
    // 다음 페이지의 URL
    const nextPageUrl = "sign_up_success.html";
    // 페이지 이동
    window.location.href = nextPageUrl;
}

// 사진을 클릭해도 체크박스에 표시되도록
function toggleCheckbox(foodItem) {
    // foodItem 내부에서 체크박스를 찾습니다.
    const checkbox = foodItem.querySelector('input[type="checkbox"]');

    // 체크박스가 존재하고 상태를 변경합니다.
    if (checkbox) {
        checkbox.checked = !checkbox.checked;
    }
}

