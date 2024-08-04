document.getElementById('designForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const designTemp = document.getElementById('inputDesignTemp').value;
    const designPress = document.getElementById('inputDesignPress').value;

    fetch('/your-django-endpoint/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ensure you include the CSRF token
        },
        body: JSON.stringify({
            design_temp: designTemp,
            design_press: designPress
        })
    })
    .then(response => response.json())
    .then(data => {
        updateTable(data);
    })
    .catch(error => console.error('Error:', error));
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function updateTable(data) {
    const tableBody = document.querySelector('#pipe_data_flange tbody');
    tableBody.innerHTML = '';  // Clear existing table data

    for (const [material, value] of Object.entries(data.organised_flange_data)) {
        const row = document.createElement('tr');
        const materialCell = document.createElement('td');
        materialCell.textContent = material;
        row.appendChild(materialCell);

        for (const flange of data.unique_flange_ratings) {
            const cell = document.createElement('td');
            const spec = value[flange];
            if (spec) {
                cell.textContent = spec.max_p.toFixed(1);
                cell.className = spec.allowable ? 'table-success border-dark' : 'table-danger border-dark';
            } else {
                cell.textContent = '-';
            }
            cell.style.minWidth = '75px';
            row.appendChild(cell);
        }

        tableBody.appendChild(row);
    }
}
