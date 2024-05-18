function scrapeUrl() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        var currentUrl = tabs[0].url;
        console.log("Current URL:", currentUrl);

        // URL'yi Python sunucusuna gönderme
        fetch('http://127.0.0.1:5000/url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({url: currentUrl})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('HTTP error, status = ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log("Python'dan gelen yanıt:", data.output);
            var responseDiv = document.getElementById('response');
            responseDiv.innerHTML = ''; // Önceki içeriği temizle
            var comments = data.output.split("--------------");
            comments.forEach(function(comment) {
                var div = document.createElement('div');
                var sentiment = '';
                if (comment.includes("Positive")) {
                    sentiment = '<span style="color: green;">Positive</span>';
                } else if (comment.includes("Negative")) {
                    sentiment = '<span style="color: red;">Negative</span>';
                } else {
                    sentiment = '<span style="color: gray;">Neutral</span>';
                }
                div.innerHTML = sentiment + ": " + comment;
                responseDiv.appendChild(div);
            });
        })
        .catch(error => {
            console.error('Fetch işlemi başarısız:', error.message);
            // Hata durumunda kullanıcıya uygun bir hata mesajı gösterme
            document.getElementById('response').innerText = "Hata: " + error.message;
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('scrapeButton').addEventListener('click', scrapeUrl);
});
