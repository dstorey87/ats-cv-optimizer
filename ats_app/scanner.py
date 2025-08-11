"""ATS Scanner Module - Comprehensive CV Analysis"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import re

logger = logging.getLogger(__name__)

class ATSScanner:
    """Main scanner for ATS compatibility analysis"""
    
    def __init__(self):
        self.ats_keywords = {
            'power_verbs': [
                'achieved', 'analyzed', 'architected', 'automated', 'built', 'collaborated',
                'created', 'delivered', 'designed', 'developed', 'enhanced', 'executed',
                'implemented', 'improved', 'increased', 'led', 'managed', 'optimized',
                'orchestrated', 'produced', 'reduced', 'resolved', 'spearheaded', 'streamlined'
            ],
            'technical_skills': [
                'python', 'java', 'javascript', 'docker', 'kubernetes', 'aws', 'azure',
                'devops', 'ci/cd', 'jenkins', 'git', 'linux', 'sql', 'nosql', 'mongodb',
                'postgresql', 'redis', 'elasticsearch', 'kafka', 'microservices', 'api',
                'rest', 'graphql', 'terraform', 'ansible', 'prometheus', 'grafana'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem-solving', 'analytical',
                'critical thinking', 'adaptability', 'mentoring', 'collaboration',
                'project management', 'stakeholder management', 'cross-functional'
            ]
        }
        
    def scan_cv(self, cv_path: Path, job_description: str = "") -> Dict[str, Any]:
        """Perform comprehensive ATS scan of CV"""
        try:
            # Extract text from CV
            cv_text = self._extract_text(cv_path)
            
            # Perform analysis
            results = {
                'timestamp': datetime.now().isoformat(),
                'cv_path': str(cv_path),
                'overall_score': 0,
                'sections': {
                    'keywords': self._analyze_keywords(cv_text, job_description),
                    'formatting': self._analyze_formatting(cv_text),
                    'content_quality': self._analyze_content_quality(cv_text),
                    'ats_compatibility': self._analyze_ats_compatibility(cv_text),
                    'quantification': self._analyze_quantification(cv_text)
                },
                'recommendations': []
            }
            
            # Calculate overall score
            results['overall_score'] = self._calculate_overall_score(results['sections'])
            
            # Generate recommendations
            results['recommendations'] = self._generate_recommendations(results['sections'])
            
            return results
            
        except Exception as e:
            logger.error(f"Error scanning CV: {e}")
            return {'error': str(e)}
    
    def _extract_text(self, cv_path: Path) -> str:
        """Extract text from CV file"""
        try:
            if cv_path.suffix.lower() == '.docx':
                from docx import Document
                doc = Document(cv_path)
                return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            elif cv_path.suffix.lower() == '.pdf':
                # PDF extraction would go here
                logger.warning("PDF extraction not yet implemented")
                return ""
            else:
                with open(cv_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"Error extracting text from {cv_path}: {e}")
            return ""
    
    def _analyze_keywords(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze keyword presence and density"""
        cv_lower = cv_text.lower()
        jd_lower = job_description.lower()
        
        # Count power verbs
        power_verb_count = sum(1 for verb in self.ats_keywords['power_verbs'] 
                              if verb in cv_lower)
        
        # Count technical skills
        tech_skills_found = [skill for skill in self.ats_keywords['technical_skills'] 
                           if skill in cv_lower]
        
        # Count soft skills
        soft_skills_found = [skill for skill in self.ats_keywords['soft_skills'] 
                           if skill in cv_lower]
        
        # Job description matching (if provided)
        jd_match_score = 0
        if job_description:
            jd_keywords = self._extract_jd_keywords(job_description)
            matched_keywords = [kw for kw in jd_keywords if kw in cv_lower]
            jd_match_score = len(matched_keywords) / max(len(jd_keywords), 1) * 100
        
        return {
            'power_verbs': {
                'count': power_verb_count,
                'score': min(power_verb_count * 10, 100)
            },
            'technical_skills': {
                'found': tech_skills_found,
                'count': len(tech_skills_found),
                'score': min(len(tech_skills_found) * 5, 100)
            },
            'soft_skills': {
                'found': soft_skills_found,
                'count': len(soft_skills_found),
                'score': min(len(soft_skills_found) * 10, 100)
            },
            'job_match': {
                'score': jd_match_score,
                'matched_count': len(matched_keywords) if job_description else 0
            }
        }
    
    def _analyze_formatting(self, cv_text: str) -> Dict[str, Any]:
        """Analyze CV formatting for ATS compatibility"""
        lines = cv_text.split('\n')
        
        # Check for common sections
        sections_found = {
            'contact': bool(re.search(r'(email|phone|linkedin)', cv_text, re.I)),
            'summary': bool(re.search(r'(summary|profile|objective)', cv_text, re.I)),
            'experience': bool(re.search(r'(experience|work|employment)', cv_text, re.I)),
            'education': bool(re.search(r'education', cv_text, re.I)),
            'skills': bool(re.search(r'skills', cv_text, re.I))
        }
        
        # Calculate formatting score
        section_score = sum(sections_found.values()) / len(sections_found) * 100
        
        # Check for bullet points
        bullet_count = sum(1 for line in lines if line.strip().startswith(('•', '-', '*')))
        bullet_score = min(bullet_count * 5, 100)
        
        return {
            'sections': sections_found,
            'section_score': section_score,
            'bullet_points': bullet_count,
            'bullet_score': bullet_score,
            'overall_formatting_score': (section_score + bullet_score) / 2
        }
    
    def _analyze_content_quality(self, cv_text: str) -> Dict[str, Any]:
        """Analyze content quality metrics"""
        words = cv_text.split()
        sentences = re.split(r'[.!?]+', cv_text)
        
        # Basic metrics
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        
        # Quality indicators
        bullet_points = len(re.findall(r'^\s*[•\-\*]', cv_text, re.MULTILINE))
        quantified_achievements = len(re.findall(r'\d+[%$]?|\$\d+', cv_text))
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': avg_words_per_sentence,
            'bullet_points': bullet_points,
            'quantified_achievements': quantified_achievements,
            'quality_score': min((bullet_points * 5) + (quantified_achievements * 10), 100)
        }
    
    def _analyze_ats_compatibility(self, cv_text: str) -> Dict[str, Any]:
        """Analyze ATS compatibility factors"""
        compatibility_issues = []
        score = 100
        
        # Check for problematic formatting
        if '\t' in cv_text:
            compatibility_issues.append('Contains tab characters')
            score -= 10
        
        # Check for excessive special characters
        special_char_count = len(re.findall(r'[^\w\s\-.,!?()%$]', cv_text))
        if special_char_count > 50:
            compatibility_issues.append('Excessive special characters')
            score -= 15
        
        # Check for proper contact info formatting
        email_found = bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', cv_text))
        phone_found = bool(re.search(r'\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}', cv_text))
        
        if not email_found:
            compatibility_issues.append('No email address found')
            score -= 20
        
        if not phone_found:
            compatibility_issues.append('No phone number found')
            score -= 10
        
        return {
            'score': max(score, 0),
            'issues': compatibility_issues,
            'contact_info': {
                'email_found': email_found,
                'phone_found': phone_found
            }
        }
    
    def _analyze_quantification(self, cv_text: str) -> Dict[str, Any]:
        """Analyze quantification in achievements"""
        # Find all bullet points
        bullet_lines = re.findall(r'^\s*[•\-\*].*$', cv_text, re.MULTILINE)
        
        # Count quantified bullets
        quantified_bullets = []
        for bullet in bullet_lines:
            if re.search(r'\d+[%$]?|\$\d+|\d+\+|\d+x|\d+ years?', bullet, re.I):
                quantified_bullets.append(bullet.strip())
        
        total_bullets = len(bullet_lines)
        quantified_count = len(quantified_bullets)
        quantification_rate = (quantified_count / max(total_bullets, 1)) * 100
        
        return {
            'total_bullets': total_bullets,
            'quantified_bullets': quantified_count,
            'quantification_rate': quantification_rate,
            'quantified_examples': quantified_bullets[:5],  # First 5 examples
            'score': quantification_rate
        }
    
    def _extract_jd_keywords(self, job_description: str) -> List[str]:
        """Extract keywords from job description"""
        # Simple keyword extraction - could be enhanced with NLP
        jd_lower = job_description.lower()
        
        # Common technical terms and skills
        all_keywords = (self.ats_keywords['technical_skills'] + 
                       self.ats_keywords['soft_skills'])
        
        # Add job-specific terms
        job_terms = re.findall(r'\b[a-z]{3,}\b', jd_lower)
        technical_terms = [term for term in job_terms 
                          if term in ['python', 'java', 'docker', 'aws', 'kubernetes']]
        
        return list(set(all_keywords + technical_terms))
    
    def _calculate_overall_score(self, sections: Dict[str, Any]) -> int:
        """Calculate overall ATS score"""
        scores = []
        
        # Keyword analysis (30%)
        keyword_score = (sections['keywords']['power_verbs']['score'] * 0.3 +
                        sections['keywords']['technical_skills']['score'] * 0.4 +
                        sections['keywords']['soft_skills']['score'] * 0.2 +
                        sections['keywords']['job_match']['score'] * 0.1)
        scores.append(keyword_score * 0.3)
        
        # Formatting (25%)
        scores.append(sections['formatting']['overall_formatting_score'] * 0.25)
        
        # Content quality (20%)
        scores.append(sections['content_quality']['quality_score'] * 0.2)
        
        # ATS compatibility (15%)
        scores.append(sections['ats_compatibility']['score'] * 0.15)
        
        # Quantification (10%)
        scores.append(sections['quantification']['score'] * 0.1)
        
        return int(sum(scores))
    
    def _generate_recommendations(self, sections: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Keyword recommendations
        if sections['keywords']['power_verbs']['count'] < 5:
            recommendations.append("Add more power verbs to strengthen impact statements")
        
        if sections['keywords']['technical_skills']['count'] < 8:
            recommendations.append("Include more relevant technical skills from your experience")
        
        # Formatting recommendations
        if not sections['formatting']['sections']['summary']:
            recommendations.append("Add a professional summary or objective section")
        
        if sections['formatting']['bullet_points'] < 10:
            recommendations.append("Use more bullet points to improve readability")
        
        # Content quality recommendations
        if sections['content_quality']['quantified_achievements'] < 5:
            recommendations.append("Add more quantified achievements with specific numbers and results")
        
        # ATS compatibility
        for issue in sections['ats_compatibility']['issues']:
            recommendations.append(f"Fix ATS issue: {issue}")
        
        # Quantification
        if sections['quantification']['quantification_rate'] < 60:
            recommendations.append("Quantify more of your achievements with specific metrics and numbers")
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def save_results(self, results: Dict[str, Any], output_path: Path) -> bool:
        """Save scan results to file"""
        try:
            # Save detailed results as JSON
            import json
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w') as f:
                json.dump(results, f, indent=2)
            
            # Save summary as CSV
            csv_path = output_path.with_suffix('.csv')
            summary_data = {
                'Metric': [],
                'Score': [],
                'Details': []
            }
            
            # Add overall score
            summary_data['Metric'].append('Overall ATS Score')
            summary_data['Score'].append(results['overall_score'])
            summary_data['Details'].append(f"{results['overall_score']}/100")
            
            # Add section scores
            for section_name, section_data in results['sections'].items():
                if isinstance(section_data, dict) and 'score' in section_data:
                    summary_data['Metric'].append(section_name.replace('_', ' ').title())
                    summary_data['Score'].append(section_data['score'])
                    summary_data['Details'].append(f"{section_data['score']}/100")
            
            df = pd.DataFrame(summary_data)
            df.to_csv(csv_path, index=False)
            
            logger.info(f"Results saved to {json_path} and {csv_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return False
