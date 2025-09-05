"""
Configuration management utilities.

This module handles loading and managing configuration files.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

import yaml
from loguru import logger


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config_dir = Path("config")
        self.config_path = config_path or self.config_dir / "config.yaml"
        self.business_profile_path = self.config_dir / "business_profile.yaml"
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
    
    def load_config(self) -> Dict[str, Any]:
        """Load main configuration file.
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            logger.info(f"Configuration loaded from {self.config_path}")
            return config or {}
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def load_business_profile(self) -> Dict[str, Any]:
        """Load business profile configuration.
        
        Returns:
            Business profile dictionary
        """
        if not self.business_profile_path.exists():
            logger.warning(f"Business profile not found: {self.business_profile_path}")
            return self._get_default_business_profile()
        
        try:
            with open(self.business_profile_path, 'r', encoding='utf-8') as f:
                profile = yaml.safe_load(f)
            
            logger.info(f"Business profile loaded from {self.business_profile_path}")
            return profile or {}
            
        except Exception as e:
            logger.error(f"Error loading business profile: {e}")
            return self._get_default_business_profile()
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(config, f, default_flow_style=False, indent=2)
            
            logger.info(f"Configuration saved to {self.config_path}")
            
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def create_default_configs(self) -> None:
        """Create default configuration files if they don't exist."""
        
        # Create main config file
        if not self.config_path.exists():
            default_config = self._get_default_config()
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(default_config, f, default_flow_style=False, indent=2)
            logger.info(f"Created default config: {self.config_path}")
        
        # Create business profile template
        if not self.business_profile_path.exists():
            default_profile = self._get_default_business_profile()
            with open(self.business_profile_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(default_profile, f, default_flow_style=False, indent=2)
            logger.info(f"Created business profile template: {self.business_profile_path}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "logging": {
                "level": "INFO",
                "format": "<green>{time}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "file": "logs/grants_monitor.log",
                "rotation": "10 MB",
                "retention": "30 days"
            },
            "scrapers": {
                "horizon_europe": {
                    "enabled": True,
                    "base_url": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/calls-for-proposals",
                    "rate_limit": {
                        "requests_per_minute": 30,
                        "delay_between_requests": 2
                    }
                },
                "digital_europe": {
                    "enabled": False,
                    "base_url": "https://digital-strategy.ec.europa.eu/en/activities/digital-programme"
                }
            },
            "analysis": {
                "keywords_weights": {
                    "artificial_intelligence": 10,
                    "machine_learning": 8,
                    "deep_learning": 8,
                    "nlp": 7,
                    "computer_vision": 7,
                    "data_science": 6,
                    "automation": 5,
                    "robotics": 6
                }
            },
            "matching": {
                "country_bonus": 10,
                "size_match_bonus": 15,
                "expertise_match_weight": 0.4,
                "industry_match_weight": 0.3,
                "funding_range_weight": 0.3
            },
            "scoring": {
                "weights": {
                    "relevance": 0.4,
                    "complexity": 0.3,
                    "amount": 0.2,
                    "deadline": 0.1
                }
            },
            "alerts": {
                "priority_threshold": 70,
                "check_interval_hours": 6,
                "deadline_warning_days": [30, 14, 7, 3, 1]
            },
            "notifications": {
                "email": {
                    "enabled": True,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "your-email@gmail.com",
                    "password": "your-app-password",
                    "from_address": "your-email@gmail.com",
                    "to_addresses": ["recipient@example.com"]
                },
                "slack": {
                    "enabled": False,
                    "webhook_url": "your-slack-webhook-url"
                }
            },
            "database": {
                "type": "sqlite",
                "sqlite": {
                    "path": "data/grants.db"
                },
                "postgresql": {
                    "host": "localhost",
                    "port": 5432,
                    "database": "grants_monitor",
                    "username": "grants_user",
                    "password": "password"
                }
            }
        }
    
    def _get_default_business_profile(self) -> Dict[str, Any]:
        """Get default business profile."""
        return {
            "company_name": "Your AI Consultancy",
            "company_size": "small",  # micro, small, medium
            "country": "DE",  # ISO country code
            
            "ai_expertise": [
                "machine_learning",
                "natural_language_processing",
                "computer_vision",
                "deep_learning",
                "data_analytics"
            ],
            
            "technology_focus": [
                "python",
                "tensorflow",
                "pytorch",
                "scikit_learn",
                "cloud_computing"
            ],
            
            "target_industries": [
                "healthcare",
                "finance",
                "manufacturing",
                "retail",
                "logistics"
            ],
            
            "business_sectors": [
                "consulting",
                "software_development",
                "research_development",
                "training"
            ],
            
            "preferred_funding_range": {
                "min": 50000,
                "max": 500000
            },
            
            "max_project_duration_months": 24,
            "complexity_preference": "simple",  # simple, medium, complex
            "team_size": 5
        }
