document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const fileDropArea = document.getElementById('dropArea');
    const fileMsg = document.querySelector('.file-msg');
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsSection = document.getElementById('resultsSection');

    // Drag and drop visuals
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileMsg.textContent = fileInput.files[0].name;
            resultsSection.classList.add('hidden'); // hide previous results
        }
    });

    fileDropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileDropArea.classList.add('dragover');
    });

    fileDropArea.addEventListener('dragleave', () => {
        fileDropArea.classList.remove('dragover');
    });

    fileDropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileDropArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            fileMsg.textContent = fileInput.files[0].name;
            resultsSection.classList.add('hidden');
        }
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (fileInput.files.length === 0) return;

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        // UI State: Loading
        submitBtn.disabled = true;
        loadingIndicator.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/process', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                let errorMsg = 'Server error';
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.error || errorMsg;
                } catch(e) {
                    errorMsg = `Server returned status ${response.status}: ${response.statusText}`;
                }
                throw new Error(errorMsg);
            }

            const data = await response.json();
            
            // Populate UI with response
            renderResults(data);

        } catch (error) {
            alert('Error processing document: ' + error.message);
        } finally {
            // UI State: Reset
            submitBtn.disabled = false;
            loadingIndicator.classList.add('hidden');
        }
    });

    function renderResults(data) {
        // Raw Text
        document.getElementById('rawText').textContent = data.raw_text || 'No text extracted.';

        // Overall Validation Status
        const valSummary = document.getElementById('validationSummary');
        if (data.validation_status.is_valid) {
            valSummary.textContent = 'All Fields Validated Successfully';
            valSummary.className = 'status-badge status-valid';
        } else {
            valSummary.textContent = 'Validation Failed: Please check the highlighted fields';
            valSummary.className = 'status-badge status-invalid';
        }

        const recordsContainer = document.getElementById('recordsContainer');
        recordsContainer.innerHTML = ''; // Clear previous records

        const records = data.structured_data;
        const validations = data.validation_status.records;

        records.forEach((record, index) => {
            const valInfo = validations[index].fields;

            const gridHtml = `
                <h3 style="margin: 1.5rem 0 1rem; color: #cbd5e1; border-bottom: 1px solid #334155; padding-bottom: 0.5rem;">Record #${index + 1}</h3>
                <div class="data-grid">
                    ${['Name', 'Amount', 'Date', 'ID'].map(field => {
                        const val = record[field];
                        const displayVal = val !== null && val !== undefined ? val : 'Not found';
                        const fieldValid = valInfo[field].valid;
                        const statusIcon = fieldValid ? '✓' : '✗';
                        const statusClass = fieldValid ? 'status-valid-icon' : 'status-invalid-icon';
                        const msg = fieldValid ? '' : valInfo[field].message;

                        return `
                            <div class="data-item">
                                <span class="label">${field}</span>
                                <span class="value">${displayVal}</span>
                                <span class="status-icon ${statusClass}">${statusIcon}</span>
                                <div class="error-msg">${msg}</div>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
            
            const recordDiv = document.createElement('div');
            recordDiv.innerHTML = gridHtml;
            recordsContainer.appendChild(recordDiv);
        });

        // Show Results
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
});
