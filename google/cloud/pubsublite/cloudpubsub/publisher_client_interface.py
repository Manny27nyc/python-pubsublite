from abc import abstractmethod
from concurrent.futures import Future
from typing import ContextManager, Mapping, Union, AsyncContextManager

from google.cloud.pubsublite.types import TopicPath


class AsyncPublisherClientInterface(AsyncContextManager):
    """
  An AsyncPublisherClientInterface publishes messages similar to Google Pub/Sub, but must be used in an
  async context. Any publish failures are permanent.

  Must be used in an `async with` block or have __aenter__() awaited before use.
  """

    @abstractmethod
    async def publish(
        self,
        topic: Union[TopicPath, str],
        data: bytes,
        ordering_key: str = "",
        **attrs: Mapping[str, str]
    ) -> str:
        """
    Publish a message.

    Args:
      topic: The topic to publish to. Publishes to new topics may have nontrivial startup latency.
      data: The bytestring payload of the message
      ordering_key: The key to enforce ordering on, or "" for no ordering.
      **attrs: Additional attributes to send.

    Returns:
      An ack id, which can be decoded using PublishMetadata.decode.

    Raises:
      GoogleApiCallError: On a permanent failure.
    """


class PublisherClientInterface(ContextManager):
    """
  A PublisherClientInterface publishes messages similar to Google Pub/Sub.

  Must be used in a `with` block or have __enter__() called before use.
  """

    @abstractmethod
    def publish(
        self,
        topic: Union[TopicPath, str],
        data: bytes,
        ordering_key: str = "",
        **attrs: Mapping[str, str]
    ) -> "Future[str]":
        """
    Publish a message.

    Args:
      topic: The topic to publish to. Publishes to new topics may have nontrivial startup latency.
      data: The bytestring payload of the message
      ordering_key: The key to enforce ordering on, or "" for no ordering.
      **attrs: Additional attributes to send.

    Returns:
      A future completed with an ack id, which can be decoded using PublishMetadata.decode.

    Raises:
      GoogleApiCallError: On a permanent failure.
    """
