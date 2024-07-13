document.getElementById('validateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    var formData = new FormData(this);
    var jsonData = {};
    for (var [key, value] of formData.entries()) { 
        jsonData[key] = value;
    }
    
    axios.post(window.location.href, jsonData)
    .then(function (response) {
        if (response.data.success) {
            document.getElementById('result').innerHTML = 'Data validated and saved successfully!';
        } else {
            document.getElementById('result').innerHTML = 'Error: ' + response.data.error;
        }
    })
    .catch(function (error) {
        document.getElementById('result').innerHTML = 'Error: ' + error.message;
    });
});