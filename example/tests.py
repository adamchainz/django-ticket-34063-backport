from django import test


class IndexTests(test.TestCase):
    async def test_post(self):
        await self.async_client.post("/")
