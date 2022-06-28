"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _ExtensionID:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _ExtensionIDEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ExtensionID.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    EID_UNSET: _ExtensionID.ValueType  # 0
    """New extensions are to be defined within this enumeration - their definition
    MUST link to a reference describing their implementation.
    """

    EID_EXPERIMENTAL: _ExtensionID.ValueType  # 999
    """An experimental extension that may be used during prototyping of a new
    extension.
    """

class ExtensionID(_ExtensionID, metaclass=_ExtensionIDEnumTypeWrapper):
    """RegisteredExtension is an enumeration acting as a registry for extensions
    defined by external sources.
    """
    pass

EID_UNSET: ExtensionID.ValueType  # 0
"""New extensions are to be defined within this enumeration - their definition
MUST link to a reference describing their implementation.
"""

EID_EXPERIMENTAL: ExtensionID.ValueType  # 999
"""An experimental extension that may be used during prototyping of a new
extension.
"""

global___ExtensionID = ExtensionID


class Extension(google.protobuf.message.Message):
    """The Extension message contains a single gNMI extension."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    REGISTERED_EXT_FIELD_NUMBER: builtins.int
    MASTER_ARBITRATION_FIELD_NUMBER: builtins.int
    HISTORY_FIELD_NUMBER: builtins.int
    @property
    def registered_ext(self) -> global___RegisteredExtension:
        """A registered extension."""
        pass
    @property
    def master_arbitration(self) -> global___MasterArbitration:
        """Well known extensions.
        Master arbitration extension.
        """
        pass
    @property
    def history(self) -> global___History:
        """History extension."""
        pass
    def __init__(self,
        *,
        registered_ext: typing.Optional[global___RegisteredExtension] = ...,
        master_arbitration: typing.Optional[global___MasterArbitration] = ...,
        history: typing.Optional[global___History] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["ext",b"ext","history",b"history","master_arbitration",b"master_arbitration","registered_ext",b"registered_ext"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ext",b"ext","history",b"history","master_arbitration",b"master_arbitration","registered_ext",b"registered_ext"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["ext",b"ext"]) -> typing.Optional[typing_extensions.Literal["registered_ext","master_arbitration","history"]]: ...
global___Extension = Extension

class RegisteredExtension(google.protobuf.message.Message):
    """The RegisteredExtension message defines an extension which is defined outside
    of this file.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ID_FIELD_NUMBER: builtins.int
    MSG_FIELD_NUMBER: builtins.int
    id: global___ExtensionID.ValueType
    """The unique ID assigned to this extension."""

    msg: builtins.bytes
    """The binary-marshalled protobuf extension payload."""

    def __init__(self,
        *,
        id: global___ExtensionID.ValueType = ...,
        msg: builtins.bytes = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["id",b"id","msg",b"msg"]) -> None: ...
global___RegisteredExtension = RegisteredExtension

class MasterArbitration(google.protobuf.message.Message):
    """MasterArbitration is used to select the master among multiple gNMI clients
    with the same Roles. The client with the largest election_id is honored as
    the master.
    The document about gNMI master arbitration can be found at
    https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-master-arbitration.md
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ROLE_FIELD_NUMBER: builtins.int
    ELECTION_ID_FIELD_NUMBER: builtins.int
    @property
    def role(self) -> global___Role: ...
    @property
    def election_id(self) -> global___Uint128: ...
    def __init__(self,
        *,
        role: typing.Optional[global___Role] = ...,
        election_id: typing.Optional[global___Uint128] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["election_id",b"election_id","role",b"role"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["election_id",b"election_id","role",b"role"]) -> None: ...
global___MasterArbitration = MasterArbitration

class Uint128(google.protobuf.message.Message):
    """Representation of unsigned 128-bit integer."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    HIGH_FIELD_NUMBER: builtins.int
    LOW_FIELD_NUMBER: builtins.int
    high: builtins.int
    low: builtins.int
    def __init__(self,
        *,
        high: builtins.int = ...,
        low: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["high",b"high","low",b"low"]) -> None: ...
global___Uint128 = Uint128

class Role(google.protobuf.message.Message):
    """There can be one master for each role. The role is identified by its id."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ID_FIELD_NUMBER: builtins.int
    id: typing.Text
    """More fields can be added if needed, for example, to specify what paths the
    role can read/write.
    """

    def __init__(self,
        *,
        id: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["id",b"id"]) -> None: ...
global___Role = Role

class History(google.protobuf.message.Message):
    """The History extension allows clients to request historical data. Its
    spec can be found at
    https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-history.md
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SNAPSHOT_TIME_FIELD_NUMBER: builtins.int
    RANGE_FIELD_NUMBER: builtins.int
    snapshot_time: builtins.int
    """Nanoseconds since the epoch"""

    @property
    def range(self) -> global___TimeRange: ...
    def __init__(self,
        *,
        snapshot_time: builtins.int = ...,
        range: typing.Optional[global___TimeRange] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["range",b"range","request",b"request","snapshot_time",b"snapshot_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["range",b"range","request",b"request","snapshot_time",b"snapshot_time"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["request",b"request"]) -> typing.Optional[typing_extensions.Literal["snapshot_time","range"]]: ...
global___History = History

class TimeRange(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    START_FIELD_NUMBER: builtins.int
    END_FIELD_NUMBER: builtins.int
    start: builtins.int
    """Nanoseconds since the epoch"""

    end: builtins.int
    """Nanoseconds since the epoch"""

    def __init__(self,
        *,
        start: builtins.int = ...,
        end: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["end",b"end","start",b"start"]) -> None: ...
global___TimeRange = TimeRange
