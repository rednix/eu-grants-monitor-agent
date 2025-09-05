"""
Profile matcher for calculating grant relevance to business profile.
"""

from typing import Dict, Any
from ..data.models import Grant, BusinessProfile


class ProfileMatcher:
    """Matches grants to business profile for relevance scoring."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the profile matcher."""
        self.config = config
    
    async def calculate_relevance(self, grant: Grant, profile: BusinessProfile) -> float:
        """Calculate relevance score for a grant based on business profile.
        
        Args:
            grant: Grant to evaluate
            profile: Business profile to match against
            
        Returns:
            Relevance score (0-100)
        """
        relevance_score = 0.0
        
        # Country match bonus
        if profile.country in grant.eligible_countries:
            relevance_score += self.config.get('country_bonus', 10)
        
        # Company size match
        size_matches = {
            "micro": ["micro", "sme", "startup"],
            "small": ["small", "sme", "startup"], 
            "medium": ["medium", "sme"]
        }
        
        profile_size_keywords = size_matches.get(profile.company_size, [])
        if any(keyword in grant.target_organizations for keyword in profile_size_keywords):
            relevance_score += self.config.get('size_match_bonus', 15)
        
        # Expertise keyword matching
        expertise_weight = self.config.get('expertise_match_weight', 0.4)
        expertise_matches = 0
        total_expertise = len(profile.ai_expertise)
        
        if total_expertise > 0:
            for expertise in profile.ai_expertise:
                if any(expertise.replace('_', ' ') in keyword.lower() for keyword in grant.keywords):
                    expertise_matches += 1
            
            expertise_ratio = expertise_matches / total_expertise
            relevance_score += expertise_ratio * expertise_weight * 100
        
        # Industry matching
        industry_weight = self.config.get('industry_match_weight', 0.3)
        industry_matches = 0
        total_industries = len(profile.target_industries)
        
        if total_industries > 0:
            for industry in profile.target_industries:
                if any(industry in keyword.lower() for keyword in grant.keywords + [grant.title.lower(), grant.description.lower()]):
                    industry_matches += 1
            
            industry_ratio = industry_matches / total_industries
            relevance_score += industry_ratio * industry_weight * 100
        
        # Funding range match
        funding_weight = self.config.get('funding_range_weight', 0.3)
        min_funding = profile.preferred_funding_range['min']
        max_funding = profile.preferred_funding_range['max']
        
        if min_funding <= grant.funding_amount <= max_funding:
            relevance_score += funding_weight * 100
        elif grant.funding_amount < min_funding:
            # Partial score for smaller grants
            relevance_score += (grant.funding_amount / min_funding) * funding_weight * 50
        else:
            # Partial score for larger grants (might be too complex)
            excess_ratio = min(2.0, grant.funding_amount / max_funding)
            relevance_score += (2.0 - excess_ratio) * funding_weight * 50
        
        return min(relevance_score, 100)
