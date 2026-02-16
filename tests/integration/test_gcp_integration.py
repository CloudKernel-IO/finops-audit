import os

import pytest
from google.auth import default
from google.cloud import compute_v1

pytestmark = pytest.mark.integration


def test_gcp_can_list_zones():
    if os.getenv("RUN_GCP_INTEGRATION") != "true":
        pytest.skip("RUN_GCP_INTEGRATION is not enabled")

    credentials, project_id = default()
    zone_client = compute_v1.ZonesClient(credentials=credentials)
    zones = list(zone_client.list(project=project_id))
    assert isinstance(zones, list)
