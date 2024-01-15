document.getElementById('searchButton').addEventListener('click', function (event) {

    event.preventDefault();

    const searchInput = document.getElementById('searchInput').value;

    fetch(`/api/search?searchInput=${searchInput}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('searchResultRow').innerText = `Row: ${data.searchResultRow}`;
            document.getElementById('searchResultCol').innerText = `Column: ${data.searchResultCol}`;
            document.getElementById('productName').innerText = `Product Name: ${data.productName}`;
            document.getElementById('productAlternativeName').innerText = `Alternative Name: ${data.productAlternativeName}`;
        })
        .catch(error => console.error('Error:', error));
});

function goToCellPage(row, col) {

    fetch('/api/cell_page', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ row, col }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        window.location.href = data.redirect_url;
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.href = `/cell_page?row=${row}&col=${col}`;
    });
}
