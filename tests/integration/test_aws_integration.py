import os

import pytest

from engines.aws_engine import AWSAudit

pytestmark = pytest.mark.integration


def test_aws_credentials_work():
    if os.getenv("RUN_AWS_INTEGRATION") != "true":
        pytest.skip("RUN_AWS_INTEGRATION is not enabled")

    audit = AWSAudit()
    regions = audit.get_regions()
    assert isinstance(regions, list)
