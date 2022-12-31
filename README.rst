Examples of backporting the fix from `#34063 <https://code.djangoproject.com/ticket/34063>`__.

Reproduce issue on first commit with ``./manage.py test``.
Use one of the methods from the later commits to backport the fix in your project.

On the first commit you’ll see the failure:

.. code-block:: sh

    $ ./manage.py test
    Found 1 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    F
    ======================================================================
    FAIL: test_post (example.tests.IndexTests.test_post)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/.../.venv/lib/python3.11/site-packages/asgiref/sync.py", line 240, in __call__
        return call_result.result()
               ^^^^^^^^^^^^^^^^^^^^
      File "/.../lib/python3.11/concurrent/futures/_base.py", line 449, in result
        return self.__get_result()
               ^^^^^^^^^^^^^^^^^^^
      File "/.../lib/python3.11/concurrent/futures/_base.py", line 401, in __get_result
        raise self._exception
      File "/.../.venv/lib/python3.11/site-packages/asgiref/sync.py", line 306, in main_wrap
        result = await self.awaitable(*args, **kwargs)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/.../example/tests.py", line 6, in test_post
        await self.async_client.post("/")
      File "/.../.venv/lib/python3.11/site-packages/django/test/client.py", line 1069, in request
        self.check_exception(response)
      File "/.../.venv/lib/python3.11/site-packages/django/test/client.py", line 663, in check_exception
        raise exc_value
      File "/.../.venv/lib/python3.11/site-packages/asgiref/sync.py", line 486, in thread_handler
        raise exc_info[1]
      File "/.../.venv/lib/python3.11/site-packages/django/core/handlers/exception.py", line 42, in inner
        response = await get_response(request)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/asgiref/sync.py", line 486, in thread_handler
        raise exc_info[1]
      File "/.../.venv/lib/python3.11/site-packages/django/core/handlers/base.py", line 253, in _get_response_async
        response = await wrapped_callback(
                   ^^^^^^^^^^^^^^^^^^^^^^^
      File "/.../example/views.py", line 5, in index
        if "x" in request.POST:
                  ^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/core/handlers/asgi.py", line 113, in _get_post
        self._load_post_and_files()
      File "/.../.venv/lib/python3.11/site-packages/django/http/request.py", line 369, in _load_post_and_files
        self._post, self._files = self.parse_file_upload(self.META, data)
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/http/request.py", line 319, in parse_file_upload
        return parser.parse()
               ^^^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/http/multipartparser.py", line 165, in parse
        for item_type, meta_data, field_stream in Parser(stream, self._boundary):
      File "/.../.venv/lib/python3.11/site-packages/django/http/multipartparser.py", line 709, in __iter__
        for sub_stream in boundarystream:
      File "/.../.venv/lib/python3.11/site-packages/django/http/multipartparser.py", line 533, in __next__
        return LazyStream(BoundaryIter(self._stream, self._boundary))
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/http/multipartparser.py", line 560, in __init__
        unused_char = self._stream.read(1)
                      ^^^^^^^^^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/http/multipartparser.py", line 427, in read
        return b"".join(parts())
               ^^^^^^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/http/multipartparser.py", line 418, in parts
        chunk = next(self)
                ^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/http/multipartparser.py", line 440, in __next__
        output = next(self._producer)
                 ^^^^^^^^^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/http/multipartparser.py", line 507, in __next__
        data = self.flo.read(self.chunk_size)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/http/request.py", line 404, in read
        return self._stream.read(*args, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/.../.venv/lib/python3.11/site-packages/django/test/client.py", line 82, in read
        assert (
    AssertionError: Cannot read more than the available bytes from the HTTP incoming data.

    ----------------------------------------------------------------------
    Ran 1 test in 0.011s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

On the later commits, you’ll see the test run succeed:

.. code-block:: sh

    $ ./manage.py test
    Found 1 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.002s

    OK
    Destroying test database for alias 'default'...

🤗
