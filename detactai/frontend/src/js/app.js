// Backend API Configuration (USE THESE)
const API_BASE_URL = 'https://detactai.vercel.app/api'; // Main deployment
// const API_BASE_URL = 'https://detactai-aymnsks-projects.vercel.app/api'; // Alternative

// Check backend connection
async function checkApiStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    if (!response.ok) throw new Error("Backend responded with error");
    document.getElementById('apiStatus').textContent = '✅ Connected';
    document.getElementById('apiStatus').style.color = 'green';
    
    // Additional check for detection endpoint
    const modelResponse = await fetch(`${API_BASE_URL}/debug/model-info`);
    const modelData = await modelResponse.json();
    console.log("Model Info:", modelData);
    
  } catch (error) {
    document.getElementById('apiStatus').textContent = '❌ Disconnected - ' + error.message;
    document.getElementById('apiStatus').style.color = 'red';
    console.error("Connection Error:", error);
  }
}

// Process image through backend
async function processImage() {
  const fileInput = document.getElementById('imageUpload');
  const resultsDiv = document.getElementById('detectionResults');
  const outputImg = document.getElementById('outputImage');

  if (!fileInput.files[0]) {
    alert('Please select an image first!');
    return;
  }

  resultsDiv.innerHTML = '<div class="loading">🔍 Processing image...</div>';
  outputImg.style.display = 'none';

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  try {
    const response = await fetch(`${API_BASE_URL}/detect/image`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Detection Data:", data); // Debug output

    if (!data.detections || data.detections.length === 0) {
      resultsDiv.innerHTML = '<p class="no-results">No objects detected</p>';
      return;
    }

    // Display detection results
    resultsDiv.innerHTML = data.detections.map(d => `
      <div class="detection-item">
        <strong>${d.class}</strong> (${(d.confidence * 100).toFixed(1)}%)
        <div>Coordinates: ${d.bbox.map(n => Math.round(n)).join(', ')}</div>
      </div>
    `).join('');

    // Display processed image
    outputImg.src = `${data.output_url.startsWith('http') ? '' : API_BASE_URL.replace('/api', '')}${data.output_url}`;
    outputImg.onload = () => {
      outputImg.style.display = 'block';
      resultsDiv.innerHTML += `<p>✅ Processed successfully!</p>`;
    };
    outputImg.onerror = () => {
      console.error("Failed to load output image");
      resultsDiv.innerHTML += `<p class="warning">⚠️ Processed image unavailable</p>`;
    };

  } catch (error) {
    resultsDiv.innerHTML = `
      <p class="error">❌ Detection failed</p>
      <p>${error.message}</p>
      <p>Check if:
        <ul>
          <li>Backend is deployed</li>
          <li>CORS is enabled on server</li>
          <li>Model file (yolov8n.pt) exists</li>
        </ul>
      </p>
    `;
    console.error("Detection Error:", error);
  }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', checkApiStatus);
