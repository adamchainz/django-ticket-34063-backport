import django
import patchy
from django import test

if django.VERSION < (4, 2):
    # Backport of https://code.djangoproject.com/ticket/34063
    from django.test.client import AsyncClientHandler
    patchy.patch(
        AsyncClientHandler.__call__,
        """\
        @@ -14,7 +14,8 @@
                 sender=self.__class__, scope=scope
             )
             request_started.connect(close_old_connections)
        -    request = ASGIRequest(scope, body_file)
        +    from django.core.handlers.wsgi import LimitedStream
        +    request = ASGIRequest(scope, LimitedStream(body_file, len(body_file)))
             # Sneaky little hack so that we can easily get round
             # CsrfViewMiddleware. This makes life easier, and is probably required
             # for backwards compatibility with external tests against admin views.
        """
    )


class IndexTests(test.TestCase):
    async def test_post(self):
        await self.async_client.post("/")
