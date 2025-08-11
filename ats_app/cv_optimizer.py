"""CV Optimizer - Main optimization engine"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import json
import requests
from .industry_standards import IndustryStandards

logger = logging.getLogger(__name__)

class CVOptimizer:
    """Main CV optimization engine with LLM integration"""
    
    def __init__(self, llm_config: Optional[Dict] = None):
        self.industry_standards = IndustryStandards()
        self.llm_config = llm_config or {
            'provider': 'ollama',
            'model': 'deepseek-r1:8b',
            'base_url': 'http://localhost:11434'
        }
        
    def optimize_cv(self, cv_text: str, job_description: str = "", 
                   optimization_level: str = "balanced") -> Dict[str, Any]:
        """Optimize CV content using LLM analysis"""
        try:
            # Prepare optimization context
            context = self._prepare_optimization_context(
                cv_text, job_description, optimization_level
            )
            
            # Generate optimized content
            optimization_result = self._generate_optimizations(context)
            
            # Validate improvements
            validation_result = self._validate_improvements(
                cv_text, optimization_result['optimized_content']
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'original_content': cv_text,
                'optimized_content': optimization_result['optimized_content'],
                'improvements': optimization_result['improvements'],
                'validation': validation_result,
                'optimization_level': optimization_level,
                'job_description': job_description,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"CV optimization failed: {e}")
            return {
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def _prepare_optimization_context(self, cv_text: str, job_description: str, 
                                    optimization_level: str) -> Dict[str, Any]:
        """Prepare context for LLM optimization"""
        # Get industry standards
        standards = self.industry_standards.get_all_standards()
        
        # Analyze current CV
        current_analysis = self._analyze_current_cv(cv_text)
        
        # Extract job requirements if provided
        job_requirements = self._extract_job_requirements(job_description) if job_description else {}
        
        return {
            'cv_text': cv_text,
            'job_description': job_description,
            'job_requirements': job_requirements,
            'optimization_level': optimization_level,
            'industry_standards': standards,
            'current_analysis': current_analysis,
            'optimization_guidelines': self._get_optimization_guidelines(optimization_level)
        }
    
    def _analyze_current_cv(self, cv_text: str) -> Dict[str, Any]:
        """Quick analysis of current CV"""
        lines = cv_text.split('\n')
        bullets = [line for line in lines if line.strip().startswith(('•', '-', '*'))]
        
        # Count different elements
        quantified_bullets = len([bullet for bullet in bullets 
                                if any(char in bullet for char in ['%', '$', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])])
        
        # Action verb analysis
        power_verbs = ['architected', 'orchestrated', 'spearheaded', 'optimized', 'transformed']
        power_verb_count = sum(1 for verb in power_verbs if verb.lower() in cv_text.lower())
        
        return {
            'total_bullets': len(bullets),
            'quantified_bullets': quantified_bullets,
            'quantification_rate': (quantified_bullets / max(len(bullets), 1)) * 100,
            'power_verb_count': power_verb_count,
            'word_count': len(cv_text.split()),
            'sections_detected': self._detect_sections(cv_text)
        }
    
    def _detect_sections(self, cv_text: str) -> List[str]:
        """Detect CV sections"""
        sections = []
        section_patterns = {
            'summary': r'(summary|profile|objective)',
            'experience': r'(experience|work|employment|career)',
            'education': r'education',
            'skills': r'skills',
            'certifications': r'(certifications|certificates)',
            'projects': r'projects'
        }
        
        cv_lower = cv_text.lower()
        for section, pattern in section_patterns.items():
            if any(pattern in line for line in cv_lower.split('\n')):
                sections.append(section)
        
        return sections
    
    def _extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract key requirements from job description"""
        jd_lower = job_description.lower()
        
        # Technical skills
        tech_skills = ['python', 'java', 'javascript', 'docker', 'kubernetes', 'aws', 'azure', 'devops']
        required_skills = [skill for skill in tech_skills if skill in jd_lower]
        
        # Experience level
        experience_years = 0
        if 'senior' in jd_lower or 'lead' in jd_lower:
            experience_years = 5
        elif 'mid' in jd_lower or 'intermediate' in jd_lower:
            experience_years = 3
        elif 'junior' in jd_lower or 'entry' in jd_lower:
            experience_years = 1
        
        return {
            'required_skills': required_skills,
            'experience_years': experience_years,
            'key_responsibilities': self._extract_responsibilities(job_description),
            'company_culture': self._extract_culture_keywords(job_description)
        }
    
    def _extract_responsibilities(self, job_description: str) -> List[str]:
        """Extract key responsibilities from JD"""
        # Simple extraction - could be enhanced
        lines = job_description.split('\n')
        responsibilities = []
        
        for line in lines:
            if any(indicator in line.lower() for indicator in ['responsible for', 'will', 'you will']):
                responsibilities.append(line.strip())
        
        return responsibilities[:5]  # Limit to top 5
    
    def _extract_culture_keywords(self, job_description: str) -> List[str]:
        """Extract company culture keywords"""
        culture_keywords = ['collaborative', 'innovative', 'agile', 'fast-paced', 'team-oriented', 'entrepreneurial']
        jd_lower = job_description.lower()
        
        return [keyword for keyword in culture_keywords if keyword in jd_lower]
    
    def _get_optimization_guidelines(self, optimization_level: str) -> Dict[str, Any]:
        """Get optimization guidelines based on level"""
        guidelines = {
            'conservative': {
                'max_changes_per_section': 2,
                'preserve_structure': True,
                'focus_areas': ['quantification', 'action_verbs'],
                'risk_level': 'low'
            },
            'balanced': {
                'max_changes_per_section': 4,
                'preserve_structure': True,
                'focus_areas': ['quantification', 'action_verbs', 'keywords', 'impact'],
                'risk_level': 'medium'
            },
            'aggressive': {
                'max_changes_per_section': 6,
                'preserve_structure': False,
                'focus_areas': ['complete_rewrite', 'quantification', 'action_verbs', 'keywords', 'impact', 'structure'],
                'risk_level': 'high'
            }
        }
        
        return guidelines.get(optimization_level, guidelines['balanced'])
    
    def _generate_optimizations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimizations using LLM"""
        try:
            # Prepare prompt for LLM
            prompt = self._create_optimization_prompt(context)
            
            # Call LLM API
            response = self._call_llm_api(prompt)
            
            # Parse response
            return self._parse_optimization_response(response, context['cv_text'])
            
        except Exception as e:
            logger.error(f"LLM optimization failed: {e}")
            # Fallback to rule-based optimization
            return self._fallback_optimization(context)
    
    def _create_optimization_prompt(self, context: Dict[str, Any]) -> str:
        """Create optimization prompt for LLM"""
        prompt = f"""
