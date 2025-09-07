#!/usr/bin/env python3
"""
Registration script for EU Grants Monitor Masumi Agent.

This script registers the EU Grants Monitor agent with the Masumi registry,
making it available for payment-based access via the Cardano blockchain.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from loguru import logger
from grants_monitor.masumi_agent import (
    EUGrantsMonitorMasumiAgent,
    create_masumi_config,
    get_default_agent_config
)


async def register_agent(
    payment_api_key: str,
    api_base_url: str,
    network: str = "Preprod",
    custom_config: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Register the EU Grants Monitor agent with Masumi.
    
    Args:
        payment_api_key: Masumi payment API key
        api_base_url: Base URL where the agent API is hosted
        network: Cardano network ("Preprod" or "Mainnet")
        custom_config: Custom agent configuration overrides
    
    Returns:
        Registration result from Masumi
    """
    logger.info("Starting EU Grants Monitor Masumi agent registration...")
    
    # Create Masumi configuration
    masumi_config = create_masumi_config(
        payment_api_key=payment_api_key,
        payment_service_url="https://api.masumi.io"
    )
    
    # Get agent configuration
    agent_config = get_default_agent_config(api_base_url)
    if custom_config:
        agent_config.update(custom_config)
    
    # Create the Masumi agent wrapper
    masumi_agent = EUGrantsMonitorMasumiAgent()
    
    # Create and configure the Masumi agent
    agent = masumi_agent.create_masumi_agent(
        masumi_config=masumi_config,
        agent_config=agent_config,
        network=network
    )
    
    logger.info(f"Created agent: {agent_config['name']}")
    logger.info(f"Network: {network}")
    logger.info(f"API Base URL: {api_base_url}")
    logger.info(f"Pricing: {agent_config['pricing_quantity']} {agent_config['pricing_unit']} per request")
    
    # Register with Masumi
    try:
        registration_result = await masumi_agent.register_with_masumi()
        logger.info("✅ Successfully registered EU Grants Monitor with Masumi!")
        return registration_result
    except Exception as e:
        logger.error(f"❌ Failed to register agent: {e}")
        raise


async def check_registration(
    payment_api_key: str,
    wallet_vkey: str,
    network: str = "Preprod"
) -> Dict[str, Any]:
    """
    Check registration status of the agent.
    
    Args:
        payment_api_key: Masumi payment API key
        wallet_vkey: Wallet verification key to check
        network: Cardano network
    
    Returns:
        Registration status from Masumi
    """
    logger.info("Checking registration status...")
    
    # Create Masumi configuration
    masumi_config = create_masumi_config(
        payment_api_key=payment_api_key,
        payment_service_url="https://api.masumi.io"
    )
    
    # Create the Masumi agent wrapper
    masumi_agent = EUGrantsMonitorMasumiAgent()
    
    # Create dummy agent for status checking
    agent_config = get_default_agent_config("http://localhost:8000")
    masumi_agent.create_masumi_agent(
        masumi_config=masumi_config,
        agent_config=agent_config,
        network=network
    )
    
    # Check status
    status = await masumi_agent.check_registration_status(wallet_vkey)
    logger.info("✅ Retrieved registration status")
    return status


def get_example_configs() -> Dict[str, Dict[str, Any]]:
    """Get example configurations for different deployment scenarios."""
    return {
        "development": {
            "name": "eu-grants-monitor-dev",
            "api_base_url": "http://localhost:8000",
            "pricing_quantity": "1000000",  # 1 ADA
            "capability_version": "1.0.0-dev"
        },
        "staging": {
            "name": "eu-grants-monitor-staging",
            "api_base_url": "https://staging.eu-grants-monitor.com",
            "pricing_quantity": "1500000",  # 1.5 ADA
            "capability_version": "1.0.0-beta"
        },
        "production": {
            "name": "eu-grants-monitor",
            "api_base_url": "https://api.eu-grants-monitor.com",
            "pricing_quantity": "2000000",  # 2 ADA
            "capability_version": "1.0.0"
        }
    }


async def main():
    """Main registration function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Register EU Grants Monitor agent with Masumi registry"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="Masumi payment API key"
    )
    parser.add_argument(
        "--api-url",
        required=True,
        help="Base URL where the agent API is hosted"
    )
    parser.add_argument(
        "--network",
        choices=["Preprod", "Mainnet"],
        default="Preprod",
        help="Cardano network to use"
    )
    parser.add_argument(
        "--environment",
        choices=["development", "staging", "production"],
        default="development",
        help="Deployment environment"
    )
    parser.add_argument(
        "--check-status",
        action="store_true",
        help="Check registration status instead of registering"
    )
    parser.add_argument(
        "--wallet-vkey",
        help="Wallet verification key (required for status check)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show configuration without registering"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.check_status and not args.wallet_vkey:
        parser.error("--wallet-vkey is required when using --check-status")
    
    # Get configuration for environment
    example_configs = get_example_configs()
    custom_config = example_configs.get(args.environment, {})
    custom_config["api_base_url"] = args.api_url
    
    if args.dry_run:
        # Show configuration
        print("🔍 Agent Configuration:")
        print("=" * 50)
        base_config = get_default_agent_config(args.api_url)
        base_config.update(custom_config)
        
        for key, value in base_config.items():
            print(f"{key}: {value}")
        
        print(f"\\nNetwork: {args.network}")
        print(f"Environment: {args.environment}")
        return
    
    try:
        if args.check_status:
            # Check registration status
            status = await check_registration(
                payment_api_key=args.api_key,
                wallet_vkey=args.wallet_vkey,
                network=args.network
            )
            
            print("\\n📊 Registration Status:")
            print("=" * 50)
            print(f"Status: {status}")
            
        else:
            # Register the agent
            result = await register_agent(
                payment_api_key=args.api_key,
                api_base_url=args.api_url,
                network=args.network,
                custom_config=custom_config
            )
            
            print("\\n🎉 Registration Complete!")
            print("=" * 50)
            print(f"Agent Name: {custom_config.get('name', 'eu-grants-monitor')}")
            print(f"Network: {args.network}")
            print(f"API URL: {args.api_url}")
            print(f"Environment: {args.environment}")
            
            if 'data' in result:
                print(f"Registration ID: {result.get('registrationId', 'N/A')}")
    
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
