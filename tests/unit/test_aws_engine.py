from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from engines.aws_engine import AWSAudit


def test_get_regions_returns_regions():
    mock_ec2_client = MagicMock()
    mock_ec2_client.describe_regions.return_value = {
        "Regions": [
            {"RegionName": "us-east-1"},
            {"RegionName": "eu-west-1"},
        ]
    }

    with patch("engines.aws_engine.boto3.client", return_value=mock_ec2_client):
        audit = AWSAudit()
        assert audit.get_regions() == ["us-east-1", "eu-west-1"]


def test_run_reports_unused_resources(capsys):
    mock_ec2_client = MagicMock()
    mock_regional_client = MagicMock()
    mock_regional_client.describe_addresses.return_value = {
        "Addresses": [
            {"PublicIp": "203.0.113.10", "AllocationId": "eipalloc-123"}
        ]
    }

    volume = SimpleNamespace(id="vol-123", size=50, volume_type="gp3")
    volumes = MagicMock()
    volumes.filter.return_value = [volume]

    mock_ec2_resource = MagicMock()
    mock_ec2_resource.volumes = volumes

    with patch("engines.aws_engine.boto3.client", side_effect=[mock_ec2_client, mock_regional_client]), \
        patch("engines.aws_engine.boto3.resource", return_value=mock_ec2_resource), \
        patch.object(AWSAudit, "get_regions", return_value=["us-east-1"]):
        audit = AWSAudit()
        audit.run()

    output = capsys.readouterr().out
    assert "Unused EBS Volume: vol-123" in output
    assert "Idle Elastic IP: 203.0.113.10" in output