You are an expert CV optimization specialist. Your task is to improve the following CV while maintaining its authenticity and factual accuracy.

CURRENT CV:
{context['cv_text']}

OPTIMIZATION LEVEL: {context['optimization_level']}

CURRENT ANALYSIS:
- Total bullet points: {context['current_analysis']['total_bullets']}
- Quantified bullets: {context['current_analysis']['quantified_bullets']} ({context['current_analysis']['quantification_rate']:.1f}%)
- Power verbs used: {context['current_analysis']['power_verb_count']}

OPTIMIZATION GUIDELINES:
- Focus on: {', '.join(context['optimization_guidelines']['focus_areas'])}
- Max changes per section: {context['optimization_guidelines']['max_changes_per_section']}
- Risk level: {context['optimization_guidelines']['risk_level']}

INDUSTRY STANDARDS TO FOLLOW:
- Use Tier 1 action verbs: architected, orchestrated, spearheaded, optimized, transformed
- Quantify 80%+ of achievements with specific numbers, percentages, or dollar amounts
- Focus on impact and results, not just responsibilities
- Use ATS-friendly formatting
"""
        
        if context.get('job_description'):
            prompt += f"""

TARGET JOB DESCRIPTION:
{context['job_description']}

REQUIRED SKILLS TO EMPHASIZE:
{', '.join(context['job_requirements'].get('required_skills', []))}
"""
        
        prompt += """

Please provide:
1. An optimized version of the CV
2. A list of specific improvements made
3. Reasoning for each major change

