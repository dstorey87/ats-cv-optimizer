"""Enhanced ATS Scanner with Advanced Analysis"""

import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from .scanner import ATSScanner
from .industry_standards import IndustryStandards

logger = logging.getLogger(__name__)

class EnhancedATSScanner(ATSScanner):
    """Enhanced scanner with industry standards and advanced analysis"""
    
    def __init__(self):
        super().__init__()
        self.industry_standards = IndustryStandards()
        
        # Enhanced keyword categories
        self.enhanced_keywords = {
            **self.ats_keywords,
            'tier1_verbs': [
                'architected', 'orchestrated', 'spearheaded', 'pioneered', 'transformed',
                'revolutionized', 'optimized', 'streamlined', 'automated', 'scaled'
            ],
            'tier2_verbs': [
                'developed', 'implemented', 'created', 'built', 'designed', 'managed',
                'led', 'delivered', 'executed', 'coordinated'
            ],
            'tier3_verbs': [
                'assisted', 'helped', 'participated', 'supported', 'contributed',
                'worked', 'involved', 'collaborated', 'engaged', 'handled'
            ],
            'leadership_indicators': [
                'led team', 'managed', 'supervised', 'mentored', 'coached',
                'directed', 'oversaw', 'guided', 'trained', 'developed team'
            ],
            'impact_indicators': [
                'reduced', 'increased', 'improved', 'enhanced', 'optimized',
                'decreased', 'accelerated', 'generated', 'saved', 'achieved'
            ]
        }
    
    def enhanced_scan(self, cv_path: Path, job_description: str = "", 
                     target_role: str = "") -> Dict[str, Any]:
        """Perform enhanced ATS scan with industry standards"""
        try:
            # Get base scan results
            results = self.scan_cv(cv_path, job_description)
            
            if 'error' in results:
                return results
            
            # Extract CV text
            cv_text = self._extract_text(cv_path)
            
            # Add enhanced analysis
            results['enhanced_analysis'] = {
                'industry_standards': self._analyze_industry_standards(cv_text),
                'verb_hierarchy': self._analyze_verb_hierarchy(cv_text),
                'leadership_analysis': self._analyze_leadership_indicators(cv_text),
                'impact_analysis': self._analyze_impact_statements(cv_text),
                'role_alignment': self._analyze_role_alignment(cv_text, target_role),
                'content_depth': self._analyze_content_depth(cv_text),
                'professional_presentation': self._analyze_presentation(cv_text)
            }
            
            # Recalculate enhanced overall score
            results['enhanced_score'] = self._calculate_enhanced_score(
                results['sections'], results['enhanced_analysis']
            )
            
            # Generate enhanced recommendations
            results['enhanced_recommendations'] = self._generate_enhanced_recommendations(
                results['sections'], results['enhanced_analysis']
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error in enhanced scan: {e}")
            return {'error': str(e)}
    
    def _analyze_industry_standards(self, cv_text: str) -> Dict[str, Any]:
        """Analyze against 7 industry standards"""
        results = {}
        
        for standard_name, standard in self.industry_standards.get_all_standards().items():
            compliance_score = 0
            findings = []
            
            # Analyze based on standard criteria
            if standard_name == 'action_verb_hierarchy':
                compliance_score, findings = self._check_action_verb_compliance(cv_text, standard)
            elif standard_name == 'quantification_standard':
                compliance_score, findings = self._check_quantification_compliance(cv_text, standard)
            elif standard_name == 'ats_formatting':
                compliance_score, findings = self._check_ats_formatting_compliance(cv_text, standard)
            elif standard_name == 'keyword_optimization':
                compliance_score, findings = self._check_keyword_compliance(cv_text, standard)
            elif standard_name == 'professional_presentation':
                compliance_score, findings = self._check_presentation_compliance(cv_text, standard)
            elif standard_name == 'impact_demonstration':
                compliance_score, findings = self._check_impact_compliance(cv_text, standard)
            elif standard_name == 'role_alignment':
                compliance_score, findings = self._check_alignment_compliance(cv_text, standard)
            
            results[standard_name] = {
                'score': compliance_score,
                'findings': findings,
                'standard_details': standard
            }
        
        # Calculate overall industry compliance
        overall_score = sum(result['score'] for result in results.values()) / len(results)
        
        return {
            'standards': results,
            'overall_compliance_score': overall_score,
            'compliant_standards': len([r for r in results.values() if r['score'] >= 80]),
            'total_standards': len(results)
        }
    
    def _analyze_verb_hierarchy(self, cv_text: str) -> Dict[str, Any]:
        """Analyze action verb usage by tier"""
        cv_lower = cv_text.lower()
        
        tier1_count = sum(1 for verb in self.enhanced_keywords['tier1_verbs'] 
                         if verb in cv_lower)
        tier2_count = sum(1 for verb in self.enhanced_keywords['tier2_verbs'] 
                         if verb in cv_lower)
        tier3_count = sum(1 for verb in self.enhanced_keywords['tier3_verbs'] 
                         if verb in cv_lower)
        
        total_verbs = tier1_count + tier2_count + tier3_count
        
        # Calculate tier distribution score (higher tier verbs are better)
        if total_verbs > 0:
            tier_score = ((tier1_count * 3) + (tier2_count * 2) + (tier3_count * 1)) / (total_verbs * 3) * 100
        else:
            tier_score = 0
        
        return {
            'tier1_count': tier1_count,
            'tier2_count': tier2_count,
            'tier3_count': tier3_count,
            'total_verbs': total_verbs,
            'tier_distribution_score': tier_score,
            'recommendation': self._get_verb_recommendation(tier1_count, tier2_count, tier3_count)
        }
    
    def _analyze_leadership_indicators(self, cv_text: str) -> Dict[str, Any]:
        """Analyze leadership and management indicators"""
        cv_lower = cv_text.lower()
        
        leadership_terms = []
        for indicator in self.enhanced_keywords['leadership_indicators']:
            if indicator in cv_lower:
                leadership_terms.append(indicator)
        
        # Look for team size indicators
        team_sizes = re.findall(r'team of (\d+)|led (\d+)', cv_lower)
        team_size_mentions = len(team_sizes)
        
        # Look for management scope
        budget_mentions = len(re.findall(r'\$[\d,]+|budget', cv_lower))
        
        leadership_score = min(
            (len(leadership_terms) * 15) + (team_size_mentions * 20) + (budget_mentions * 10),
            100
        )
        
        return {
            'leadership_terms': leadership_terms,
            'leadership_term_count': len(leadership_terms),
            'team_size_mentions': team_size_mentions,
            'budget_mentions': budget_mentions,
            'leadership_score': leadership_score
        }
    
    def _analyze_impact_statements(self, cv_text: str) -> Dict[str, Any]:
        """Analyze impact and achievement statements"""
        # Find quantified impact statements
        impact_patterns = [
            r'(reduced|decreased|cut).*?(\d+%|\d+)',
            r'(increased|improved|grew|boosted).*?(\d+%|\d+)',
            r'(saved|generated).*?\$([\d,]+)',
            r'(achieved|delivered).*?(\d+%|\d+)',
        ]
        
        impact_statements = []
        for pattern in impact_patterns:
            matches = re.findall(pattern, cv_text, re.IGNORECASE)
            for match in matches:
                impact_statements.append(' '.join(match))
        
        # Analyze impact quality
        high_impact_count = len([stmt for stmt in impact_statements 
                               if any(term in stmt.lower() for term in ['million', '$', '%'])])
        
        impact_score = min((len(impact_statements) * 20) + (high_impact_count * 10), 100)
        
        return {
            'impact_statements': impact_statements[:10],  # Limit for display
            'total_impact_statements': len(impact_statements),
            'high_impact_statements': high_impact_count,
            'impact_score': impact_score
        }
    
    def _analyze_role_alignment(self, cv_text: str, target_role: str) -> Dict[str, Any]:
        """Analyze alignment with target role"""
        if not target_role:
            return {'score': 50, 'message': 'No target role specified'}
        
        # Role-specific keyword mapping
        role_keywords = {
            'devops': ['docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'aws', 'ci/cd'],
            'developer': ['python', 'java', 'javascript', 'react', 'node.js', 'api', 'database'],
            'data': ['python', 'sql', 'machine learning', 'pandas', 'numpy', 'visualization'],
            'manager': ['leadership', 'team', 'budget', 'strategy', 'stakeholder', 'project'],
            'architect': ['design', 'architecture', 'system', 'scalability', 'microservices']
        }
        
        target_lower = target_role.lower()
        cv_lower = cv_text.lower()
        
        # Find matching role category
        relevant_keywords = []
        for role_type, keywords in role_keywords.items():
            if role_type in target_lower:
                relevant_keywords.extend(keywords)
        
        if not relevant_keywords:
            # Generic analysis if no specific role match
            relevant_keywords = (self.enhanced_keywords['technical_skills'] + 
                               self.enhanced_keywords['soft_skills'])
        
        # Count matches
        matched_keywords = [kw for kw in relevant_keywords if kw in cv_lower]
        alignment_score = (len(matched_keywords) / max(len(relevant_keywords), 1)) * 100
        
        return {
            'target_role': target_role,
            'relevant_keywords': relevant_keywords[:20],  # Limit for display
            'matched_keywords': matched_keywords[:15],
            'alignment_score': alignment_score,
            'recommendation': self._get_alignment_recommendation(alignment_score)
        }
    
    def _analyze_content_depth(self, cv_text: str) -> Dict[str, Any]:
        """Analyze depth and quality of content"""
        lines = cv_text.split('\n')
        bullet_lines = [line for line in lines if line.strip().startswith(('•', '-', '*'))]
        
        # Analyze bullet point quality
        detailed_bullets = 0
        weak_bullets = 0
        
        for bullet in bullet_lines:
            word_count = len(bullet.split())
            if word_count >= 12:  # Detailed description
                detailed_bullets += 1
            elif word_count <= 4:  # Too brief
                weak_bullets += 1
        
        # Content depth metrics
        avg_bullet_length = sum(len(bullet.split()) for bullet in bullet_lines) / max(len(bullet_lines), 1)
        
        depth_score = min(
            (detailed_bullets * 15) - (weak_bullets * 5) + (avg_bullet_length * 2),
            100
        )
        
        return {
            'total_bullets': len(bullet_lines),
            'detailed_bullets': detailed_bullets,
            'weak_bullets': weak_bullets,
            'avg_bullet_length': avg_bullet_length,
            'depth_score': max(depth_score, 0)
        }
    
    def _analyze_presentation(self, cv_text: str) -> Dict[str, Any]:
        """Analyze professional presentation"""
        # Check for consistency indicators
        date_formats = len(set(re.findall(r'\d{4}|\d{1,2}/\d{4}|\w+ \d{4}', cv_text)))
        
        # Check for professional language
        unprofessional_terms = ['awesome', 'cool', 'stuff', 'things', 'guys']
        unprofessional_count = sum(1 for term in unprofessional_terms 
                                 if term in cv_text.lower())
        
        # Check for consistency in formatting
        bullet_formats = len(set(re.findall(r'^\s*([•\-\*])', cv_text, re.MULTILINE)))
        
        presentation_score = 100
        issues = []
        
        if date_formats > 2:
            presentation_score -= 15
            issues.append('Inconsistent date formatting')
        
        if unprofessional_count > 0:
            presentation_score -= unprofessional_count * 10
            issues.append(f'{unprofessional_count} unprofessional terms found')
        
        if bullet_formats > 1:
            presentation_score -= 10
            issues.append('Inconsistent bullet point formatting')
        
        return {
            'presentation_score': max(presentation_score, 0),
            'issues': issues,
            'date_format_consistency': date_formats <= 2,
            'professional_language': unprofessional_count == 0,
            'bullet_consistency': bullet_formats <= 1
        }
    
    def _calculate_enhanced_score(self, base_sections: Dict[str, Any], 
                                enhanced_analysis: Dict[str, Any]) -> int:
        """Calculate enhanced overall score"""
        # Base score (60% weight)
        base_score = sum([
            base_sections['keywords'].get('power_verbs', {}).get('score', 0) * 0.15,
            base_sections['keywords'].get('technical_skills', {}).get('score', 0) * 0.20,
            base_sections['formatting'].get('overall_formatting_score', 0) * 0.15,
            base_sections['ats_compatibility'].get('score', 0) * 0.10
        ]) * 0.6
        
        # Enhanced analysis (40% weight)
        enhanced_score = sum([
            enhanced_analysis['industry_standards']['overall_compliance_score'] * 0.15,
            enhanced_analysis['verb_hierarchy']['tier_distribution_score'] * 0.08,
            enhanced_analysis['leadership_analysis']['leadership_score'] * 0.05,
            enhanced_analysis['impact_analysis']['impact_score'] * 0.07,
            enhanced_analysis['content_depth']['depth_score'] * 0.03,
            enhanced_analysis['professional_presentation']['presentation_score'] * 0.02
        ]) * 0.4
        
        return int(base_score + enhanced_score)
    
    def _generate_enhanced_recommendations(self, base_sections: Dict[str, Any], 
                                        enhanced_analysis: Dict[str, Any]) -> List[str]:
        """Generate enhanced recommendations"""
        recommendations = []
        
        # Industry standards recommendations
        standards = enhanced_analysis['industry_standards']['standards']
        for standard_name, data in standards.items():
            if data['score'] < 70:
                recommendations.append(
                    f"Improve {standard_name.replace('_', ' ')}: {data['findings'][0] if data['findings'] else 'Review standard requirements'}"
                )
        
        # Verb hierarchy recommendations
        verb_analysis = enhanced_analysis['verb_hierarchy']
        if verb_analysis['tier1_count'] < 3:
            recommendations.append("Use more Tier 1 action verbs (architected, orchestrated, spearheaded)")
        
        # Leadership recommendations
        leadership = enhanced_analysis['leadership_analysis']
        if leadership['leadership_score'] < 50:
            recommendations.append("Add more leadership indicators and team management examples")
        
        # Impact recommendations
        impact = enhanced_analysis['impact_analysis']
        if impact['impact_score'] < 60:
            recommendations.append("Include more quantified impact statements with specific results")
        
        # Content depth recommendations
        depth = enhanced_analysis['content_depth']
        if depth['weak_bullets'] > 3:
            recommendations.append("Expand brief bullet points with more detailed descriptions")
        
        # Presentation recommendations
        presentation = enhanced_analysis['professional_presentation']
        for issue in presentation['issues']:
            recommendations.append(f"Fix presentation issue: {issue}")
        
        return recommendations[:12]  # Limit to top 12
    
    # Helper methods for industry standard compliance checks
    def _check_action_verb_compliance(self, cv_text: str, standard: Dict) -> Tuple[int, List[str]]:
        cv_lower = cv_text.lower()
        tier1_count = sum(1 for verb in self.enhanced_keywords['tier1_verbs'] if verb in cv_lower)
        
        if tier1_count >= 5:
            return 90, ["Excellent use of Tier 1 action verbs"]
        elif tier1_count >= 3:
            return 75, ["Good use of action verbs, add more Tier 1 verbs"]
        else:
            return 50, ["Need more powerful Tier 1 action verbs"]
    
    def _check_quantification_compliance(self, cv_text: str, standard: Dict) -> Tuple[int, List[str]]:
        bullet_lines = re.findall(r'^\s*[•\-\*].*$', cv_text, re.MULTILINE)
        quantified_bullets = [bullet for bullet in bullet_lines 
                            if re.search(r'\d+[%$]?|\$\d+', bullet)]
        
        if not bullet_lines:
            return 0, ["No bullet points found"]
        
        quantification_rate = len(quantified_bullets) / len(bullet_lines) * 100
        
        if quantification_rate >= 80:
            return 95, ["Excellent quantification rate"]
        elif quantification_rate >= 60:
            return 80, ["Good quantification, aim for 80%+ of bullets"]
        else:
            return int(quantification_rate), [f"Only {quantification_rate:.1f}% of bullets quantified"]
    
    def _check_ats_formatting_compliance(self, cv_text: str, standard: Dict) -> Tuple[int, List[str]]:
        issues = []
        score = 100
        
        if '\t' in cv_text:
            issues.append("Remove tab characters")
            score -= 20
        
        if not re.search(r'[\w.-]+@[\w.-]+\.\w+', cv_text):
            issues.append("Add proper email format")
            score -= 30
        
        return max(score, 0), issues if issues else ["ATS formatting compliant"]
    
    def _check_keyword_compliance(self, cv_text: str, standard: Dict) -> Tuple[int, List[str]]:
        cv_lower = cv_text.lower()
        tech_count = sum(1 for skill in self.enhanced_keywords['technical_skills'] if skill in cv_lower)
        
        if tech_count >= 12:
            return 90, ["Strong keyword presence"]
        elif tech_count >= 8:
            return 75, ["Good keyword coverage"]
        else:
            return 50, ["Need more relevant technical keywords"]
    
    def _check_presentation_compliance(self, cv_text: str, standard: Dict) -> Tuple[int, List[str]]:
        return self._analyze_presentation(cv_text)['presentation_score'], []
    
    def _check_impact_compliance(self, cv_text: str, standard: Dict) -> Tuple[int, List[str]]:
        impact_analysis = self._analyze_impact_statements(cv_text)
        return impact_analysis['impact_score'], []
    
    def _check_alignment_compliance(self, cv_text: str, standard: Dict) -> Tuple[int, List[str]]:
        # Generic alignment check
        return 70, ["Role alignment requires specific target role"]
    
    def _get_verb_recommendation(self, tier1: int, tier2: int, tier3: int) -> str:
        if tier1 >= 5:
            return "Excellent use of powerful action verbs"
        elif tier1 >= 3:
            return "Good verb usage, consider adding more Tier 1 verbs"
        else:
            return "Focus on using more impactful Tier 1 action verbs"
    
    def _get_alignment_recommendation(self, score: float) -> str:
        if score >= 80:
            return "Strong alignment with target role"
        elif score >= 60:
            return "Good alignment, consider adding more role-specific skills"
        else:
            return "Needs better alignment with target role requirements"
