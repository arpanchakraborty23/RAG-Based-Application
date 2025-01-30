function uploadFile() {
    let fileInput = document.getElementById("fileInput").files[0];
    if (!fileInput) {
        alert("Please select a file!");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("uploadMessage").innerText = data.message;
    })
    .catch(error => console.error("Error uploading file:", error));
}

function sendQuery() {
    let userQuery = document.getElementById("userQuery").value;
    if (!userQuery.trim()) return;

    let chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userQuery}</p>`;

    fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuery })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<p><strong>AI:</strong> ${data.answer}</p>`;
        document.getElementById("userQuery").value = "";
    })
    .catch(error => console.error("Error:", error));
}
