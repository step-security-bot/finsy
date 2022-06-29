"Utility functions for protobuf messages."

# Copyright (c) 2022 Bill Fisher
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from typing import Type

import google.protobuf.json_format as json_format
import google.protobuf.text_format as text_format
import grpc
from google.protobuf.any_pb2 import Any as _Any
from google.protobuf.message import Message as _Message
from google.protobuf.reflection import GeneratedProtocolMessageType

import finsy
from finsy.gnmiclient import gNMIPath
from finsy.log import MSG_LOG
from finsy.proto import gnmi, p4r

PBAny = _Any
PBMessage = _Message


def from_text(data: str, msg_class: Type[PBMessage]):
    "Read protobuf message from given text/json string."
    assert isinstance(data, str)
    assert isinstance(msg_class, GeneratedProtocolMessageType)

    msg = msg_class()
    if data[0] == "{":
        json_format.Parse(data, msg)
    else:
        text_format.Parse(data, msg)

    return msg


def from_dict(value: dict, msg_class: Type[PBMessage]):
    "Convert Python dict to protobuf message."
    assert isinstance(msg_class, GeneratedProtocolMessageType)
    return json_format.ParseDict(value, msg_class())


def to_text(
    msg: PBMessage,
    *,
    as_one_line: bool = True,
    custom_format: bool = False,
) -> str:
    "Convert protobuf message to text format."
    assert isinstance(msg, PBMessage)
    formatter = _message_formatter if custom_format else None
    result = text_format.MessageToString(
        msg,
        as_one_line=as_one_line,
        message_formatter=formatter,
    )
    return result


def to_json(msg: PBMessage) -> str:
    "Convert protobuf message to JSON format."
    assert isinstance(msg, PBMessage), f"not a Message: {msg!r}"
    return json_format.MessageToJson(msg, preserving_proto_field_name=True)


def to_dict(msg: PBMessage) -> dict:
    "Convert protobuf message to Python dict."
    assert isinstance(msg, PBMessage), f"not a Message: {msg!r}"
    return json_format.MessageToDict(msg, preserving_proto_field_name=True)


def _message_formatter(msg, _indent, _as_one_line):
    if isinstance(msg, p4r.ForwardingPipelineConfig):
        return f"📦[p4cookie=0x{msg.cookie.cookie:x}]"
    if isinstance(msg, gnmi.Path):
        return f"📂{gNMIPath(msg)}"
    if isinstance(msg, gnmi.Update):
        value = repr(msg.val).strip()
        dups = "" if not msg.duplicates else f" ({msg.duplicates} dups)"
        return f"📂{gNMIPath(msg.path)} = {value}{dups}"
    if isinstance(msg, (p4r.PacketIn, p4r.PacketOut)):
        metadata = " ".join(
            f"meta[{md.metadata_id}]={md.value.hex()}" for md in msg.metadata
        )
        return f"📬{msg.payload.hex()} {metadata}"
    return None


def log_msg(
    state: grpc.ChannelConnectivity,
    msg: PBMessage,
    schema: "finsy.P4Schema | None",
):
    """Log a sent/received client message.

    Format:
        <state><mesg-type> (<size> bytes): <msg-contents>

    <state> is empty if the client state is READY. Otherwise, it's the
    channel connectivity state.
    """
    # Include the channel's state if it's not READY.
    state_name = ""
    if state != grpc.ChannelConnectivity.READY:
        state_name = f"{state.name} "  # trailing space necessary

    if isinstance(msg, (p4r.ReadResponse, p4r.WriteRequest)):
        text = to_text(msg, as_one_line=False, custom_format=True)
        if schema is not None:
            text = _log_annotate(text, schema)
    elif isinstance(msg, gnmi.GetResponse):
        text = to_text(msg, as_one_line=False, custom_format=True)
    else:
        text = to_text(msg, custom_format=True)

    size = msg.ByteSize()

    MSG_LOG.debug(
        "%s%s (%d bytes): %s",
        state_name,
        type(msg).__name__,
        size,
        text,
    )


_ANNOTATE_REGEX = re.compile(r"([a-z]+_id): (\d+)\n", re.MULTILINE)


def _log_annotate(text: str, schema: "finsy.P4Schema") -> str:
    "Annotate table_id, action_id, etc. in log messages."

    action_id = 0
    table_id = 0

    def _replace(m):
        nonlocal action_id, table_id

        key, value = m.groups()
        name = None

        try:
            match key:
                case "table_id":
                    table_id = int(value)
                    name = schema.tables[table_id].name
                case "action_id":
                    action_id = int(value)
                    name = schema.actions[action_id].name
                case "digest_id":
                    name = schema.digests[int(value)].name
                case "field_id":
                    name = schema.tables[table_id].match_fields[int(value)].name
                case "param_id":
                    name = schema.actions[action_id].params[int(value)].name
                # TODO: Annotate more identifier types.

        except (LookupError, ValueError):
            # If there is a failure, don't replace anything.
            pass

        if name:
            return f"{key}: {value}  # {name}\n"

        return m[0]

    return _ANNOTATE_REGEX.sub(_replace, text)
