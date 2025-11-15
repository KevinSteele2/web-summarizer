document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('frm').addEventListener('submit', (e) => {
        e.preventDefault();
        const url = document.getElementById('url').value.trim();
        document.getElementById('out').textContent = "Loading...";
        fetch('/summarize', {
            method: 'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({url})
        })
        .then(r => r.json())
        .then(data => document.getElementById('out').textContent = data.summary)
        .catch(err => document.getElementById('out').textContent = "Error: " + err);
    });
});