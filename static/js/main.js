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
            document.getElementById('result').innerHTML = 'File uploaded and processed successfully!';
            displayValidationForm(response.data.extracted_data);
        } else {
            document.getElementById('result').innerHTML = 'Error: ' + response.data.error;
        }
    })
    .catch(function (error) {
        document.getElementById('result').innerHTML = 'Error: ' + error.message;
    });
});

function displayValidationForm(data) {
    var form = document.getElementById('dataValidationForm');
    form.innerHTML = '';
    for (var key in data) {
        form.innerHTML += `
            <div>
                <label for="${key}">${key}:</label>
                <input type="text" id="${key}" name="${key}" value="${data[key]}">
            </div>
        `;
    }
}

document.getElementById('submitValidation').addEventListener('click', function() {
    var form = document.getElementById('dataValidationForm');
    var data = {};
    for (var i = 0; i < form.elements.length; i++) {
        var element = form.elements[i];
        data[element.name] = element.value;
    }
    
    axios.post('/validate', data)
    .then(function (response) {
        if (response.data.success) {
            document.getElementById('finalOutput').innerHTML = 'Validation successful. Final JSON output: <pre>' + JSON.stringify(response.data.final_data, null, 2) + '</pre>';
        } else {
            document.getElementById('finalOutput').innerHTML = 'Error: ' + response.data.error;
        }
    })
    .catch(function (error) {
        document.getElementById('finalOutput').innerHTML = 'Error: ' + error.message;
    });
});

// Initialize the validation form with empty fields
displayValidationForm({
    'patient_1': '', 'amount_1': '',
    'patient_2': '', 'amount_2': '',
    'patient_3': '', 'amount_3': '',
    'patient_4': '', 'amount_4': '',
    'patient_5': '', 'amount_5': ''
});