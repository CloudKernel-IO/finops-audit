from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from engines.gcp_engine import GCPAudit


def test_get_all_zones_returns_names():
    zone = SimpleNamespace(name="us-central1-a")
    mock_zone_client = MagicMock()
    mock_zone_client.list.return_value = [zone]

    with patch("engines.gcp_engine.default", return_value=(MagicMock(), "proj-123")), \
        patch("engines.gcp_engine.compute_v1.DisksClient"), \
        patch("engines.gcp_engine.compute_v1.AddressesClient"), \
        patch("engines.gcp_engine.compute_v1.ZonesClient", return_value=mock_zone_client):
        audit = GCPAudit()
        assert audit.get_all_zones() == ["us-central1-a"]


def test_audit_disks_reports_orphaned(capsys):
    zone = SimpleNamespace(name="us-central1-a")
    disk = SimpleNamespace(name="disk-1", size_gb=200, users=[])

    mock_zone_client = MagicMock()
    mock_zone_client.list.return_value = [zone]

    mock_disk_client = MagicMock()
    mock_disk_client.list.return_value = [disk]

    with patch("engines.gcp_engine.default", return_value=(MagicMock(), "proj-123")), \
        patch("engines.gcp_engine.compute_v1.DisksClient", return_value=mock_disk_client), \
        patch("engines.gcp_engine.compute_v1.AddressesClient"), \
        patch("engines.gcp_engine.compute_v1.ZonesClient", return_value=mock_zone_client):
        audit = GCPAudit()
        audit.audit_disks()

    output = capsys.readouterr().out
    assert "Orphaned Zonal Disk: disk-1" in output


def test_audit_ips_reports_reserved(capsys):
    response = SimpleNamespace(
        addresses=[
            SimpleNamespace(status="RESERVED", address="203.0.113.20"),
            SimpleNamespace(status="IN_USE", address="203.0.113.21"),
        ]
    )
    agg_list = [("regions/us-central1", response)]

    mock_addr_client = MagicMock()
    mock_addr_client.aggregated_list.return_value = agg_list

    with patch("engines.gcp_engine.default", return_value=(MagicMock(), "proj-123")), \
        patch("engines.gcp_engine.compute_v1.DisksClient"), \
        patch("engines.gcp_engine.compute_v1.AddressesClient", return_value=mock_addr_client), \
        patch("engines.gcp_engine.compute_v1.ZonesClient"):
        audit = GCPAudit()
        audit.audit_ips()

    output = capsys.readouterr().out
    assert "Unused Static IP Found: 203.0.113.20" in output
