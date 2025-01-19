// File Path: C:\Users\Msi\Desktop\Speech to Text\static\scripts.js

document.addEventListener("DOMContentLoaded", function () {
    const uploadOnlyButton = document.getElementById("upload-only");
    const uploadConvertButton = document.getElementById("upload-convert");
    const fileInput = document.querySelector('input[type="file"]');
    const statusMessage = document.getElementById("status-message");

    // Event listener for "Upload Only"
    uploadOnlyButton.addEventListener("click", function (event) {
        event.preventDefault();
        const file = fileInput.files[0];
        if (file) {
            uploadFile(file, "/upload");
        } else {
            statusMessage.textContent = "Please select a file to upload.";
            statusMessage.style.color = "red";
        }
    });

    // Event listener for "Upload and Convert to Text"
    uploadConvertButton.addEventListener("click", function (event) {
        event.preventDefault();
        const file = fileInput.files[0];
        if (file) {
            uploadFile(file, "/upload-and-convert");
        } else {
            statusMessage.textContent = "Please select a file to upload.";
            statusMessage.style.color = "red";
        }
    });

    // Function to handle file upload
    function uploadFile(file, endpoint) {
        const validTypes = ['audio/wav', 'audio/mp3', 'audio/flac', 'audio/m4a', 'audio/ogg'];

        if (!validTypes.includes(file.type)) {
            statusMessage.textContent = "Please upload a valid audio file (.wav, .mp3, .flac, .m4a, .ogg).";
            statusMessage.style.color = "red";
            return;
        }

        statusMessage.textContent = `Processing: ${file.name}`;
        statusMessage.style.color = "blue";

        const formData = new FormData();
        formData.append("file", file);

        fetch(endpoint, {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.download_url) {
                    statusMessage.textContent = `File processed successfully in ${data.processing_time}s!`;
                    statusMessage.style.color = "green";
                    const downloadLink = document.createElement("a");
                    downloadLink.href = data.download_url;
                    downloadLink.textContent = "Download Excel Sheet";
                    downloadLink.setAttribute("download", "");
                    document.body.appendChild(downloadLink);
                    downloadLink.click();
                    document.body.removeChild(downloadLink);
                } else if (data.error) {
                    statusMessage.textContent = `Error: ${data.error}`;
                    statusMessage.style.color = "red";
                }
            })
            .catch((error) => {
                statusMessage.textContent = "Error uploading file.";
                statusMessage.style.color = "red";
            });
    }
});
