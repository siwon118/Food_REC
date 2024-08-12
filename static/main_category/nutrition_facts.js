// 작동 xxxx
document.getElementById('upload-button').addEventListener('click', function() {
    document.getElementById('upload-photo').click();
});

document.getElementById('upload-photo').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.getElementById('uploaded-photo');
            img.src = e.target.result;
            img.style.display = 'block';
            document.getElementById('upload-instruction').style.display = 'none';
        }
        reader.readAsDataURL(file);
    }
});

window.onload = function() {
    const testImg = document.querySelector('.test-img');
    testImg.style.display = 'block';
};


// 작동 xxxxx
$('#upload-button').click(function () {
    // 파일 선택창 열기
    $('#upload-photo').click();
  });

  // 파일 선택 시
  $('#upload-photo').change(function () {
    var file = this.files[0];
    var formData = new FormData();
    formData.append('file', file);

    // 파일을 서버로 업로드
    $.ajax({
      url: '/upload',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        // 결과값 표시
        $('#result').text(response.food_name);
      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  });


  






  document.getElementById('analyze-button').addEventListener('click', function() {
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/analyze_ocr', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                document.getElementById('energy-value').innerText = data.energy + 'kcal';
                document.getElementById('na-value').innerText = data.na + 'mg';
                document.getElementById('cbh-value').innerText = data.cbh + 'g';
                document.getElementById('sugar-value').innerText = data.sugar + 'g';
                document.getElementById('fat-value').innerText = data.fat + 'g';
                document.getElementById('transfat-value').innerText = data.transfat + 'g';
                document.getElementById('saturatedfat-value').innerText = data.saturatedfat + 'g';
                document.getElementById('kol-value').innerText = data.kol + 'mg';
                document.getElementById('prot-value').innerText = data.prot + 'g';

                const allergyInfo = data.allergy.length > 0 ? data.allergy.join(', ') : '없음';
                document.getElementById('allergy-info').innerText = allergyInfo;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to analyze the image.');
        });
    }
});