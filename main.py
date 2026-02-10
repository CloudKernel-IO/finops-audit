"""CloudKernel-IO FinOps audit entry point."""

import logging
import argparse
from engines.azure_engine import AzureAudit
from engines.aws_engine import AWSAudit
from engines.gcp_engine import GCPAudit

# Configuración de logging profesional
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="CloudKernel FinOps Audit Engine")
    parser.add_argument("--all", action="store_true", help="Run audit on all cloud providers")
    args = parser.parse_args()

    if args.all:
        logger.info("Starting Multi-Cloud Audit...")
        
        # Ejecución Azure
        try:
            AzureAudit().run()
        except Exception as e:
            logger.error(f"Azure Audit failed: {e}")

        # Ejecución AWS
        try:
            AWSAudit().run()
        except Exception as e:
            logger.error(f"AWS Audit failed: {e}")

        # Ejecución GCP
        try:
            GCPAudit().run()
        except Exception as e:
            logger.error(f"GCP Audit failed: {e}")

if __name__ == "__main__":
    main()
