import os
import logging
from flask import Flask, request, render_template, flash, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
from document_processor import DocumentProcessor
from change_tracker import ChangeTracker
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-key-change-in-production")

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and process documents"""
    try:
        # Check if both files are present
        if 'base_cp' not in request.files or 'recap' not in request.files:
            flash('Both Base CP and Recap files are required', 'error')
            return redirect(url_for('index'))
        
        base_cp_file = request.files['base_cp']
        recap_file = request.files['recap']
        
        # Check if files are selected
        if base_cp_file.filename == '' or recap_file.filename == '':
            flash('Please select both files', 'error')
            return redirect(url_for('index'))
        
        # Check file extensions
        if not (allowed_file(base_cp_file.filename) and allowed_file(recap_file.filename)):
            flash('Only PDF and DOCX files are allowed', 'error')
            return redirect(url_for('index'))
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Save uploaded files
        base_cp_filename = secure_filename(f"{session_id}_base_cp_{base_cp_file.filename}")
        recap_filename = secure_filename(f"{session_id}_recap_{recap_file.filename}")
        
        base_cp_path = os.path.join(app.config['UPLOAD_FOLDER'], base_cp_filename)
        recap_path = os.path.join(app.config['UPLOAD_FOLDER'], recap_filename)
        
        base_cp_file.save(base_cp_path)
        recap_file.save(recap_path)
        
        # Process documents
        processor = DocumentProcessor()
        change_tracker = ChangeTracker()
        
        # Extract text from documents
        base_cp_text = processor.extract_text_from_file(base_cp_path)
        recap_data = processor.extract_recap_data(recap_path)
        
        # Merge documents and track changes
        merged_document, changes = processor.merge_documents(base_cp_text, recap_data, change_tracker)
        
        # Generate output files
        output_docx_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{session_id}_merged_cp.docx")
        output_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{session_id}_merged_cp.pdf")
        
        processor.generate_docx(merged_document, output_docx_path)
        processor.generate_pdf(merged_document, output_pdf_path)
        
        # Generate change summary
        change_summary = change_tracker.generate_summary(changes)
        
        # Clean up uploaded files
        os.remove(base_cp_path)
        os.remove(recap_path)
        
        return render_template('results.html', 
                             session_id=session_id,
                             changes=changes,
                             change_summary=change_summary,
                             merged_content=merged_document[:2000] + "..." if len(merged_document) > 2000 else merged_document)
        
    except Exception as e:
        logging.error(f"Error processing documents: {str(e)}")
        flash(f'Error processing documents: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<session_id>/<file_type>')
def download_file(session_id, file_type):
    """Download generated document"""
    try:
        if file_type == 'docx':
            filename = f"{session_id}_merged_cp.docx"
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif file_type == 'pdf':
            filename = f"{session_id}_merged_cp.pdf"
            mimetype = 'application/pdf'
        else:
            flash('Invalid file type', 'error')
            return redirect(url_for('index'))
        
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            flash('File not found', 'error')
            return redirect(url_for('index'))
        
        return send_file(file_path, 
                        as_attachment=True, 
                        download_name=f"charter_party_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_type}",
                        mimetype=mimetype)
        
    except Exception as e:
        logging.error(f"Error downloading file: {str(e)}")
        flash('Error downloading file', 'error')
        return redirect(url_for('index'))

@app.route('/preview/<session_id>')
def preview_document(session_id):
    """Preview the merged document"""
    try:
        filename = f"{session_id}_merged_cp.docx"
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        processor = DocumentProcessor()
        preview_text = processor.extract_text_from_file(file_path)
        
        return jsonify({'content': preview_text})
        
    except Exception as e:
        logging.error(f"Error previewing document: {str(e)}")
        return jsonify({'error': 'Error previewing document'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
