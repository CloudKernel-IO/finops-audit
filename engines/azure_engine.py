"""Azure audit engine placeholder."""

import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import SubscriptionClient

logger = logging.getLogger(__name__)

class AzureAudit:
    def __init__(self):
        self.credential = DefaultAzureCredential()

    def run(self):
        sub_client = SubscriptionClient(self.credential)
        
        for sub in sub_client.subscriptions.list():
            print(f"\n--- Scanning Azure Subscription: {sub.display_name} ---")
            subscription_id = sub.subscription_id
            
            # 1. Auditoría de Discos Huérfanos
            self.audit_disks(subscription_id)
            
            # 2. Auditoría de IPs Públicas no asociadas
            self.audit_public_ips(subscription_id)

    def audit_disks(self, subscription_id):
        compute_client = ComputeManagementClient(self.credential, subscription_id)
        disks = compute_client.disks.list()
        for disk in disks:
            # En Azure, si 'managed_by' es None, el disco no está enganchado a ninguna VM
            if disk.managed_by is None:
                print(f"[!] Unattached Disk: {disk.name} | Size: {disk.disk_size_gb}GB | Tier: {disk.sku.name}")

    def audit_public_ips(self, subscription_id):
        network_client = NetworkManagementClient(self.credential, subscription_id)
        ips = network_client.public_ip_addresses.list_all()
        for ip in ips:
            # Si no tiene 'ip_configuration', la IP está reservada pero no se usa (y se cobra)
            if ip.ip_configuration is None:
                print(f"[!] Idle Public IP: {ip.name} | Address: {ip.ip_address} | Location: {ip.location}")
