import os


import pytest
from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient

pytestmark = pytest.mark.integration


def test_azure_can_list_subscriptions():
    if os.getenv("RUN_AZURE_INTEGRATION") != "true":
        pytest.skip("RUN_AZURE_INTEGRATION is not enabled")

    credential = DefaultAzureCredential()
    sub_client = SubscriptionClient(credential)
    subscriptions = list(sub_client.subscriptions.list())
    assert isinstance(subscriptions, list)
