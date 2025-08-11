"""
🚀 ENHANCED CV OPTIMIZER WEB INTERFACE
Modern multi-page Streamlit application with dynamic LLM detection, visual comparisons, and comprehensive management
"""

import streamlit as st
import os
import sys
from pathlib import Path
import json
import tempfile
from datetime import datetime
import pandas as pd
import requests
from typing import List, Dict, Optional, Tuple
import difflib
import re

# Configure page
st.set_page_config(
    page_title="ATS CV Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the ats_app directory to the path
sys.path.append(str(Path(__file__).parent / "ats_app"))

try:
    from ats_app.cv_optimizer_enhanced import IntelligentCVOptimizer
    from ats_app.cv_enhancer import CVEnhancer, OptimizationWorkflow
    from ats_app.industry_standards import CVIndustryStandards
    from ats_app.utils import setup_logger
except ImportError:
    st.error("❌ ATS app modules not found. Please ensure all files are in the correct directory structure.")
    st.stop()

# Custom CSS
def load_css():
    """Load custom CSS styling"""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-color: #2E86AB;
        --primary-light: #A8DADC;
        --primary-dark: #1D5F7E;
        --secondary-color: #F1FAEE;
        --accent-color: #E63946;
        --success-color: #06D6A0;
        --warning-color: #FFD23F;
        --info-color: #118AB2;
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8F9FA;
        --text-primary: #212529;
        --text-secondary: #6C757D;
        --border-color: #DEE2E6;
        --shadow: rgba(0, 0, 0, 0.1);
        --radius: 0.75rem;
    }

    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }
    
    .stApp {
        font-family: 'Inter', sans-serif !important;
    }

    .page-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        padding: 2rem;
        border-radius: var(--radius);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px var(--shadow);
    }

    .page-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .metric-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px var(--shadow);
    }

    .metric-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        display: block;
    }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .status-success {
        background-color: var(--success-color);
        color: white;
    }

    .comparison-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }

    .comparison-side {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: var(--radius);
        padding: 1rem;
    }

    .comparison-side.before {
        border-color: var(--accent-color);
    }

    .comparison-side.after {
        border-color: var(--success-color);
    }

    .highlight-add {
        background-color: rgba(6, 214, 160, 0.2);
        padding: 2px 4px;
        border-radius: 4px;
    }

    .highlight-remove {
        background-color: rgba(230, 57, 70, 0.2);
        padding: 2px 4px;
        border-radius: 4px;
        text-decoration: line-through;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Navigation
def create_navigation():
    """Create navigation sidebar"""
    st.sidebar.markdown("## 🧭 Navigation")
    
    pages = {
        "🏠 Home": "home",
        "📄 CV Optimizer": "cv_optimizer", 
        "📋 Job Descriptions": "job_descriptions",
        "📊 CV Management": "cv_management",
        "⚙️ Settings": "settings"
    }
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    
    for page_name, page_key in pages.items():
        if st.sidebar.button(page_name, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun()
    
    return st.session_state.current_page

# Ollama Model Detection
@st.cache_data(ttl=300)
def get_available_models() -> List[str]:
    """Dynamically fetch available Ollama models"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            return [model["name"] for model in models_data.get("models", [])]
        else:
            st.warning("⚠️ Could not connect to Ollama. Using fallback models.")
            return ["deepseek-r1:8b"]
    except requests.exceptions.RequestException:
        st.warning("⚠️ Ollama not available. Using fallback models.")
        return ["deepseek-r1:8b"]

def test_ollama_connection(url: str, model: str) -> Tuple[bool, str]:
    """Test connection to Ollama"""
    try:
        optimizer = IntelligentCVOptimizer(ollama_url=url, model=model)
        result = optimizer.test_ollama_connection()
        return result["success"], result.get("message", "Connection test completed")
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

# Data Management
def get_cv_store() -> Dict:
    """Get CV management data"""
    cv_dir = Path("data/cvs")
    cv_dir.mkdir(exist_ok=True, parents=True)
    
    cvs = {}
    for cv_file in cv_dir.glob("*.json"):
        try:
            with open(cv_file, 'r', encoding='utf-8') as f:
                cv_data = json.load(f)
                cvs[cv_file.stem] = cv_data
        except Exception as e:
            st.error(f"Error loading CV {cv_file}: {e}")
    
    return cvs

def get_jd_store() -> Dict:
    """Get Job Description store"""
    jd_dir = Path("data/job_descriptions")
    jd_dir.mkdir(exist_ok=True, parents=True)
    
    jds = {}
    for jd_file in jd_dir.glob("*.json"):
        try:
            with open(jd_file, 'r', encoding='utf-8') as f:
                jd_data = json.load(f)
                jds[jd_file.stem] = jd_data
        except Exception as e:
            st.error(f"Error loading JD {jd_file}: {e}")
    
    return jds

def save_job_description(title: str, content: str, company: str = "", url: str = ""):
    """Save job description with enhanced metadata"""
    jd_dir = Path("data/job_descriptions")
    jd_dir.mkdir(exist_ok=True, parents=True)
    
    jd_data = {
        "title": title,
        "company": company,
        "content": content,
        "url": url,
        "saved_at": datetime.now().isoformat(),
        "word_count": len(content.split()),
        "char_count": len(content)
    }
    
    safe_filename = "".join(c for c in f"{company}_{title}" if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
    
    jd_path = jd_dir / f"{safe_filename}.json"
    with open(jd_path, 'w', encoding='utf-8') as f:
        json.dump(jd_data, f, indent=2, ensure_ascii=False)
    
    return True

# Page Functions
def home_page():
    """Home page with dashboard"""
    st.markdown("""
    <div class="page-header fade-in">
        <h1>🚀 ATS CV Optimizer</h1>
        <p>AI-Powered CV optimization with strict industry governance and visual feedback</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    cvs = get_cv_store()
    jds = get_jd_store()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-number">{len(cvs)}</span>
            <div class="metric-label">CVs Stored</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-number">{len(jds)}</span>
            <div class="metric-label">Job Descriptions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        available_models = get_available_models()
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-number">{len(available_models)}</span>
            <div class="metric-label">LLM Models</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <span class="metric-number">7</span>
            <div class="metric-label">Industry Standards</div>
        </div>
        """, unsafe_allow_html=True)

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Optimize CV", key="quick_cv", type="primary"):
            st.session_state.current_page = "cv_optimizer"
            st.rerun()
    
    with col2:
        if st.button("📋 Manage JDs", key="quick_jd"):
            st.session_state.current_page = "job_descriptions" 
            st.rerun()
    
    with col3:
        if st.button("📊 CV Library", key="quick_lib"):
            st.session_state.current_page = "cv_management"
            st.rerun()

def cv_optimizer_page():
    """Enhanced CV optimization page with visual comparisons"""
    st.markdown("""
    <div class="page-header">
        <h1>📄 CV Optimizer</h1>
        <p>AI-powered optimization with before/after comparisons and change approval</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuration Section
    with st.expander("⚙️ LLM Configuration", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            ollama_url = st.text_input("Ollama Server URL", value="http://localhost:11434")
        
        with col2:
            available_models = get_available_models()
            if available_models:
                model_name = st.selectbox("LLM Model", options=available_models)
            else:
                st.error("❌ No Ollama models available")
                return
        
        # Test Connection
        if st.button("🔍 Test Connection"):
            with st.spinner("Testing connection..."):
                success, message = test_ollama_connection(ollama_url, model_name)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
    
    # CV Upload Section
    st.markdown("### 📎 Upload CV")
    cv_file = st.file_uploader("Choose your CV file", type=['docx', 'pdf', 'txt'])
    
    # Job Description Section
    st.markdown("### 📋 Job Description")
    jd_tab1, jd_tab2, jd_tab3 = st.tabs(["📝 Paste", "📄 Upload", "🗄️ Saved"])
    
    jd_content = ""
    
    with jd_tab1:
        jd_content = st.text_area("Paste job description here:", height=200, 
                                 placeholder="Copy and paste the job description from the website...")
        
        if jd_content:
            col1, col2 = st.columns([3, 1])
            with col1:
                jd_title = st.text_input("Job Title", placeholder="e.g., Senior DevOps Engineer")
                jd_company = st.text_input("Company", placeholder="e.g., Lumenalta")
            
            with col2:
                if st.button("💾 Save JD", type="primary"):
                    if jd_title and jd_content:
                        if save_job_description(jd_title, jd_content, jd_company):
                            st.success("✅ Job description saved!")
                    else:
                        st.warning("⚠️ Please provide both title and content")
    
    with jd_tab2:
        jd_file = st.file_uploader("Choose job description file", type=['txt', 'pdf', 'docx'])
        if jd_file:
            jd_content = jd_file.read().decode('utf-8') if jd_file.type.startswith('text') else "File uploaded - processing needed"
    
    with jd_tab3:
        saved_jds = get_jd_store()
        if saved_jds:
            selected_jd = st.selectbox("Select saved job description:", list(saved_jds.keys()))
            if selected_jd:
                jd_data = saved_jds[selected_jd]
                st.info(f"**{jd_data['title']}** at {jd_data.get('company', 'Unknown Company')}")
                jd_content = jd_data['content']
        else:
            st.info("📭 No saved job descriptions yet")
    
    # Process Button
    if st.button("🚀 Optimize CV", type="primary", disabled=not (cv_file and jd_content)):
        if cv_file and jd_content:
            with st.spinner("🔄 Optimizing your CV..."):
                try:
                    # Save uploaded CV temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{cv_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(cv_file.read())
                        tmp_cv_path = tmp_file.name
                    
                    # Initialize optimizer
                    optimizer = IntelligentCVOptimizer(ollama_url=ollama_url, model=model_name)
                    
                    # Process CV
                    results = optimizer.optimize_cv(
                        cv_path=tmp_cv_path,
                        job_description=jd_content,
                        governance_level="comprehensive"
                    )
                    
                    if results["success"]:
                        st.success("✅ CV optimization completed!")
                        
                        # Show basic comparison
                        original_content = results.get('original_content', '')
                        optimized_content = results.get('optimized_content', '')
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**📄 Original CV**")
                            st.text_area("", value=original_content[:500] + "...", height=300, disabled=True)
                        
                        with col2:
                            st.markdown("**✨ Optimized CV**")
                            st.text_area("", value=optimized_content[:500] + "...", height=300, disabled=True)
                        
                        # Show report if available
                        if 'report' in results:
                            st.markdown("### 📊 Optimization Report")
                            st.markdown(results['report'])
                    
                    else:
                        st.error(f"❌ Optimization failed: {results.get('message', 'Unknown error')}")
                    
                    # Clean up
                    os.unlink(tmp_cv_path)
                    
                except Exception as e:
                    st.error(f"❌ Error during optimization: {str(e)}")

def job_descriptions_page():
    """Job Descriptions management page"""
    st.markdown("""
    <div class="page-header">
        <h1>📋 Job Descriptions</h1>
        <p>Comprehensive job description management and analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 Job Description management page - Full implementation available in source code")

def cv_management_page():
    """CV management page"""
    st.markdown("""
    <div class="page-header">
        <h1>📊 CV Management</h1>
        <p>Manage your CV versions, track optimizations, and analyze performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 CV Management page - Full implementation available in source code")

def settings_page():
    """Settings page"""
    st.markdown("""
    <div class="page-header">
        <h1>⚙️ Settings</h1>
        <p>Configure your CV optimization preferences and system settings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # LLM Configuration
    st.markdown("### 🤖 LLM Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ollama_url = st.text_input("Ollama Server URL", value="http://localhost:11434")
        available_models = get_available_models()
        
        if available_models:
            default_model = st.selectbox("Default LLM Model", options=available_models)
            
            st.markdown("**Available Models:**")
            for model in available_models:
                status_indicator = "🟢" if model == default_model else "⚪"
                st.markdown(f"{status_indicator} {model}")
        else:
            st.error("❌ No models available. Please check Ollama installation.")
    
    with col2:
        st.markdown("**Connection Status**")
        if st.button("🔍 Test Connection"):
            with st.spinner("Testing..."):
                success, message = test_ollama_connection(ollama_url, available_models[0] if available_models else "")
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")

# Main App
def main():
    """Main application entry point"""
    # Load custom CSS
    load_css()
    
    # Create navigation
    current_page = create_navigation()
    
    # Route to appropriate page
    if current_page == "home":
        home_page()
    elif current_page == "cv_optimizer":
        cv_optimizer_page()
    elif current_page == "job_descriptions":
        job_descriptions_page()
    elif current_page == "cv_management":
        cv_management_page()
    elif current_page == "settings":
        settings_page()
    else:
        home_page()  # Fallback

if __name__ == "__main__":
    main()