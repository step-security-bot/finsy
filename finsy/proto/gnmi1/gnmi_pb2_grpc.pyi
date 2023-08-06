"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Package gNMI defines a service specification for the gRPC Network Management
Interface. This interface is defined to be a standard interface via which
a network management system ("client") can subscribe to state values,
retrieve snapshots of state information, and manipulate the state of a data
tree supported by a device ("target").

This document references the gNMI Specification which can be found at
http://github.com/openconfig/reference/blob/master/rpc/gnmi
"""
import abc
import collections.abc
from . import gnmi_pb2 as _dot_gnmi_pb2
import grpc
import grpc.aio
import typing

_T = typing.TypeVar('_T')

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta):
    ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore
    ...

class gNMIStub:
    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Capabilities: grpc.UnaryUnaryMultiCallable[
        _dot_gnmi_pb2.CapabilityRequest,
        _dot_gnmi_pb2.CapabilityResponse,
    ]
    """Capabilities allows the client to retrieve the set of capabilities that
    is supported by the target. This allows the target to validate the
    service version that is implemented and retrieve the set of models that
    the target supports. The models can then be specified in subsequent RPCs
    to restrict the set of data that is utilized.
    Reference: gNMI Specification Section 3.2
    """
    Get: grpc.UnaryUnaryMultiCallable[
        _dot_gnmi_pb2.GetRequest,
        _dot_gnmi_pb2.GetResponse,
    ]
    """Retrieve a snapshot of data from the target. A Get RPC requests that the
    target snapshots a subset of the data tree as specified by the paths
    included in the message and serializes this to be returned to the
    client using the specified encoding.
    Reference: gNMI Specification Section 3.3
    """
    Set: grpc.UnaryUnaryMultiCallable[
        _dot_gnmi_pb2.SetRequest,
        _dot_gnmi_pb2.SetResponse,
    ]
    """Set allows the client to modify the state of data on the target. The
    paths to modified along with the new values that the client wishes
    to set the value to.
    Reference: gNMI Specification Section 3.4
    """
    Subscribe: grpc.StreamStreamMultiCallable[
        _dot_gnmi_pb2.SubscribeRequest,
        _dot_gnmi_pb2.SubscribeResponse,
    ]
    """Subscribe allows a client to request the target to send it values
    of particular paths within the data tree. These values may be streamed
    at a particular cadence (STREAM), sent one off on a long-lived channel
    (POLL), or sent as a one-off retrieval (ONCE).
    Reference: gNMI Specification Section 3.5
    """

class gNMIAsyncStub:
    Capabilities: grpc.aio.UnaryUnaryMultiCallable[
        _dot_gnmi_pb2.CapabilityRequest,
        _dot_gnmi_pb2.CapabilityResponse,
    ]
    """Capabilities allows the client to retrieve the set of capabilities that
    is supported by the target. This allows the target to validate the
    service version that is implemented and retrieve the set of models that
    the target supports. The models can then be specified in subsequent RPCs
    to restrict the set of data that is utilized.
    Reference: gNMI Specification Section 3.2
    """
    Get: grpc.aio.UnaryUnaryMultiCallable[
        _dot_gnmi_pb2.GetRequest,
        _dot_gnmi_pb2.GetResponse,
    ]
    """Retrieve a snapshot of data from the target. A Get RPC requests that the
    target snapshots a subset of the data tree as specified by the paths
    included in the message and serializes this to be returned to the
    client using the specified encoding.
    Reference: gNMI Specification Section 3.3
    """
    Set: grpc.aio.UnaryUnaryMultiCallable[
        _dot_gnmi_pb2.SetRequest,
        _dot_gnmi_pb2.SetResponse,
    ]
    """Set allows the client to modify the state of data on the target. The
    paths to modified along with the new values that the client wishes
    to set the value to.
    Reference: gNMI Specification Section 3.4
    """
    Subscribe: grpc.aio.StreamStreamMultiCallable[
        _dot_gnmi_pb2.SubscribeRequest,
        _dot_gnmi_pb2.SubscribeResponse,
    ]
    """Subscribe allows a client to request the target to send it values
    of particular paths within the data tree. These values may be streamed
    at a particular cadence (STREAM), sent one off on a long-lived channel
    (POLL), or sent as a one-off retrieval (ONCE).
    Reference: gNMI Specification Section 3.5
    """

class gNMIServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def Capabilities(
        self,
        request: _dot_gnmi_pb2.CapabilityRequest,
        context: _ServicerContext,
    ) -> typing.Union[_dot_gnmi_pb2.CapabilityResponse, collections.abc.Awaitable[_dot_gnmi_pb2.CapabilityResponse]]:
        """Capabilities allows the client to retrieve the set of capabilities that
        is supported by the target. This allows the target to validate the
        service version that is implemented and retrieve the set of models that
        the target supports. The models can then be specified in subsequent RPCs
        to restrict the set of data that is utilized.
        Reference: gNMI Specification Section 3.2
        """
    @abc.abstractmethod
    def Get(
        self,
        request: _dot_gnmi_pb2.GetRequest,
        context: _ServicerContext,
    ) -> typing.Union[_dot_gnmi_pb2.GetResponse, collections.abc.Awaitable[_dot_gnmi_pb2.GetResponse]]:
        """Retrieve a snapshot of data from the target. A Get RPC requests that the
        target snapshots a subset of the data tree as specified by the paths
        included in the message and serializes this to be returned to the
        client using the specified encoding.
        Reference: gNMI Specification Section 3.3
        """
    @abc.abstractmethod
    def Set(
        self,
        request: _dot_gnmi_pb2.SetRequest,
        context: _ServicerContext,
    ) -> typing.Union[_dot_gnmi_pb2.SetResponse, collections.abc.Awaitable[_dot_gnmi_pb2.SetResponse]]:
        """Set allows the client to modify the state of data on the target. The
        paths to modified along with the new values that the client wishes
        to set the value to.
        Reference: gNMI Specification Section 3.4
        """
    @abc.abstractmethod
    def Subscribe(
        self,
        request_iterator: _MaybeAsyncIterator[_dot_gnmi_pb2.SubscribeRequest],
        context: _ServicerContext,
    ) -> typing.Union[collections.abc.Iterator[_dot_gnmi_pb2.SubscribeResponse], collections.abc.AsyncIterator[_dot_gnmi_pb2.SubscribeResponse]]:
        """Subscribe allows a client to request the target to send it values
        of particular paths within the data tree. These values may be streamed
        at a particular cadence (STREAM), sent one off on a long-lived channel
        (POLL), or sent as a one-off retrieval (ONCE).
        Reference: gNMI Specification Section 3.5
        """

def add_gNMIServicer_to_server(servicer: gNMIServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
