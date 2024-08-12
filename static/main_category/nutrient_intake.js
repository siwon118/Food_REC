// 영양소 입력 요소와 그래프 업데이트
function updateProgressBar(inputId, progressId) {
    const input = document.getElementById(inputId);
    const progress = document.getElementById(progressId);
    const value = parseInt(input.value);

    if (value > 100) {
        // 100%를 초과할 경우 색상을 진하게 설정
        progress.style.backgroundColor = 'Red';
        progress.style.width = '100%';
    } else {
        // 그 외의 경우 기본 색상 설정
        progress.style.backgroundColor = 'ForestGreem';
        progress.style.width = value + '%';
    }
}

// 입력 값 변경 감지 및 그래프 업데이트
document.addEventListener('DOMContentLoaded', function() {
    const nutrients = ['energy', 'na', 'cbh', 'sugar', 'fat', 'transfat', 'saturatedfat', 'kol', 'prot'];

    nutrients.forEach(nutrient => {
        const inputId = nutrient;
        const progressId = nutrient + '-progress';

        const input = document.getElementById(inputId);
        input.addEventListener('input', function() {
            updateProgressBar(inputId, progressId);
        });

        // 초기화
        updateProgressBar(inputId, progressId);
    });
});
