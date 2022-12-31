import django
from django import test

if django.VERSION < (4, 2):
    # Backport of https://code.djangoproject.com/ticket/34063
    from django.core.handlers.wsgi import LimitedStream
    from django.test.client import AsyncClient, AsyncClientHandler

    class FixedAsyncClientHandler(AsyncClientHandler):
        async def get_response_async(self, request):
            request._stream = LimitedStream(
                request._stream,
                len(request._stream),
            )
            return await super().get_response_async(request)

    class FixedAsyncClient(AsyncClient):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.handler.__class__ = FixedAsyncClientHandler


class TestCase(test.TestCase):
    if django.VERSION < (4, 2):
        async_client_class = FixedAsyncClient


class IndexTests(TestCase):
    async def test_post(self):
        await self.async_client.post("/")
