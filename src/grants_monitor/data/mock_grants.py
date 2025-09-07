"""
Mock grant data for testing and demonstration purposes.

This module contains sample grant opportunities that demonstrate
the various features of the application assistance system.
"""

from datetime import date, timedelta
from ..data.models import Grant, FundingProgram


def get_mock_grants():
    """Get a collection of mock grant opportunities for testing."""
    
    grants = []
    
    # Grant 1: AI for Healthcare SMEs
    grants.append(Grant(
        id="HE-2024-AI-001",
        title="AI for Healthcare SMEs",
        description=(
            "This call supports Small and Medium Enterprises (SMEs) in developing "
            "artificial intelligence solutions for healthcare applications. Focus areas "
            "include machine learning for medical diagnosis, natural language processing "
            "for clinical documentation, and computer vision for medical imaging. "
            "Projects should demonstrate clear clinical validation and regulatory compliance."
        ),
        synopsis="AI solutions for healthcare: ML diagnosis, NLP clinical docs, CV medical imaging",
        program=FundingProgram.HORIZON_EUROPE,
        funding_amount=250000,
        min_funding=50000,
        max_funding=500000,
        deadline=date.today() + timedelta(days=45),
        start_date=date.today() + timedelta(days=120),
        end_date=date.today() + timedelta(days=850),
        eligible_countries=["DE", "FR", "IT", "ES", "NL", "BE", "AT", "SE", "DK", "FI"],
        target_organizations=["SME", "Small Enterprise", "Medium Enterprise"],
        keywords=[
            "artificial intelligence", "healthcare", "machine learning", "medical diagnosis",
            "clinical validation", "regulatory compliance", "medical imaging", "nlp"
        ],
        url="https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/HORIZON-EIC-2024-PATHFINDEROPEN-01",
        documents_url="https://ec.europa.eu/info/funding-tenders/opportunities/documents",
        relevance_score=0.0,
        complexity_score=0.0,
        priority_score=0.0
    ))
    
    # Grant 2: Digital Innovation for Manufacturing
    grants.append(Grant(
        id="DIGITAL-EU-2024-002",
        title="Digital Innovation for Manufacturing SMEs",
        description=(
            "Supporting digital transformation in European manufacturing through "
            "Industry 4.0 technologies. This call targets SMEs developing solutions "
            "in areas such as IoT integration, predictive maintenance using AI, "
            "automated quality control, and supply chain optimization. Projects should "
            "demonstrate measurable productivity improvements and scalability."
        ),
        synopsis="Industry 4.0: IoT, AI predictive maintenance, automated quality control",
        program=FundingProgram.DIGITAL_EUROPE,
        funding_amount=150000,
        min_funding=75000,
        max_funding=300000,
        deadline=date.today() + timedelta(days=60),
        start_date=date.today() + timedelta(days=90),
        end_date=date.today() + timedelta(days=720),
        eligible_countries=["DE", "FR", "IT", "ES", "PL", "CZ", "HU", "SK"],
        target_organizations=["SME", "Manufacturing Company", "Technology Provider"],
        keywords=[
            "digital transformation", "industry 40", "iot", "predictive maintenance",
            "automation", "supply chain", "manufacturing", "productivity"
        ],
        url="https://digital-strategy.ec.europa.eu/en/activities/digital-programme",
        documents_url="https://digital-strategy.ec.europa.eu/documents",
        relevance_score=0.0,
        complexity_score=0.0,
        priority_score=0.0
    ))
    
    # Grant 3: Large Consortium AI Research
    grants.append(Grant(
        id="HE-2024-AI-CONSORTIUM-003",
        title="Next-Generation AI for European Competitiveness",
        description=(
            "Large-scale research and innovation action focusing on breakthrough AI "
            "technologies for multiple sectors. This call requires international "
            "consortiums with at least 5 partners from different EU countries, "
            "including research institutions, large enterprises, and SMEs. Focus areas "
            "include federated learning, explainable AI, edge computing, and ethical AI. "
            "Strong emphasis on European digital sovereignty and global competitiveness."
        ),
        synopsis="Large consortium: Federated learning, explainable AI, edge computing, ethical AI",
        program=FundingProgram.HORIZON_EUROPE,
        funding_amount=3500000,
        min_funding=2000000,
        max_funding=5000000,
        deadline=date.today() + timedelta(days=90),
        start_date=date.today() + timedelta(days=180),
        end_date=date.today() + timedelta(days=1460),  # 4 years
        eligible_countries=["EU", "Associated Countries"],
        target_organizations=[
            "Research Institution", "Large Enterprise", "SME", "University"
        ],
        keywords=[
            "artificial intelligence", "federated learning", "explainable ai",
            "edge computing", "ethical ai", "digital sovereignty", "research",
            "innovation", "consortium"
        ],
        url="https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/HORIZON-CL4-2024-HUMAN-01",
        documents_url="https://ec.europa.eu/info/funding-tenders/opportunities/documents",
        relevance_score=0.0,
        complexity_score=0.0,
        priority_score=0.0
    ))
    
    # Grant 4: Green Tech Innovation
    grants.append(Grant(
        id="LIFE-2024-GREEN-004",
        title="AI-Powered Environmental Monitoring Solutions",
        description=(
            "This call supports SMEs and start-ups in developing AI-powered solutions "
            "for environmental monitoring and climate change mitigation. Focus areas "
            "include satellite data analysis, IoT sensor networks, predictive modeling "
            "for environmental risks, and automated reporting systems. Solutions should "
            "contribute to the European Green Deal objectives."
        ),
        synopsis="Green AI: Satellite analysis, IoT sensors, environmental risk modeling",
        program=FundingProgram.LIFE,
        funding_amount=180000,
        min_funding=80000,
        max_funding=250000,
        deadline=date.today() + timedelta(days=75),
        start_date=date.today() + timedelta(days=150),
        end_date=date.today() + timedelta(days=880),
        eligible_countries=["EU27", "Iceland", "Norway", "Turkey"],
        target_organizations=["SME", "Start-up", "Environmental Organization"],
        keywords=[
            "environmental monitoring", "climate change", "green deal", "satellite data",
            "iot sensors", "predictive modeling", "environmental risks", "sustainability"
        ],
        url="https://ec.europa.eu/easme/en/life",
        documents_url="https://ec.europa.eu/easme/en/life/documents",
        relevance_score=0.0,
        complexity_score=0.0,
        priority_score=0.0
    ))
    
    # Grant 5: Education Technology
    grants.append(Grant(
        id="ERASMUS-2024-EDTECH-005",
        title="AI in Education and Training",
        description=(
            "Supporting the development of AI-powered educational tools and platforms "
            "for enhanced learning experiences. This call targets organizations "
            "developing personalized learning systems, automated assessment tools, "
            "language learning applications, and skills training platforms. Special "
            "focus on digital inclusion and accessibility."
        ),
        synopsis="EdTech AI: Personalized learning, automated assessment, language apps",
        program=FundingProgram.ERASMUS_PLUS,
        funding_amount=120000,
        min_funding=60000,
        max_funding=200000,
        deadline=date.today() + timedelta(days=30),  # Tight deadline
        start_date=date.today() + timedelta(days=60),
        end_date=date.today() + timedelta(days=550),
        eligible_countries=["EU", "Associated Countries", "Third Countries"],
        target_organizations=["Educational Institution", "SME", "NGO", "Training Provider"],
        keywords=[
            "education technology", "personalized learning", "automated assessment",
            "language learning", "skills training", "digital inclusion", "accessibility",
            "ai in education"
        ],
        url="https://ec.europa.eu/programmes/erasmus-plus/",
        documents_url="https://ec.europa.eu/programmes/erasmus-plus/documents",
        relevance_score=0.0,
        complexity_score=0.0,
        priority_score=0.0
    ))
    
    return grants


def get_grant_by_id(grant_id: str) -> Grant:
    """Get a specific grant by ID.
    
    Args:
        grant_id: The grant identifier
        
    Returns:
        Grant object if found
        
    Raises:
        ValueError: If grant ID is not found
    """
    grants = get_mock_grants()
    for grant in grants:
        if grant.id == grant_id:
            return grant
    
    raise ValueError(f"Grant with ID '{grant_id}' not found")


def get_grants_by_keyword(keyword: str) -> list[Grant]:
    """Get grants that match a specific keyword.
    
    Args:
        keyword: Keyword to search for
        
    Returns:
        List of matching grants
    """
    grants = get_mock_grants()
    matching_grants = []
    
    for grant in grants:
        if (keyword.lower() in grant.title.lower() or
            keyword.lower() in grant.description.lower() or
            any(keyword.lower() in kw.lower() for kw in grant.keywords)):
            matching_grants.append(grant)
    
    return matching_grants
