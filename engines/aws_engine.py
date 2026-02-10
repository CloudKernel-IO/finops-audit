"""AWS audit engine placeholder."""

import boto3
import logging

logger = logging.getLogger(__name__)

class AWSAudit:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')

    def get_regions(self):
        """Obtiene solo las regiones habilitadas para la cuenta"""
        regions = self.ec2_client.describe_regions()
        return [region['RegionName'] for region in regions['Regions']]

    def run(self):
        regions = self.get_regions()
        
        for region in regions:
            print(f"\n--- Scanning AWS Region: {region} ---")
            ec2 = boto3.resource('ec2', region_name=region)
            client = boto3.client('ec2', region_name=region)

            # 1. Auditoría de Volúmenes EBS (Status: available significa que no está in-use)
            volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
            for vol in volumes:
                print(f"[!] Unused EBS Volume: {vol.id} | Size: {vol.size}GB | Type: {vol.volume_type}")

            # 2. Auditoría de Elastic IPs (EIPs)
            # AWS cobra por EIPs que NO están asociadas a una instancia en ejecución
            addresses = client.describe_addresses()
            for addr in addresses['Addresses']:
                if 'InstanceId' not in addr and 'NetworkInterfaceId' not in addr:
                    print(f"[!] Idle Elastic IP: {addr['PublicIp']} | AllocationId: {addr['AllocationId']}")
