import asyncio

import pytest
from google.api_core.exceptions import InternalServerError
from google.cloud.pubsublite.internal.wire.gapic_connection import GapicConnection
from google.cloud.pubsublite.testing.test_utils import async_iterable

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_read_error_fails():
  conn = GapicConnection[int, int]()
  conn.set_response_it(async_iterable([InternalServerError("abc")]))
  with pytest.raises(InternalServerError):
    await conn.read()
  with pytest.raises(InternalServerError):
    await conn.read()
  with pytest.raises(InternalServerError):
    await conn.write(3)


async def test_read_success():
  conn = GapicConnection[int, int]()
  conn.set_response_it(async_iterable([3, 4, 5]))
  assert [await conn.read() for _ in range(3)] == [3, 4, 5]


async def test_writes():
  conn = GapicConnection[int, int]()
  conn.set_response_it(async_iterable([]))
  task1 = asyncio.ensure_future(conn.write(1))
  task2 = asyncio.ensure_future(conn.write(2))
  assert not task1.done()
  assert not task2.done()
  assert await conn.__anext__() == 1
  await task1
  assert not task2.done()
  assert await conn.__anext__() == 2
  await task2
