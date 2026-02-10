"""GCP audit engine placeholder."""

import logging
from google.cloud import compute_v1
from google.auth import default

logger = logging.getLogger(__name__)

class GCPAudit:
    def __init__(self):
        # Autenticación profesional: utiliza las credenciales del entorno
        self.credentials, self.project_id = default()
        self.disk_client = compute_v1.DisksClient()
        self.addr_client = compute_v1.AddressesClient()
        self.zone_client = compute_v1.ZonesClient()

    def get_all_zones(self):
        """Obtiene todas las zonas activas del proyecto para auditar discos"""
        zones = self.zone_client.list(project=self.project_id)
        return [zone.name for zone in zones]

    def audit_disks(self):
        """Detecta discos zonales que no tienen usuarios asociados"""
        print(f"\n--- GCP Project: {self.project_id} (Disks) ---")
        zones = self.get_all_zones()
        for zone in zones:
            disks = self.disk_client.list(project=self.project_id, zone=zone)
            for disk in disks:
                # Si la lista de usuarios (instancias) está vacía, el disco es huérfano
                if not disk.users:
                    print(f"[!] Orphaned Zonal Disk: {disk.name} in {zone} ({disk.size_gb}GB)")

    def audit_ips(self):
        """Detecta IPs estáticas externas con estado RESERVED (sin uso)"""
        print(f"\n--- GCP Project: {self.project_id} (Static IPs) ---")
        # GCP cobra por IPs estáticas reservadas que no están asignadas a un recurso
        request = compute_v1.AggregatedListAddressesRequest(project=self.project_id)
        agg_list = self.addr_client.aggregated_list(request=request)
        
        for region, response in agg_list:
            if response.addresses:
                for addr in response.addresses:
                    if addr.status == "RESERVED":
                        print(f"[!] Unused Static IP Found: {addr.address} in {region}")

    def run(self):
        try:
            self.audit_disks()
            self.audit_ips()
        except Exception as e:
            logger.error(f"Error during GCP Audit: {e}")
