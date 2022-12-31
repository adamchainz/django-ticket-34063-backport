import django
from django import test

if django.VERSION < (4, 2):
    # Backport https://code.djangoproject.com/ticket/34063

    from django.core.handlers.wsgi import LimitedStream
    from django.test.client import AsyncClientHandler

    orig_get_response_async = AsyncClientHandler.get_response_async

    async def get_response_async(self, request):
        request._stream = LimitedStream(
            request._stream,
            len(request._stream),
        )
        return await orig_get_response_async(self, request)

    AsyncClientHandler.get_response_async = get_response_async


class IndexTests(test.TestCase):
    async def test_post(self):
        await self.async_client.post("/")
