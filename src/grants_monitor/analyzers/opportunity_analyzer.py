"""
Opportunity analyzer for assessing grant complexity and viability.
"""

from typing import Dict, Any
from ..data.models import Grant


class OpportunityAnalyzer:
    """Analyzes grant opportunities for complexity and other factors."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the opportunity analyzer."""
        self.config = config
    
    async def assess_complexity(self, grant: Grant) -> float:
        """Assess application complexity for a grant.
        
        Args:
            grant: Grant to analyze
            
        Returns:
            Complexity score (0-100, where 0 is simplest)
        """
        # Placeholder implementation
        # In reality, this would analyze:
        # - Application requirements
        # - Document complexity
        # - Consortium requirements
        # - Reporting obligations
        # - Budget complexity
        
        base_complexity = 30
        
        # Adjust based on funding amount (higher = more complex)
        if grant.funding_amount > 1000000:
            base_complexity += 30
        elif grant.funding_amount > 500000:
            base_complexity += 20
        elif grant.funding_amount > 100000:
            base_complexity += 10
        
        # Adjust based on keywords
        complex_keywords = ["consortium", "multi-partner", "phd", "research"]
        for keyword in complex_keywords:
            if any(keyword.lower() in desc.lower() for desc in [grant.title, grant.description]):
                base_complexity += 15
                break
        
        return min(base_complexity, 100)