Return your response in this JSON format:
{
    "optimized_content": "[full optimized CV text]",
    "improvements": [
        {
            "section": "[section name]",
            "original": "[original text]",
            "improved": "[improved text]",
            "reason": "[reason for change]",
            "impact_score": [1-10 rating]
        }
    ],
    "summary": "[brief summary of optimizations made]"
}
"""
        
        return prompt
    
    def _call_llm_api(self, prompt: str) -> str:
        """Call LLM API (Ollama)"""
        try:
            if self.llm_config['provider'] == 'ollama':
                url = f"{self.llm_config['base_url']}/api/generate"
                payload = {
                    "model": self.llm_config['model'],
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 4000
                    }
                }
                
                response = requests.post(url, json=payload, timeout=120)
                response.raise_for_status()
                
                return response.json().get('response', '')
            
            else:
                raise ValueError(f"Unsupported LLM provider: {self.llm_config['provider']}")
                
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            raise
    
    def _parse_optimization_response(self, response: str, original_cv: str) -> Dict[str, Any]:
        """Parse LLM optimization response"""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                result = json.loads(json_str)
                
                # Validate required fields
                if 'optimized_content' in result and 'improvements' in result:
                    return result
            
            # If JSON parsing fails, create structured response
            return {
                'optimized_content': response if len(response) > len(original_cv) * 0.8 else original_cv,
                'improvements': [{
                    'section': 'general',
                    'original': 'Various sections',
                    'improved': 'Enhanced content',
                    'reason': 'LLM optimization applied',
                    'impact_score': 7
                }],
                'summary': 'CV optimized using AI analysis'
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return self._create_fallback_response(original_cv)
    
    def _create_fallback_response(self, original_cv: str) -> Dict[str, Any]:
        """Create fallback response when LLM fails"""
        return {
            'optimized_content': original_cv,
            'improvements': [],
            'summary': 'Optimization failed - original content preserved',
            'fallback_used': True
        }
    
    def _fallback_optimization(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based fallback optimization"""
        cv_text = context['cv_text']
        improvements = []
        
        # Simple rule-based improvements
        lines = cv_text.split('\n')
        optimized_lines = []
        
        for line in lines:
            optimized_line = line
            
            # Replace weak verbs with stronger ones
            verb_replacements = {
                'worked on': 'developed',
                'helped with': 'contributed to',
                'was responsible for': 'managed',
                'assisted': 'supported'
            }
            
            original_line = line
            for weak, strong in verb_replacements.items():
                if weak in line.lower():
                    optimized_line = line.lower().replace(weak, strong)
                    if optimized_line != original_line:
                        improvements.append({
                            'section': 'experience',
                            'original': original_line,
                            'improved': optimized_line,
                            'reason': f'Replaced weak verb "{weak}" with stronger "{strong}"',
                            'impact_score': 6
                        })
            
            optimized_lines.append(optimized_line)
        
        return {
            'optimized_content': '\n'.join(optimized_lines),
            'improvements': improvements,
            'summary': f'Applied {len(improvements)} rule-based improvements',
            'fallback_used': True
        }
    
    def _validate_improvements(self, original: str, optimized: str) -> Dict[str, Any]:
        """Validate that improvements are actually better"""
        original_analysis = self._analyze_current_cv(original)
        optimized_analysis = self._analyze_current_cv(optimized)
        
        improvements = {
            'quantification_improvement': optimized_analysis['quantification_rate'] - original_analysis['quantification_rate'],
            'power_verb_improvement': optimized_analysis['power_verb_count'] - original_analysis['power_verb_count'],
            'length_change': len(optimized.split()) - len(original.split()),
            'bullet_count_change': optimized_analysis['total_bullets'] - original_analysis['total_bullets']
        }
        
        # Calculate overall improvement score
        improvement_score = 0
        if improvements['quantification_improvement'] > 0:
            improvement_score += 30
        if improvements['power_verb_improvement'] > 0:
            improvement_score += 25
        if -50 <= improvements['length_change'] <= 200:  # Reasonable length change
            improvement_score += 20
        if improvements['bullet_count_change'] >= 0:  # Didn't lose content
            improvement_score += 25
        
        return {
            'improvements': improvements,
            'improvement_score': improvement_score,
            'validation_passed': improvement_score >= 50,
            'original_analysis': original_analysis,
            'optimized_analysis': optimized_analysis
        }
    
    def get_optimization_suggestions(self, cv_text: str, job_description: str = "") -> List[Dict[str, Any]]:
        """Get specific optimization suggestions without full optimization"""
        try:
            analysis = self._analyze_current_cv(cv_text)
            suggestions = []
            
            # Quantification suggestions
            if analysis['quantification_rate'] < 80:
                suggestions.append({
                    'category': 'quantification',
                    'priority': 'high',
                    'suggestion': f"Add numbers to {analysis['total_bullets'] - analysis['quantified_bullets']} more bullet points",
                    'impact': 'Quantified achievements are 40% more likely to pass ATS screening',
                    'examples': ['Increased efficiency by 25%', 'Managed team of 8 developers', 'Reduced costs by $50K annually']
                })
            
            # Action verb suggestions
            if analysis['power_verb_count'] < 5:
                suggestions.append({
                    'category': 'action_verbs',
                    'priority': 'high',
                    'suggestion': 'Replace weak verbs with powerful action verbs',
                    'impact': 'Strong action verbs improve readability and impact',
                    'examples': ['Architected scalable solutions', 'Orchestrated cross-team initiatives', 'Spearheaded digital transformation']
                })
            
            # Section suggestions
            missing_sections = ['summary', 'skills'] - set(analysis['sections_detected'])
            if missing_sections:
                suggestions.append({
                    'category': 'structure',
                    'priority': 'medium',
                    'suggestion': f"Add missing sections: {', '.join(missing_sections)}",
                    'impact': 'Complete sections improve ATS parsing and readability',
                    'examples': ['Professional Summary with 3-4 key achievements', 'Technical Skills section with relevant technologies']
                })
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return []
    
    def save_optimization_result(self, result: Dict[str, Any], output_path: Path) -> bool:
        """Save optimization result to file"""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Optimization result saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving optimization result: {e}")
            return False
