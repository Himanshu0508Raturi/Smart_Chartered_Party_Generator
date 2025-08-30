// Charter Party Document Automation - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeFileUploads();
    initializeFormValidation();
    initializeDragAndDrop();
});

function initializeFileUploads() {
    const baseCpFile = document.getElementById('baseCpFile');
    const recapFile = document.getElementById('recapFile');
    
    if (baseCpFile) {
        baseCpFile.addEventListener('change', function() {
            handleFileSelection(this, 'baseCpInfo', 'baseCpArea');
        });
    }
    
    if (recapFile) {
        recapFile.addEventListener('change', function() {
            handleFileSelection(this, 'recapInfo', 'recapArea');
        });
    }
}

function handleFileSelection(fileInput, infoId, areaId) {
    const file = fileInput.files[0];
    const fileInfo = document.getElementById(infoId);
    const uploadArea = document.getElementById(areaId);
    
    if (file) {
        // Show file info
        const fileName = fileInfo.querySelector('.file-name');
        fileName.textContent = `${file.name} (${formatFileSize(file.size)})`;
        fileInfo.style.display = 'block';
        
        // Update upload area appearance
        uploadArea.classList.add('has-file');
        
        // Validate file
        if (!validateFile(file, fileInput.accept)) {
            showError(`Invalid file type for ${file.name}. Please select a valid file.`);
            resetFileInput(fileInput, infoId, areaId);
            return;
        }
        
        // Check file size (16MB limit)
        if (file.size > 16 * 1024 * 1024) {
            showError(`File ${file.name} is too large. Maximum size is 16MB.`);
            resetFileInput(fileInput, infoId, areaId);
            return;
        }
        
        validateFormAndEnableSubmit();
    } else {
        resetFileInput(fileInput, infoId, areaId);
    }
}

function resetFileInput(fileInput, infoId, areaId) {
    const fileInfo = document.getElementById(infoId);
    const uploadArea = document.getElementById(areaId);
    
    fileInput.value = '';
    fileInfo.style.display = 'none';
    uploadArea.classList.remove('has-file');
    validateFormAndEnableSubmit();
}

function validateFile(file, acceptedTypes) {
    if (!acceptedTypes) return true;
    
    const types = acceptedTypes.split(',').map(type => type.trim().toLowerCase());
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    return types.includes(fileExtension);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function initializeFormValidation() {
    const form = document.getElementById('uploadForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                return false;
            }
            
            showProcessingIndicator();
        });
    }
}

function validateForm() {
    const baseCpFile = document.getElementById('baseCpFile');
    const recapFile = document.getElementById('recapFile');
    
    if (!baseCpFile.files.length) {
        showError('Please select a Base Charter Party file.');
        return false;
    }
    
    if (!recapFile.files.length) {
        showError('Please select a Fixture Recap file.');
        return false;
    }
    
    return true;
}

function validateFormAndEnableSubmit() {
    const baseCpFile = document.getElementById('baseCpFile');
    const recapFile = document.getElementById('recapFile');
    const processBtn = document.getElementById('processBtn');
    
    if (processBtn) {
        const isValid = baseCpFile.files.length > 0 && recapFile.files.length > 0;
        processBtn.disabled = !isValid;
    }
}

function initializeDragAndDrop() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        area.addEventListener('dragover', handleDragOver);
        area.addEventListener('dragenter', handleDragEnter);
        area.addEventListener('dragleave', handleDragLeave);
        area.addEventListener('drop', handleDrop);
    });
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDragEnter(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const fileInput = this.querySelector('input[type="file"]');
        if (fileInput) {
            // Create a new FileList with the dropped file
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(files[0]);
            fileInput.files = dataTransfer.files;
            
            // Trigger change event
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }
}

function showProcessingIndicator() {
    const indicator = document.getElementById('processingIndicator');
    const processBtn = document.getElementById('processBtn');
    
    if (indicator) {
        indicator.style.display = 'block';
    }
    
    if (processBtn) {
        processBtn.disabled = true;
        processBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    }
}

function showError(message) {
    // Create and show error alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function showSuccess(message) {
    // Create and show success alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 3000);
}

// Utility functions for results page
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Content copied to clipboard!');
    }).catch(err => {
        showError('Failed to copy content to clipboard.');
    });
}

function exportChanges() {
    if (typeof changes !== 'undefined' && changes.length > 0) {
        const csvContent = generateCSV(changes);
        downloadCSV(csvContent, 'charter_party_changes.csv');
    } else {
        showError('No changes available to export.');
    }
}

function generateCSV(data) {
    const headers = ['Field', 'Change Type', 'Description', 'Old Value', 'New Value', 'Timestamp'];
    const csvRows = [headers.join(',')];
    
    data.forEach(change => {
        const row = [
            `"${change.field.replace(/"/g, '""')}"`,
            `"${change.change_type}"`,
            `"${change.description.replace(/"/g, '""')}"`,
            `"${(change.old_value || '').replace(/"/g, '""')}"`,
            `"${(change.new_value || '').replace(/"/g, '""')}"`,
            `"${change.timestamp}"`
        ];
        csvRows.push(row.join(','));
    });
    
    return csvRows.join('\n');
}

function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}
