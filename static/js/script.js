document.addEventListener('DOMContentLoaded', function() {
    // Canvas setup
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    const clearBtn = document.getElementById('clearCanvas');
    const brushColor = document.getElementById('brushColor');
    const brushSize = document.getElementById('brushSize');
    const brushSizeValue = document.getElementById('brushSizeValue');
    const fileInput = document.getElementById('fileInput');

    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // File upload elements
    const dropArea = document.getElementById('dropArea');

    const fileName = document.getElementById('fileName');
    
    // Result elements
    const generateBtn = document.getElementById('generateBtn');

    const resultImage = document.getElementById('resultImage');
    const resultPlaceholder = document.querySelector('.placeholder');
    
    // Drawing variables
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
    
    // Initialize canvas
    initCanvas();
    
    // Drawing event listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
    
    // Touch events for mobile
    canvas.addEventListener('touchstart', handleTouchStart);
    canvas.addEventListener('touchmove', handleTouchMove);
    canvas.addEventListener('touchend', stopDrawing);
    
    // Canvas controls
    clearBtn.addEventListener('click', clearCanvas);
    brushSize.addEventListener('input', updateBrushSize);
    
    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all tabs
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            btn.classList.add('active');
            document.getElementById(`${btn.dataset.tab}-content`).classList.add('active');
        });
    });
    
    // File upload handling
    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropArea.style.borderColor = 'var(--primary-pink)';
        dropArea.style.backgroundColor = 'rgba(255, 105, 180, 0.1)';
    });
    
    dropArea.addEventListener('dragleave', () => {
        dropArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
        dropArea.style.backgroundColor = 'transparent';
    });
    
    dropArea.addEventListener('drop', handleFileDrop);
    dropArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    
    // Generate button
    generateBtn.addEventListener('click', generateImage);
    
    // Functions
    function initCanvas() {
        // Set white background
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    
    function startDrawing(e) {
        isDrawing = true;
        const coords = getCoordinates(e);
        [lastX, lastY] = [coords.x, coords.y];
    }
    
    function draw(e) {
        if (!isDrawing) return;
        
        const coords = getCoordinates(e);
        ctx.strokeStyle = brushColor.value;
        ctx.lineJoin = 'round';
        ctx.lineCap = 'round';
        ctx.lineWidth = brushSize.value;
        
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(coords.x, coords.y);
        ctx.stroke();
        
        [lastX, lastY] = [coords.x, coords.y];
    }
    
    function stopDrawing() {
        isDrawing = false;
    }
    
    function handleTouchStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousedown', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    }
    
    function handleTouchMove(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousemove', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    }
    
    function getCoordinates(e) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }
    
    function clearCanvas() {
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    
    function updateBrushSize() {
        brushSizeValue.textContent = `${brushSize.value}px`;
    }
    
    function handleFileDrop(e) {
        e.preventDefault();
        dropArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
        dropArea.style.backgroundColor = 'transparent';
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFile(file);
        }
    }
    
    function handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    }
    
    function handleFile(file) {
        fileName.textContent = file.name;
        
        // Preview file (optional)
        const reader = new FileReader();
        reader.onload = function(e) {
            // You could create a preview here if needed
        };
        reader.readAsDataURL(file);
    }
    
   async function generateImage() {
    let formData = new FormData();

    // Determine if drawing tab is active
    if (document.querySelector('.tab-btn[data-tab="draw"]').classList.contains('active')) {
        const imageData = canvas.toDataURL('image/png');
        formData.append('imageData', imageData);
    } else {
        if (fileInput.files.length === 0) {
            alert('Please upload a sketch image first');
            return;
        }
        formData.append('file', fileInput.files[0]);
    }

    // Show loading spinner
    generateBtn.classList.add('loading');

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Display the generated image
        resultPlaceholder.style.display = 'none';
        resultImage.src = data.result;
        resultImage.style.display = 'block';
        resultImage.style.opacity = '0';

        setTimeout(() => {
            resultImage.style.transition = 'opacity 0.5s ease';
            resultImage.style.opacity = '1';
        }, 100);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate image. Please try again.');
    } finally {
        generateBtn.classList.remove('loading');
    }
}

});