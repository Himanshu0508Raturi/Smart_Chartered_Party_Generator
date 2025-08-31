# Charter Party Document Automation

## Overview

This is a Flask-based web application that automates the merging of Charter Party documents with fixture recaps. The system processes PDF and DOCX files, extracts text content, tracks changes during the merging process, and generates merged documents. It's designed for maritime industry professionals who need to efficiently combine charter party templates with fixture recap information.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask for server-side rendering
- **UI Framework**: Bootstrap with dark theme for responsive design
- **Client-side Features**: JavaScript for file upload handling, drag-and-drop functionality, and form validation
- **File Upload**: Multi-file upload interface supporting PDF and DOCX formats with size validation (16MB limit)

### Backend Architecture
- **Web Framework**: Flask application with modular design
- **Document Processing**: Dedicated `DocumentProcessor` class for text extraction from PDF (using pdfplumber) and DOCX (using python-docx) files
- **Change Tracking**: `ChangeTracker` class that monitors and logs all modifications during document merging
- **File Management**: Organized upload and output directories with secure filename handling
- **Session Management**: Flask sessions with configurable secret key

### Core Components
- **Document Processor**: Handles text extraction from multiple file formats and document generation
- **Change Tracker**: Provides detailed diff analysis and change summarization
- **File Validation**: Ensures uploaded files meet format and size requirements
- **Error Handling**: Comprehensive logging and user feedback system

### Data Flow
1. Users upload base charter party and recap documents
2. System validates file formats and sizes
3. Text extraction occurs for both documents
4. Change tracking monitors the merging process
5. Final merged document is generated and made available for download

## External Dependencies

### Python Libraries
- **Flask**: Web framework for HTTP handling and routing
- **pdfplumber**: PDF text extraction and processing
- **python-docx**: DOCX document reading and writing
- **reportlab**: PDF generation for output documents
- **werkzeug**: Secure filename handling and file utilities

### Frontend Dependencies
- **Bootstrap**: CSS framework for responsive UI design
- **Font Awesome**: Icon library for enhanced visual elements
- **Bootstrap Agent Dark Theme**: Custom dark theme for improved user experience

### File System Dependencies
- **Upload Directory**: Temporary storage for uploaded documents
- **Output Directory**: Storage for generated merged documents
- **Static Assets**: CSS and JavaScript files for frontend functionality

### Environment Configuration
- **Session Secret**: Configurable secret key for Flask sessions
- **File Size Limits**: 16MB maximum file size restriction
- **Allowed Extensions**: PDF, DOCX, and DOC file format support