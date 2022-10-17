"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
This package and its contents are a work-in-progress."""
import abc
import collections.abc
import grpc
import p4.v1.p4runtime_pb2

class P4RuntimeStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    Write: grpc.UnaryUnaryMultiCallable[
        p4.v1.p4runtime_pb2.WriteRequest,
        p4.v1.p4runtime_pb2.WriteResponse,
    ]
    """Update one or more P4 entities on the target."""
    Read: grpc.UnaryStreamMultiCallable[
        p4.v1.p4runtime_pb2.ReadRequest,
        p4.v1.p4runtime_pb2.ReadResponse,
    ]
    """Read one or more P4 entities from the target."""
    SetForwardingPipelineConfig: grpc.UnaryUnaryMultiCallable[
        p4.v1.p4runtime_pb2.SetForwardingPipelineConfigRequest,
        p4.v1.p4runtime_pb2.SetForwardingPipelineConfigResponse,
    ]
    """Sets the P4 forwarding-pipeline config."""
    GetForwardingPipelineConfig: grpc.UnaryUnaryMultiCallable[
        p4.v1.p4runtime_pb2.GetForwardingPipelineConfigRequest,
        p4.v1.p4runtime_pb2.GetForwardingPipelineConfigResponse,
    ]
    """Gets the current P4 forwarding-pipeline config."""
    StreamChannel: grpc.StreamStreamMultiCallable[
        p4.v1.p4runtime_pb2.StreamMessageRequest,
        p4.v1.p4runtime_pb2.StreamMessageResponse,
    ]
    """Represents the bidirectional stream between the controller and the
    switch (initiated by the controller), and is managed for the following
    purposes:
    - connection initiation through client arbitration
    - indicating switch session liveness: the session is live when switch
      sends a positive client arbitration update to the controller, and is
      considered dead when either the stream breaks or the switch sends a
      negative update for client arbitration
    - the controller sending/receiving packets to/from the switch
    - streaming of notifications from the switch
    """
    Capabilities: grpc.UnaryUnaryMultiCallable[
        p4.v1.p4runtime_pb2.CapabilitiesRequest,
        p4.v1.p4runtime_pb2.CapabilitiesResponse,
    ]

class P4RuntimeServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def Write(
        self,
        request: p4.v1.p4runtime_pb2.WriteRequest,
        context: grpc.ServicerContext,
    ) -> p4.v1.p4runtime_pb2.WriteResponse:
        """Update one or more P4 entities on the target."""
    @abc.abstractmethod
    def Read(
        self,
        request: p4.v1.p4runtime_pb2.ReadRequest,
        context: grpc.ServicerContext,
    ) -> collections.abc.Iterator[p4.v1.p4runtime_pb2.ReadResponse]:
        """Read one or more P4 entities from the target."""
    @abc.abstractmethod
    def SetForwardingPipelineConfig(
        self,
        request: p4.v1.p4runtime_pb2.SetForwardingPipelineConfigRequest,
        context: grpc.ServicerContext,
    ) -> p4.v1.p4runtime_pb2.SetForwardingPipelineConfigResponse:
        """Sets the P4 forwarding-pipeline config."""
    @abc.abstractmethod
    def GetForwardingPipelineConfig(
        self,
        request: p4.v1.p4runtime_pb2.GetForwardingPipelineConfigRequest,
        context: grpc.ServicerContext,
    ) -> p4.v1.p4runtime_pb2.GetForwardingPipelineConfigResponse:
        """Gets the current P4 forwarding-pipeline config."""
    @abc.abstractmethod
    def StreamChannel(
        self,
        request_iterator: collections.abc.Iterator[p4.v1.p4runtime_pb2.StreamMessageRequest],
        context: grpc.ServicerContext,
    ) -> collections.abc.Iterator[p4.v1.p4runtime_pb2.StreamMessageResponse]:
        """Represents the bidirectional stream between the controller and the
        switch (initiated by the controller), and is managed for the following
        purposes:
        - connection initiation through client arbitration
        - indicating switch session liveness: the session is live when switch
          sends a positive client arbitration update to the controller, and is
          considered dead when either the stream breaks or the switch sends a
          negative update for client arbitration
        - the controller sending/receiving packets to/from the switch
        - streaming of notifications from the switch
        """
    @abc.abstractmethod
    def Capabilities(
        self,
        request: p4.v1.p4runtime_pb2.CapabilitiesRequest,
        context: grpc.ServicerContext,
    ) -> p4.v1.p4runtime_pb2.CapabilitiesResponse: ...

def add_P4RuntimeServicer_to_server(servicer: P4RuntimeServicer, server: grpc.Server) -> None: ...
