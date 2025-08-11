# Installation Guide

## Quick Setup

1. **Clone and Install**
   ```bash
   git clone https://github.com/dstorey87/ats-cv-optimizer.git
   cd ats-cv-optimizer
   pip install -r requirements.txt
   ```

2. **Install Ollama**
   ```bash
   # On macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # On Windows
   # Download from https://ollama.ai/download/windows
   ```

3. **Install LLM Model**
   ```bash
   ollama pull deepseek-r1:8b
   ```

4. **Run Application**
   ```bash
   streamlit run app.py
   ```

## Features Overview

### 🎯 Dynamic Model Detection
- Automatically discovers available Ollama models
- No more hardcoded model lists
- Real-time connection testing

### 🎨 Modern Interface
- Professional dark/light theme support
- Responsive design for all devices
- Clean typography with Inter font
- Smooth animations and transitions

### 👀 Visual Comparisons
- Side-by-side before/after CV comparison
- Highlight additions, removals, and modifications
- Accept/reject individual changes
- Interactive change approval system

### 📚 Comprehensive Management
- **Job Descriptions**: Save, categorize, and reuse JDs from websites
- **CV Versions**: Track optimization history and performance
- **Settings**: Configure LLM preferences and system options

### 🛡️ Industry Standards
- 7-standard validation system
- Action verb hierarchy (Tier 1: Architected, Optimized, etc.)
- Quantification requirements (80% of bullets need metrics)
- ATS compatibility scoring

## Troubleshooting

### Ollama Not Found
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

### Port Already in Use
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### Missing Dependencies
```bash
# Install missing packages
pip install streamlit requests python-docx pandas
```