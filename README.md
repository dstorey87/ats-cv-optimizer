# 🚀 ATS CV Optimizer

## Advanced AI-Powered CV Optimization with Visual Feedback

**Transform your CV into an ATS-friendly powerhouse with LLM-powered optimization, comprehensive industry governance, and intuitive visual comparisons.**

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.36.0-red.svg)

## ✨ Key Features

- **🎯 AI-Powered Optimization**: Local LLM integration via Ollama with dynamic model detection
- **🛡️ Industry Governance**: 7 comprehensive standards based on Fortune 500 hiring practices
- **👀 Visual Comparisons**: Side-by-side before/after views with change approval system
- **📱 Multi-Modal Interface**: Web, desktop, and CLI interfaces for different workflows
- **📊 CV Version Control**: Track optimization history and performance metrics
- **💾 Job Description Management**: Save, categorize, and reuse JDs from websites

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed and running locally
- At least one LLM model in Ollama (recommended: `deepseek-r1:8b`)

### Installation

```bash
# Clone the repository
git clone https://github.com/dstorey87/ats-cv-optimizer.git
cd ats-cv-optimizer

# Install dependencies
pip install -r requirements.txt

# Install Ollama model (if not already installed)
ollama pull deepseek-r1:8b

# Start the web interface
streamlit run app.py
```

### 🌐 Web Interface
Access the modern multi-page interface at `http://localhost:8501`:
- **Home Dashboard**: Overview and quick statistics
- **CV Optimizer**: Main optimization workflow with visual comparisons
- **Job Descriptions**: Comprehensive JD management and storage
- **CV Library**: Version control and performance tracking
- **Settings**: LLM configuration and system preferences

## 🏗️ Architecture

```
ats-cv-optimizer/
├── app.py                      # Main Streamlit interface
├── ats_app/                    # Core optimization engine
│   ├── cv_optimizer_enhanced.py   # LLM-powered optimizer
│   ├── industry_standards.py      # Governance rules
│   ├── visual_cv_optimizer.py     # Change tracking
│   └── utils.py                   # Utilities
├── data/                       # Local storage
│   ├── cvs/                   # CV versions
│   └── job_descriptions/      # Saved JDs
└── requirements.txt           # Dependencies
```

## 🎨 Modern Interface

The enhanced interface features:
- **Clean, professional design** with Inter font and modern color scheme
- **Responsive layout** that works on desktop and mobile
- **Visual diff engine** showing exact changes with syntax highlighting
- **Interactive change approval** - accept or reject individual modifications
- **Real-time statistics** and performance metrics
- **Dynamic model detection** - automatically discovers available Ollama models

## 🔧 Industry Standards

### Action Verb Hierarchy
- **Tier 1 (Mandatory)**: Architected, Optimized, Automated, Spearheaded
- **Tier 2 (Preferred)**: Developed, Managed, Led, Implemented
- **Tier 3 (Acceptable)**: Configured, Maintained, Monitored
- **Forbidden**: "Responsible for", "Worked on", "Helped with"

### Quantification Requirements
- 80% of bullet points must include metrics
- Specific numbers over ranges ($50K vs $45K-$55K)
- Multiple metric types: percentages, dollars, time, volume

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

---

**⭐ Star this repository if you find it helpful!**