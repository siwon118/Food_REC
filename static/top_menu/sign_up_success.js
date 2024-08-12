// JavaScript를 사용하여 사용자 아이디를 동적으로 삽입
var usernameElement = document.getElementById('username');
var username = ''; // 사용자 아이디가 들어갈 변수

// 여기에 사용자 아이디를 가져오는 로직을 작성해야 합니다.
// 사용자 아이디를 변수 username에 할당하는 예시 코드:
username = '사용자 아이디';

// 사용자 아이디를 페이지에 삽입
usernameElement.textContent = username;


// home 버튼을 눌러 선호도 조사 페이지로 넘어가기
function home() {
    // 다음 페이지의 URL
    const nextPageUrl = "home.html";
    // 페이지 이동
    window.location.href = nextPageUrl;
}

// my_info 버튼을 눌러 선호도 조사 페이지로 넘어가기
function my_info() {
    // 다음 페이지의 URL
    const nextPageUrl = "my_info.html";
    // 페이지 이동
    window.location.href = nextPageUrl;
}