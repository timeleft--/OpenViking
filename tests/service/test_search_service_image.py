import pytest

from openviking.server.identity import RequestContext, Role
from openviking.service.search_service import SearchService
from openviking.utils.model_retry import effective_max_retries
from openviking_cli.session.user_id import UserIdentifier


class FakeVikingFS:
    def __init__(self):
        self.image_url = None
        self.retry_values = []

    async def read_file_bytes(self, uri, ctx=None):
        assert uri == "viking://resources/cat.png"
        return b"\x89PNG\r\n\x1a\n"

    async def find(self, **kwargs):
        self.image_url = kwargs["image_url"]
        self.retry_values.append(effective_max_retries(3))
        return {"ok": True}

    async def search(self, **kwargs):
        self.retry_values.append(effective_max_retries(3))
        return {"ok": True}


@pytest.mark.asyncio
async def test_search_service_resolves_viking_image_url_to_data_uri():
    fs = FakeVikingFS()
    service = SearchService(fs)
    ctx = RequestContext(user=UserIdentifier("acc", "user"), role=Role.USER)

    result = await service.find(
        query="",
        image_url="viking://resources/cat.png",
        ctx=ctx,
    )

    assert result == {"ok": True}
    assert fs.image_url.startswith("data:image/png;base64,")


@pytest.mark.asyncio
async def test_search_and_find_disable_model_retries_for_the_call():
    fs = FakeVikingFS()
    service = SearchService(fs)
    ctx = RequestContext(user=UserIdentifier("acc", "user"), role=Role.USER)

    await service.find(query="find", ctx=ctx)
    await service.search(query="search", ctx=ctx)

    assert fs.retry_values == [0, 0]
    assert effective_max_retries(3) == 3
