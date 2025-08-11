# ATS CV Optimizer

A professional CV optimization tool that helps create ATS-friendly resumes with intelligent scanning and enhancement capabilities.

## Features

- **ATS Scanning**: Analyze CVs against job descriptions for keyword matching
- **CV Enhancement**: Intelligent suggestions for improvement
- **Job Description Management**: Store and manage job postings
- **Progress Tracking**: Monitor optimization iterations
- **Multiple Interfaces**: CLI, web interface, and API support

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run CLI Scanner**
   ```bash
   python cli.py --cv "path/to/cv.docx" --jd "path/to/job.txt"
   ```

3. **Launch Web Interface**
   ```bash
   streamlit run streamlit_app.py
   ```

## Project Structure

- `ats_app/` - Core application modules
- `CVs/` - CV storage and versions
- `JD/` - Job description storage
- `Scans/` - Scan results and reports
- `cli.py` - Command line interface
- `streamlit_app.py` - Web interface

## Configuration

The application uses Ollama for LLM integration. Ensure Ollama is running:
```bash
ollama serve
```

## License

MIT License