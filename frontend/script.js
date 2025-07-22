alert("JS loaded");
document.getElementById('themeToggle').addEventListener('click', () => {
    const body = document.body;
    const isDark = body.classList.toggle('light-mode');
    body.classList.toggle('dark-mode', !isDark);
    document.getElementById('themeToggle').textContent = isDark ? '☀️' : '🌙';
});

const pdfUpload = document.getElementById("pdfUpload");
const inputSection = document.getElementById("inputSection");

pdfUpload.addEventListener("change", async () => {
    const file = pdfUpload.files[0];
    if (file && file.type !== "application/pdf") {

        inputSection.classList.add("hidden");
        alert("Please upload a valid PDF file.");
    } else {

        inputSection.classList.remove("hidden");
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/api/upload-pdf", {
                method: "POST",
                body: formData,
            });

            

            if (response.ok) {
                const result = await response.json();
                alert("✅ PDF uploaded and processed successfully!");
                console.log("📄 File URL:", result.url); // Optional: show S3 URL
            } else {
                let errorText = await response.text();
                alert("❌ Upload failed: " + errorText);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("❌ An unexpected error occurred.");
        }


    }
});

const sendMessage = () => {
    const input = document.getElementById('userInput');
    const chatBox = document.getElementById('chatBox');

    if (input.value.trim() === '') return;

    const userMessage = document.createElement('div');
    userMessage.textContent = input.value;
    userMessage.style.margin = '0.5rem 0';
    chatBox.appendChild(userMessage);

    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;
};

// Handle click on send button
document.getElementById('sendButton').addEventListener('click', sendMessage);

// Handle Enter key press
document.getElementById('userInput').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        //   event.preventDefault();
        sendMessage();
    }
});