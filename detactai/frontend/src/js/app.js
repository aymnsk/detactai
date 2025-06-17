// Backend API Base URL (Update with your Vercel URL)
const API_BASE_URL = window.location.hostname.includes('vercel.app') 
  ? 'https://your-vercel-app.vercel.app/api' 
  : 'http://localhost:8000/api';

// Check backend connection
async function checkApiStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    document.getElementById('apiStatus').textContent = '✅ Connected';
    document.getElementById('apiStatus').style.color = 'green';
  } catch (error) {
    document.getElementById('apiStatus').textContent = '❌ Disconnected';
    document.getElementById('apiStatus').style.color = 'red';
    console.error("API Connection Error:", error);
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

  resultsDiv.innerHTML = '<p>Processing...</p>';
  outputImg.style.display = 'none';

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  try {
    const response = await fetch(`${API_BASE_URL}/detect/image`, {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    // Display detection results
    resultsDiv.innerHTML = data.detections.map(d => `
      <div class="detection-item">
        <strong>${d.class}</strong> (${(d.confidence * 100).toFixed(1)}%)
        <div>Bounding box: [${d.bbox.map(n => n.toFixed(1)).join(', ')}]</div>
      </div>
    `).join('');

    // Display processed image
    outputImg.src = `${API_BASE_URL.replace('/api', '')}${data.output_url}`;
    outputImg.style.display = 'block';

  } catch (error) {
    resultsDiv.innerHTML = '<p class="error">Detection failed. Check console.</p>';
    console.error("Detection Error:", error);
  }
}

// Initialize
checkApiStatus();
