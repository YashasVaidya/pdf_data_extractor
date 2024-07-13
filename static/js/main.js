document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    var formData = new FormData(this);
    
    axios.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    .then(function (response) {
        if (response.data.success) {
            window.location.href = '/validate/' + response.data.record_id;
        } else {
            document.getElementById('result').innerHTML = 'Error: ' + response.data.error;
        }
    })
    .catch(function (error) {
        document.getElementById('result').innerHTML = 'Error: ' + error.message;
    });
});