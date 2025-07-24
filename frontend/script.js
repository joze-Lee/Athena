
document.getElementById('themeToggle').addEventListener('click', () => {
    const body = document.body;
    const isDark = body.classList.toggle('light-mode');
    body.classList.toggle('dark-mode', !isDark);
    document.getElementById('themeToggle').textContent = isDark ? '☀️' : '🌙';
});

const pdfUpload = document.getElementById("pdfUpload");
const inputSection = document.getElementById("inputSection");
const overlay = document.getElementById('overlay-loader');

function showLoader() {
  overlay.classList.remove("hidden");
}

function hideLoader() {
  overlay.classList.add("hidden");
}


// Interpolate between two colors
function interpolateColor(color1, color2, factor) {
    const c1 = parseInt(color1.slice(1), 16);
    const c2 = parseInt(color2.slice(1), 16);
  
    const r1 = (c1 >> 16) & 0xff;
    const g1 = (c1 >> 8) & 0xff;
    const b1 = c1 & 0xff;
  
    const r2 = (c2 >> 16) & 0xff;
    const g2 = (c2 >> 8) & 0xff;
    const b2 = c2 & 0xff;
  
    const r = Math.round(r1 + (r2 - r1) * factor);
    const g = Math.round(g1 + (g2 - g1) * factor);
    const b = Math.round(b1 + (b2 - b1) * factor);
  
    return `rgb(${r}, ${g}, ${b})`;
  }
  
  // Apply the colors on load
  function setDotColors() {
    const startColor = "#a336c4";
    const endColor = "#00ffff";
    const dots = document.querySelectorAll('.dot');
  
    dots.forEach((dot, index) => {
      const factor = index / (dots.length - 1);
      dot.style.setProperty('--dot-color', interpolateColor(startColor, endColor, factor));
    });
  }
  
  // Run once DOM is ready
  document.addEventListener("DOMContentLoaded", setDotColors);
  


pdfUpload.addEventListener("change", async () => {
    // console.log("i am in for upload")
    const file = pdfUpload.files[0];
    if (file && file.type !== "application/pdf") {

        inputSection.classList.add("hidden");
        alert("Please upload a valid PDF file.");
    } else {

        
        const formData = new FormData();
        formData.append("file", file);

        try {
            // overlay.classList.remove("hidden"); // Show loader
            showLoader();
            const response = await fetch("/api/upload-pdf", {
                method: "POST",
                body: formData,
            });

            
            if (response.ok) {

                const result = await response.json();
                // overlay.classList.add("hidden"); // Hide loader
                inputSection.classList.remove("hidden");
                // alert("✅ PDF uploaded and processed successfully!");
                console.log("✅  " +result.message); // Optional: show S3 URL
            } else {
                let errorText = await response.text();
                alert("❌ Upload failed: " + errorText);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("❌ An unexpected error occurred.");
        }
        finally{
            // overlay.classList.add("hidden"); // Hide loader
            hideLoader();
            pdfUpload.value = null;
        }


    }
});


const sendMessage = async() => {
    const input = document.getElementById('userInput');
    const chatBox = document.getElementById('chatBox');

    const userText = input.value.trim();
    if (userText === '') return;

     // Show user's message
    const userMessage = document.createElement('div');
    // userMessage.textContent = input.value;
    // userMessage.textContent = `🧑 You: ${userText}`;
    // userMessage.style.margin = '0.5rem 0';
    // userMessage.style.color = '#a336c4'
    // userMessage.style.fontWeight = 'bold';
    // chatBox.appendChild(userMessage);





    // const userMessage = document.createElement('div');
    userMessage.textContent = input.value;
    userMessage.style.margin = '8px 0';
    userMessage.style.padding = '12px 20px';
    userMessage.style.backgroundColor = '#00ffff';
    userMessage.style.color = '#222'; // Dark text for contrast
    userMessage.style.alignSelf = 'flex-start';
    userMessage.style.borderRadius = '20px 20px 20px 4px';
    userMessage.style.maxWidth = '60%';
    userMessage.style.boxShadow = '0 2px 8px rgba(163, 54, 196, 0.3)';
    userMessage.style.fontFamily = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    userMessage.style.fontSize = '15px';
    chatBox.appendChild(userMessage);
    


      // Clear input & scroll
      input.value = '';
      chatBox.scrollTop = chatBox.scrollHeight;

      const loadingMessage = document.createElement('div');
    loadingMessage.textContent = "🤖 Athena is thinking...";
    loadingMessage.style.color = 'gray';
    chatBox.appendChild(loadingMessage);

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: userText })
        });

        const data = await response.json();
        chatBox.removeChild(loadingMessage);

        if (response.ok && data.results.length > 0) {
            // Add Athena's response(s)
            // data.results.forEach((item, idx) => {
            //     const botMessage = document.createElement('div');
            //     botMessage.textContent = `🤖 Jarvis (${idx + 1}): ${item.text}`;
            //     botMessage.style.margin = '0.5rem 0';
            //     botMessage.style.color = '#1a73e8';
            //     chatBox.appendChild(botMessage);
            // });

            // const topAnswer = data.results[0];
            // const botMessage = document.createElement('div');
            // botMessage.textContent = `🤖 Athena: ${topAnswer.text}`;
            // botMessage.style.margin = '0.5rem 0';
            // botMessage.style.color = '#00ffff';
            // chatBox.appendChild(botMessage);


            const topAnswer = data.results[0];

            // 🤖 Athena Message (Right Aligned, Cyan Bubble)
            const botMessage = document.createElement('div');
            botMessage.textContent = topAnswer.text;
            botMessage.style.margin = '8px 0';
            botMessage.style.padding = '12px 20px';
            botMessage.style.backgroundColor = '#a336c4';
            botMessage.style.color = 'white';
            botMessage.style.alignSelf = 'flex-end';
            botMessage.style.borderRadius = '20px 20px 4px 20px';
            botMessage.style.maxWidth = '60%';
            botMessage.style.boxShadow = '0 2px 8px rgba(0, 255, 255, 0.3)';
            botMessage.style.fontFamily = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
            botMessage.style.fontSize = '15px';

            chatBox.appendChild(botMessage);
            chatBox.scrollTop = chatBox.scrollHeight;

        } else {
            const errorMessage = document.createElement('div');
            errorMessage.textContent = "❌ No results found.";
            errorMessage.style.color = 'red';
            chatBox.appendChild(errorMessage);
        }
    } catch (error) {
        chatBox.removeChild(loadingMessage);
        const errorMessage = document.createElement('div');
        errorMessage.textContent = "❌ Failed to get response from Jarvis.";
        errorMessage.style.color = 'red';
        chatBox.appendChild(errorMessage);
        console.error("Fetch error:", error);
    }

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