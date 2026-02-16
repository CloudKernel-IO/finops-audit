from types import SimpleNamespace
from unittest.mock import MagicMock, patch


from engines.azure_engine import AzureAudit


def test_run_calls_audit_for_each_subscription():
    subscription = SimpleNamespace(display_name="TestSub", subscription_id="sub-123")
    mock_sub_client = MagicMock()
    mock_sub_client.subscriptions.list.return_value = [subscription]

    with patch("engines.azure_engine.SubscriptionClient", return_value=mock_sub_client), \
        patch("engines.azure_engine.DefaultAzureCredential"):
        audit = AzureAudit()
        with patch.object(audit, "audit_disks") as mock_disks, \
            patch.object(audit, "audit_public_ips") as mock_ips:
            audit.run()

    mock_disks.assert_called_once_with("sub-123")
    mock_ips.assert_called_once_with("sub-123")


def test_audit_disks_reports_unattached(capsys):
    disk = SimpleNamespace(
        name="disk-1",
        disk_size_gb=128,
        sku=SimpleNamespace(name="Standard_LRS"),
        managed_by=None,
    )
    mock_compute_client = MagicMock()
    mock_compute_client.disks.list.return_value = [disk]

    with patch("engines.azure_engine.ComputeManagementClient", return_value=mock_compute_client), \
        patch("engines.azure_engine.DefaultAzureCredential"):
        audit = AzureAudit()
        audit.audit_disks("sub-123")

    output = capsys.readouterr().out
    assert "Unattached Disk: disk-1" in output


def test_audit_public_ips_reports_idle(capsys):
    ip = SimpleNamespace(
        name="ip-1",
        ip_address="198.51.100.10",
        location="westeurope",
        ip_configuration=None,
    )
    mock_network_client = MagicMock()
    mock_network_client.public_ip_addresses.list_all.return_value = [ip]

    with patch("engines.azure_engine.NetworkManagementClient", return_value=mock_network_client), \
        patch("engines.azure_engine.DefaultAzureCredential"):
        audit = AzureAudit()
        audit.audit_public_ips("sub-123")

    output = capsys.readouterr().out
    assert "Idle Public IP: ip-1" in output
