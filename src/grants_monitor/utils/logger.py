"""
Logging configuration utilities.

This module sets up structured logging for the application.
"""

import sys
from pathlib import Path
from typing import Dict, Any

from loguru import logger


def setup_logging(config: Dict[str, Any]) -> None:
    """Setup application logging.
    
    Args:
        config: Logging configuration dictionary
    """
    # Remove default handler
    logger.remove()
    
    # Get configuration values
    level = config.get('level', 'INFO')
    format_str = config.get('format', 
        "<green>{time}</green> | <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    # Console handler
    logger.add(
        sys.stderr,
        format=format_str,
        level=level,
        colorize=True
    )
    
    # File handler (if configured)
    log_file = config.get('file')
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_path,
            format=format_str,
            level=level,
            rotation=config.get('rotation', '10 MB'),
            retention=config.get('retention', '30 days'),
            compression='gz'
        )
    
    logger.info("Logging configured successfully")
