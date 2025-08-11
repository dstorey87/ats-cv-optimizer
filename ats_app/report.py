"""Report Generation Module"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import pandas as pd

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate comprehensive reports for CV analysis and optimization"""
    
    def __init__(self):
        self.report_templates = {
            'executive_summary': self._create_executive_summary,
            'detailed_analysis': self._create_detailed_analysis,
            'improvement_recommendations': self._create_improvement_recommendations,
            'comparison_report': self._create_comparison_report,
            'ats_compliance_report': self._create_ats_compliance_report
        }
    
    def generate_comprehensive_report(self, analysis_results: Dict[str, Any], 
                                    optimization_results: Optional[Dict[str, Any]] = None,
                                    output_path: Optional[Path] = None) -> Dict[str, Any]:
        """Generate comprehensive report combining analysis and optimization"""
        try:
            report = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'report_type': 'comprehensive_cv_analysis',
                    'cv_analyzed': analysis_results.get('cv_path', 'Unknown'),
                    'analysis_timestamp': analysis_results.get('timestamp'),
                    'optimization_applied': optimization_results is not None
                },
                'executive_summary': self._create_executive_summary(analysis_results, optimization_results),
                'detailed_analysis': self._create_detailed_analysis(analysis_results),
                'ats_compliance': self._create_ats_compliance_report(analysis_results),
                'improvement_recommendations': self._create_improvement_recommendations(analysis_results),
                'performance_metrics': self._create_performance_metrics(analysis_results)
            }
            
            # Add optimization comparison if available
            if optimization_results:
                report['optimization_comparison'] = self._create_comparison_report(
                    analysis_results, optimization_results
                )
            
            # Save report if path provided
            if output_path:
                self._save_report(report, output_path)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            return {'error': str(e)}
    
    def _create_executive_summary(self, analysis_results: Dict[str, Any], 
                                optimization_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create executive summary section"""
        try:
            overall_score = analysis_results.get('overall_score', 0)
            enhanced_score = analysis_results.get('enhanced_score', overall_score)
            
            # Determine grade
            if enhanced_score >= 90:
                grade = 'A+'
                assessment = 'Excellent'
            elif enhanced_score >= 80:
                grade = 'A'
                assessment = 'Very Good'
            elif enhanced_score >= 70:
                grade = 'B'
                assessment = 'Good'
            elif enhanced_score >= 60:
                grade = 'C'
                assessment = 'Needs Improvement'
            else:
                grade = 'D'
                assessment = 'Significant Improvements Required'
            
            # Key strengths and weaknesses
            strengths = self._identify_strengths(analysis_results)
            weaknesses = self._identify_weaknesses(analysis_results)
            
            # Priority actions
            priority_actions = self._get_priority_actions(analysis_results)
            
            summary = {
                'overall_assessment': {
                    'score': enhanced_score,
                    'grade': grade,
                    'assessment': assessment,
                    'improvement_potential': max(0, 95 - enhanced_score)
                },
                'key_strengths': strengths[:3],
                'critical_weaknesses': weaknesses[:3],
                'priority_actions': priority_actions[:5],
                'ats_readiness': {
                    'score': analysis_results.get('sections', {}).get('ats_compatibility', {}).get('score', 0),
                    'status': 'Ready' if analysis_results.get('sections', {}).get('ats_compatibility', {}).get('score', 0) >= 80 else 'Needs Work'
                }
            }
            
            # Add optimization summary if available
            if optimization_results and optimization_results.get('success'):
                validation = optimization_results.get('validation', {})
                summary['optimization_impact'] = {
                    'improvements_applied': len(optimization_results.get('improvements', [])),
                    'score_improvement': validation.get('improvement_score', 0),
                    'validation_passed': validation.get('validation_passed', False)
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error creating executive summary: {e}")
            return {'error': str(e)}
    
    def _create_detailed_analysis(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed analysis section"""
        try:
            sections = analysis_results.get('sections', {})
            enhanced_analysis = analysis_results.get('enhanced_analysis', {})
            
            detailed = {
                'content_analysis': {
                    'word_count': sections.get('content_quality', {}).get('word_count', 0),
                    'bullet_points': sections.get('content_quality', {}).get('bullet_points', 0),
                    'quantified_achievements': sections.get('quantification', {}).get('quantified_bullets', 0),
                    'quantification_rate': sections.get('quantification', {}).get('quantification_rate', 0),
                    'sections_found': sections.get('formatting', {}).get('sections', {})
                },
                'keyword_analysis': sections.get('keywords', {}),
                'formatting_analysis': {
                    'ats_compatibility_score': sections.get('ats_compatibility', {}).get('score', 0),
                    'formatting_issues': sections.get('ats_compatibility', {}).get('issues', []),
                    'section_completeness': sections.get('formatting', {}).get('section_score', 0)
                }
            }
            
            # Add enhanced analysis if available
            if enhanced_analysis:
                detailed['enhanced_metrics'] = {
                    'industry_compliance': enhanced_analysis.get('industry_standards', {}),
                    'verb_hierarchy': enhanced_analysis.get('verb_hierarchy', {}),
                    'leadership_indicators': enhanced_analysis.get('leadership_analysis', {}),
                    'impact_statements': enhanced_analysis.get('impact_analysis', {})
                }
            
            return detailed
            
        except Exception as e:
            logger.error(f"Error creating detailed analysis: {e}")
            return {'error': str(e)}
    
    def _create_ats_compliance_report(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create ATS compliance focused report"""
        try:
            ats_data = analysis_results.get('sections', {}).get('ats_compatibility', {})
            formatting_data = analysis_results.get('sections', {}).get('formatting', {})
            
            compliance = {
                'overall_score': ats_data.get('score', 0),
                'compatibility_issues': ats_data.get('issues', []),
                'contact_info_check': ats_data.get('contact_info', {}),
                'formatting_compliance': {
                    'section_structure': formatting_data.get('sections', {}),
                    'bullet_point_usage': formatting_data.get('bullet_points', 0),
                    'consistency_score': formatting_data.get('section_score', 0)
                },
                'keyword_optimization': analysis_results.get('sections', {}).get('keywords', {}),
                'recommendations': [
                    'Use standard section headers (Experience, Education, Skills)',
                    'Include complete contact information',
                    'Avoid special characters and complex formatting',
                    'Use consistent bullet point formatting',
                    'Include relevant keywords naturally in content'
                ]
            }
            
            # Add compliance status
            if compliance['overall_score'] >= 85:
                compliance['status'] = 'Excellent ATS Compatibility'
            elif compliance['overall_score'] >= 70:
                compliance['status'] = 'Good ATS Compatibility'
            elif compliance['overall_score'] >= 50:
                compliance['status'] = 'Moderate ATS Compatibility - Improvements Needed'
            else:
                compliance['status'] = 'Poor ATS Compatibility - Major Issues'
            
            return compliance
            
        except Exception as e:
            logger.error(f"Error creating ATS compliance report: {e}")
            return {'error': str(e)}
    
    def _create_improvement_recommendations(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create improvement recommendations section"""
        try:
            recommendations = {
                'high_priority': [],
                'medium_priority': [],
                'low_priority': [],
                'quick_wins': [],
                'strategic_improvements': []
            }
            
            # Get recommendations from analysis
            base_recommendations = analysis_results.get('recommendations', [])
            enhanced_recommendations = analysis_results.get('enhanced_recommendations', [])
            
            all_recommendations = base_recommendations + enhanced_recommendations
            
            # Categorize recommendations by priority and effort
            for rec in all_recommendations:
                rec_item = {
                    'recommendation': rec,
                    'estimated_impact': self._estimate_impact(rec),
                    'effort_level': self._estimate_effort(rec),
                    'category': self._categorize_recommendation(rec)
                }
                
                # Assign to priority levels
                if rec_item['estimated_impact'] >= 8:
                    recommendations['high_priority'].append(rec_item)
                elif rec_item['estimated_impact'] >= 6:
                    recommendations['medium_priority'].append(rec_item)
                else:
                    recommendations['low_priority'].append(rec_item)
                
                # Identify quick wins (high impact, low effort)
                if rec_item['estimated_impact'] >= 7 and rec_item['effort_level'] <= 3:
                    recommendations['quick_wins'].append(rec_item)
                
                # Identify strategic improvements (high impact, high effort)
                if rec_item['estimated_impact'] >= 8 and rec_item['effort_level'] >= 7:
                    recommendations['strategic_improvements'].append(rec_item)
            
            # Add implementation timeline
            recommendations['implementation_timeline'] = {
                'immediate': len(recommendations['quick_wins']),
                'short_term': len(recommendations['high_priority']) - len(recommendations['quick_wins']),
                'medium_term': len(recommendations['medium_priority']),
                'long_term': len(recommendations['strategic_improvements'])
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error creating improvement recommendations: {e}")
            return {'error': str(e)}
    
    def _create_comparison_report(self, analysis_results: Dict[str, Any], 
                                optimization_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create before/after comparison report"""
        try:
            validation = optimization_results.get('validation', {})
            improvements = optimization_results.get('improvements', [])
            
            comparison = {
                'score_comparison': {
                    'original_score': analysis_results.get('overall_score', 0),
                    'optimized_score': validation.get('optimized_analysis', {}).get('overall_score', 0),
                    'improvement': validation.get('improvement_score', 0)
                },
                'metric_improvements': validation.get('improvements', {}),
                'changes_summary': {
                    'total_improvements': len(improvements),
                    'sections_modified': len(set(imp.get('section', '') for imp in improvements)),
                    'average_impact_score': sum(imp.get('impact_score', 5) for imp in improvements) / max(len(improvements), 1)
                },
                'detailed_changes': improvements[:10],  # Limit to top 10 changes
                'validation_results': {
                    'passed': validation.get('validation_passed', False),
                    'quantification_improvement': validation.get('improvements', {}).get('quantification_improvement', 0),
                    'power_verb_improvement': validation.get('improvements', {}).get('power_verb_improvement', 0),
                    'length_change': validation.get('improvements', {}).get('length_change', 0)
                }
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error creating comparison report: {e}")
            return {'error': str(e)}
    
    def _create_performance_metrics(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create performance metrics dashboard"""
        try:
            sections = analysis_results.get('sections', {})
            enhanced_analysis = analysis_results.get('enhanced_analysis', {})
            
            metrics = {
                'readability_score': self._calculate_readability_score(sections),
                'keyword_density': self._calculate_keyword_density(sections),
                'impact_score': self._calculate_impact_score(sections, enhanced_analysis),
                'professional_score': self._calculate_professional_score(sections, enhanced_analysis),
                'ats_optimization_score': sections.get('ats_compatibility', {}).get('score', 0),
                'benchmark_comparison': self._create_benchmark_comparison(analysis_results)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error creating performance metrics: {e}")
            return {'error': str(e)}
    
    def _identify_strengths(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Identify CV strengths"""
        strengths = []
        sections = analysis_results.get('sections', {})
        
        if sections.get('quantification', {}).get('quantification_rate', 0) >= 70:
            strengths.append("Strong quantification of achievements")
        
        if sections.get('keywords', {}).get('technical_skills', {}).get('count', 0) >= 8:
            strengths.append("Good technical keyword coverage")
        
        if sections.get('ats_compatibility', {}).get('score', 0) >= 80:
            strengths.append("ATS-friendly formatting")
        
        enhanced = analysis_results.get('enhanced_analysis', {})
        if enhanced.get('verb_hierarchy', {}).get('tier1_count', 0) >= 3:
            strengths.append("Uses powerful action verbs")
        
        if enhanced.get('leadership_analysis', {}).get('leadership_score', 0) >= 60:
            strengths.append("Demonstrates leadership experience")
        
        return strengths if strengths else ["Basic structure present"]
    
    def _identify_weaknesses(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Identify CV weaknesses"""
        weaknesses = []
        sections = analysis_results.get('sections', {})
        
        if sections.get('quantification', {}).get('quantification_rate', 0) < 50:
            weaknesses.append("Insufficient quantification of achievements")
        
        if sections.get('keywords', {}).get('power_verbs', {}).get('count', 0) < 5:
            weaknesses.append("Limited use of strong action verbs")
        
        if sections.get('ats_compatibility', {}).get('score', 0) < 70:
            weaknesses.append("ATS compatibility issues")
        
        enhanced = analysis_results.get('enhanced_analysis', {})
        if enhanced.get('impact_analysis', {}).get('impact_score', 0) < 40:
            weaknesses.append("Limited demonstration of impact")
        
        if not sections.get('formatting', {}).get('sections', {}).get('summary', False):
            weaknesses.append("Missing professional summary")
        
        return weaknesses if weaknesses else ["No critical issues identified"]
    
    def _get_priority_actions(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Get priority actions based on analysis"""
        actions = []
        
        # High-impact, low-effort improvements
        sections = analysis_results.get('sections', {})
        
        if sections.get('quantification', {}).get('quantification_rate', 0) < 60:
            actions.append("Add specific numbers and percentages to 5+ bullet points")
        
        if not sections.get('formatting', {}).get('sections', {}).get('summary', False):
            actions.append("Add a 3-4 line professional summary at the top")
        
        if sections.get('keywords', {}).get('technical_skills', {}).get('count', 0) < 6:
            actions.append("Include more relevant technical skills and keywords")
        
        if sections.get('ats_compatibility', {}).get('issues'):
            actions.append(f"Fix ATS issues: {sections['ats_compatibility']['issues'][0]}")
        
        enhanced = analysis_results.get('enhanced_analysis', {})
        if enhanced.get('verb_hierarchy', {}).get('tier1_count', 0) < 2:
            actions.append("Replace weak verbs with powerful action verbs (architected, orchestrated, etc.)")
        
        return actions
    
    def _estimate_impact(self, recommendation: str) -> int:
        """Estimate impact of recommendation (1-10 scale)"""
        high_impact_keywords = ['quantif', 'action verb', 'ats', 'keyword', 'achievement']
        medium_impact_keywords = ['format', 'section', 'bullet', 'professional']
        
        rec_lower = recommendation.lower()
        
        if any(keyword in rec_lower for keyword in high_impact_keywords):
            return 8
        elif any(keyword in rec_lower for keyword in medium_impact_keywords):
            return 6
        else:
            return 4
    
    def _estimate_effort(self, recommendation: str) -> int:
        """Estimate effort required (1-10 scale)"""
        low_effort_keywords = ['add', 'include', 'fix', 'remove']
        high_effort_keywords = ['rewrite', 'restructure', 'complete', 'overhaul']
        
        rec_lower = recommendation.lower()
        
        if any(keyword in rec_lower for keyword in high_effort_keywords):
            return 8
        elif any(keyword in rec_lower for keyword in low_effort_keywords):
            return 3
        else:
            return 5
    
    def _categorize_recommendation(self, recommendation: str) -> str:
        """Categorize recommendation by type"""
        categories = {
            'content': ['quantif', 'achievement', 'bullet', 'verb'],
            'formatting': ['format', 'section', 'ats'],
            'keywords': ['keyword', 'skill', 'technical'],
            'structure': ['section', 'summary', 'experience']
        }
        
        rec_lower = recommendation.lower()
        
        for category, keywords in categories.items():
            if any(keyword in rec_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _calculate_readability_score(self, sections: Dict[str, Any]) -> int:
        """Calculate readability score"""
        content_quality = sections.get('content_quality', {})
        formatting = sections.get('formatting', {})
        
        score = 0
        score += min(formatting.get('bullet_score', 0), 40)  # Max 40 points for bullets
        score += min(content_quality.get('avg_words_per_sentence', 15) * 2, 30)  # Max 30 for sentence length
        score += min(formatting.get('section_score', 0) * 0.3, 30)  # Max 30 for sections
        
        return min(int(score), 100)
    
    def _calculate_keyword_density(self, sections: Dict[str, Any]) -> int:
        """Calculate keyword optimization score"""
        keywords = sections.get('keywords', {})
        
        tech_score = min(keywords.get('technical_skills', {}).get('count', 0) * 5, 40)
        power_verb_score = min(keywords.get('power_verbs', {}).get('count', 0) * 8, 40)
        job_match_score = min(keywords.get('job_match', {}).get('score', 0) * 0.2, 20)
        
        return min(int(tech_score + power_verb_score + job_match_score), 100)
    
    def _calculate_impact_score(self, sections: Dict[str, Any], enhanced: Dict[str, Any]) -> int:
        """Calculate impact demonstration score"""
        quantification_score = sections.get('quantification', {}).get('score', 0) * 0.4
        
        if enhanced.get('impact_analysis'):
            impact_score = enhanced['impact_analysis'].get('impact_score', 0) * 0.6
        else:
            impact_score = 0
        
        return min(int(quantification_score + impact_score), 100)
    
    def _calculate_professional_score(self, sections: Dict[str, Any], enhanced: Dict[str, Any]) -> int:
        """Calculate professional presentation score"""
        ats_score = sections.get('ats_compatibility', {}).get('score', 0) * 0.5
        
        if enhanced.get('professional_presentation'):
            presentation_score = enhanced['professional_presentation'].get('presentation_score', 0) * 0.5
        else:
            presentation_score = 40  # Default moderate score
        
        return min(int(ats_score + presentation_score), 100)
    
    def _create_benchmark_comparison(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create benchmark comparison"""
        overall_score = analysis_results.get('enhanced_score', analysis_results.get('overall_score', 0))
        
        benchmarks = {
            'industry_average': 65,
            'top_10_percent': 85,
            'ats_passing_threshold': 70,
            'interview_likely_threshold': 80
        }
        
        comparison = {}
        for benchmark_name, threshold in benchmarks.items():
            comparison[benchmark_name] = {
                'threshold': threshold,
                'current_score': overall_score,
                'meets_benchmark': overall_score >= threshold,
                'points_needed': max(0, threshold - overall_score)
            }
        
        return comparison
    
    def _save_report(self, report: Dict[str, Any], output_path: Path) -> bool:
        """Save report to multiple formats"""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save JSON report
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Save text summary
            txt_path = output_path.with_suffix('.txt')
            self._save_text_summary(report, txt_path)
            
            # Save CSV metrics
            csv_path = output_path.with_suffix('.csv')
            self._save_csv_metrics(report, csv_path)
            
            logger.info(f"Report saved in multiple formats: {output_path.stem}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return False
    
    def _save_text_summary(self, report: Dict[str, Any], output_path: Path) -> None:
        """Save human-readable text summary"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("CV ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            # Executive Summary
            exec_summary = report.get('executive_summary', {})
            assessment = exec_summary.get('overall_assessment', {})
            f.write(f"OVERALL SCORE: {assessment.get('score', 0)}/100 (Grade: {assessment.get('grade', 'N/A')})\n")
            f.write(f"ASSESSMENT: {assessment.get('assessment', 'N/A')}\n\n")
            
            # Strengths
            f.write("KEY STRENGTHS:\n")
            for strength in exec_summary.get('key_strengths', []):
                f.write(f"• {strength}\n")
            f.write("\n")
            
            # Weaknesses
            f.write("AREAS FOR IMPROVEMENT:\n")
            for weakness in exec_summary.get('critical_weaknesses', []):
                f.write(f"• {weakness}\n")
            f.write("\n")
            
            # Priority Actions
            f.write("PRIORITY ACTIONS:\n")
            for action in exec_summary.get('priority_actions', []):
                f.write(f"• {action}\n")
    
    def _save_csv_metrics(self, report: Dict[str, Any], output_path: Path) -> None:
        """Save metrics in CSV format"""
        metrics_data = []
        
        # Overall scores
        exec_summary = report.get('executive_summary', {})
        assessment = exec_summary.get('overall_assessment', {})
        metrics_data.append(['Overall Score', assessment.get('score', 0), '0-100', assessment.get('grade', 'N/A')])
        
        # Performance metrics
        performance = report.get('performance_metrics', {})
        for metric_name, score in performance.items():
            if isinstance(score, (int, float)):
                metrics_data.append([metric_name.replace('_', ' ').title(), score, '0-100', 'Score'])
        
        # Create DataFrame and save
        df = pd.DataFrame(metrics_data, columns=['Metric', 'Score', 'Scale', 'Type'])
        df.to_csv(output_path, index=False)
