# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gnmi1/gnmi.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2
from gnmi1 import gnmi_ext_pb2 as gnmi1_dot_gnmi__ext__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10gnmi1/gnmi.proto\x12\x04gnmi\x1a\x19google/protobuf/any.proto\x1a google/protobuf/descriptor.proto\x1a\x14gnmi1/gnmi_ext.proto\"\x94\x01\n\x0cNotification\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\x1a\n\x06prefix\x18\x02 \x01(\x0b\x32\n.gnmi.Path\x12\x1c\n\x06update\x18\x04 \x03(\x0b\x32\x0c.gnmi.Update\x12\x1a\n\x06\x64\x65lete\x18\x05 \x03(\x0b\x32\n.gnmi.Path\x12\x0e\n\x06\x61tomic\x18\x06 \x01(\x08J\x04\x08\x03\x10\x04R\x05\x61lias\"u\n\x06Update\x12\x18\n\x04path\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12\x1e\n\x05value\x18\x02 \x01(\x0b\x32\x0b.gnmi.ValueB\x02\x18\x01\x12\x1d\n\x03val\x18\x03 \x01(\x0b\x32\x10.gnmi.TypedValue\x12\x12\n\nduplicates\x18\x04 \x01(\r\"\x83\x03\n\nTypedValue\x12\x14\n\nstring_val\x18\x01 \x01(\tH\x00\x12\x11\n\x07int_val\x18\x02 \x01(\x03H\x00\x12\x12\n\x08uint_val\x18\x03 \x01(\x04H\x00\x12\x12\n\x08\x62ool_val\x18\x04 \x01(\x08H\x00\x12\x13\n\tbytes_val\x18\x05 \x01(\x0cH\x00\x12\x17\n\tfloat_val\x18\x06 \x01(\x02\x42\x02\x18\x01H\x00\x12\x14\n\ndouble_val\x18\x0e \x01(\x01H\x00\x12*\n\x0b\x64\x65\x63imal_val\x18\x07 \x01(\x0b\x32\x0f.gnmi.Decimal64B\x02\x18\x01H\x00\x12)\n\x0cleaflist_val\x18\x08 \x01(\x0b\x32\x11.gnmi.ScalarArrayH\x00\x12\'\n\x07\x61ny_val\x18\t \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x12\x12\n\x08json_val\x18\n \x01(\x0cH\x00\x12\x17\n\rjson_ietf_val\x18\x0b \x01(\x0cH\x00\x12\x13\n\tascii_val\x18\x0c \x01(\tH\x00\x12\x15\n\x0bproto_bytes\x18\r \x01(\x0cH\x00\x42\x07\n\x05value\"Y\n\x04Path\x12\x13\n\x07\x65lement\x18\x01 \x03(\tB\x02\x18\x01\x12\x0e\n\x06origin\x18\x02 \x01(\t\x12\x1c\n\x04\x65lem\x18\x03 \x03(\x0b\x32\x0e.gnmi.PathElem\x12\x0e\n\x06target\x18\x04 \x01(\t\"j\n\x08PathElem\x12\x0c\n\x04name\x18\x01 \x01(\t\x12$\n\x03key\x18\x02 \x03(\x0b\x32\x17.gnmi.PathElem.KeyEntry\x1a*\n\x08KeyEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"8\n\x05Value\x12\r\n\x05value\x18\x01 \x01(\x0c\x12\x1c\n\x04type\x18\x02 \x01(\x0e\x32\x0e.gnmi.Encoding:\x02\x18\x01\"N\n\x05\x45rror\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\"\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x14.google.protobuf.Any:\x02\x18\x01\"2\n\tDecimal64\x12\x0e\n\x06\x64igits\x18\x01 \x01(\x03\x12\x11\n\tprecision\x18\x02 \x01(\r:\x02\x18\x01\"0\n\x0bScalarArray\x12!\n\x07\x65lement\x18\x01 \x03(\x0b\x32\x10.gnmi.TypedValue\"\x9d\x01\n\x10SubscribeRequest\x12+\n\tsubscribe\x18\x01 \x01(\x0b\x32\x16.gnmi.SubscriptionListH\x00\x12\x1a\n\x04poll\x18\x03 \x01(\x0b\x32\n.gnmi.PollH\x00\x12&\n\textension\x18\x05 \x03(\x0b\x32\x13.gnmi_ext.ExtensionB\t\n\x07requestJ\x04\x08\x04\x10\x05R\x07\x61liases\"\x06\n\x04Poll\"\xa8\x01\n\x11SubscribeResponse\x12$\n\x06update\x18\x01 \x01(\x0b\x32\x12.gnmi.NotificationH\x00\x12\x17\n\rsync_response\x18\x03 \x01(\x08H\x00\x12 \n\x05\x65rror\x18\x04 \x01(\x0b\x32\x0b.gnmi.ErrorB\x02\x18\x01H\x00\x12&\n\textension\x18\x05 \x03(\x0b\x32\x13.gnmi_ext.ExtensionB\n\n\x08response\"\xd5\x02\n\x10SubscriptionList\x12\x1a\n\x06prefix\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12(\n\x0csubscription\x18\x02 \x03(\x0b\x32\x12.gnmi.Subscription\x12\x1d\n\x03qos\x18\x04 \x01(\x0b\x32\x10.gnmi.QOSMarking\x12)\n\x04mode\x18\x05 \x01(\x0e\x32\x1b.gnmi.SubscriptionList.Mode\x12\x19\n\x11\x61llow_aggregation\x18\x06 \x01(\x08\x12#\n\nuse_models\x18\x07 \x03(\x0b\x32\x0f.gnmi.ModelData\x12 \n\x08\x65ncoding\x18\x08 \x01(\x0e\x32\x0e.gnmi.Encoding\x12\x14\n\x0cupdates_only\x18\t \x01(\x08\"&\n\x04Mode\x12\n\n\x06STREAM\x10\x00\x12\x08\n\x04ONCE\x10\x01\x12\x08\n\x04POLL\x10\x02J\x04\x08\x03\x10\x04R\x0buse_aliases\"\x9f\x01\n\x0cSubscription\x12\x18\n\x04path\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12$\n\x04mode\x18\x02 \x01(\x0e\x32\x16.gnmi.SubscriptionMode\x12\x17\n\x0fsample_interval\x18\x03 \x01(\x04\x12\x1a\n\x12suppress_redundant\x18\x04 \x01(\x08\x12\x1a\n\x12heartbeat_interval\x18\x05 \x01(\x04\"\x1d\n\nQOSMarking\x12\x0f\n\x07marking\x18\x01 \x01(\r\"\xa9\x01\n\nSetRequest\x12\x1a\n\x06prefix\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12\x1a\n\x06\x64\x65lete\x18\x02 \x03(\x0b\x32\n.gnmi.Path\x12\x1d\n\x07replace\x18\x03 \x03(\x0b\x32\x0c.gnmi.Update\x12\x1c\n\x06update\x18\x04 \x03(\x0b\x32\x0c.gnmi.Update\x12&\n\textension\x18\x05 \x03(\x0b\x32\x13.gnmi_ext.Extension\"\xac\x01\n\x0bSetResponse\x12\x1a\n\x06prefix\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12$\n\x08response\x18\x02 \x03(\x0b\x32\x12.gnmi.UpdateResult\x12 \n\x07message\x18\x03 \x01(\x0b\x32\x0b.gnmi.ErrorB\x02\x18\x01\x12\x11\n\ttimestamp\x18\x04 \x01(\x03\x12&\n\textension\x18\x05 \x03(\x0b\x32\x13.gnmi_ext.Extension\"\xca\x01\n\x0cUpdateResult\x12\x15\n\ttimestamp\x18\x01 \x01(\x03\x42\x02\x18\x01\x12\x18\n\x04path\x18\x02 \x01(\x0b\x32\n.gnmi.Path\x12 \n\x07message\x18\x03 \x01(\x0b\x32\x0b.gnmi.ErrorB\x02\x18\x01\x12(\n\x02op\x18\x04 \x01(\x0e\x32\x1c.gnmi.UpdateResult.Operation\"=\n\tOperation\x12\x0b\n\x07INVALID\x10\x00\x12\n\n\x06\x44\x45LETE\x10\x01\x12\x0b\n\x07REPLACE\x10\x02\x12\n\n\x06UPDATE\x10\x03\"\x97\x02\n\nGetRequest\x12\x1a\n\x06prefix\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12\x18\n\x04path\x18\x02 \x03(\x0b\x32\n.gnmi.Path\x12\'\n\x04type\x18\x03 \x01(\x0e\x32\x19.gnmi.GetRequest.DataType\x12 \n\x08\x65ncoding\x18\x05 \x01(\x0e\x32\x0e.gnmi.Encoding\x12#\n\nuse_models\x18\x06 \x03(\x0b\x32\x0f.gnmi.ModelData\x12&\n\textension\x18\x07 \x03(\x0b\x32\x13.gnmi_ext.Extension\";\n\x08\x44\x61taType\x12\x07\n\x03\x41LL\x10\x00\x12\n\n\x06\x43ONFIG\x10\x01\x12\t\n\x05STATE\x10\x02\x12\x0f\n\x0bOPERATIONAL\x10\x03\"\x7f\n\x0bGetResponse\x12(\n\x0cnotification\x18\x01 \x03(\x0b\x32\x12.gnmi.Notification\x12\x1e\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x0b.gnmi.ErrorB\x02\x18\x01\x12&\n\textension\x18\x03 \x03(\x0b\x32\x13.gnmi_ext.Extension\";\n\x11\x43\x61pabilityRequest\x12&\n\textension\x18\x01 \x03(\x0b\x32\x13.gnmi_ext.Extension\"\xaa\x01\n\x12\x43\x61pabilityResponse\x12)\n\x10supported_models\x18\x01 \x03(\x0b\x32\x0f.gnmi.ModelData\x12+\n\x13supported_encodings\x18\x02 \x03(\x0e\x32\x0e.gnmi.Encoding\x12\x14\n\x0cgNMI_version\x18\x03 \x01(\t\x12&\n\textension\x18\x04 \x03(\x0b\x32\x13.gnmi_ext.Extension\"@\n\tModelData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0corganization\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t*D\n\x08\x45ncoding\x12\x08\n\x04JSON\x10\x00\x12\t\n\x05\x42YTES\x10\x01\x12\t\n\x05PROTO\x10\x02\x12\t\n\x05\x41SCII\x10\x03\x12\r\n\tJSON_IETF\x10\x04*A\n\x10SubscriptionMode\x12\x12\n\x0eTARGET_DEFINED\x10\x00\x12\r\n\tON_CHANGE\x10\x01\x12\n\n\x06SAMPLE\x10\x02\x32\xe3\x01\n\x04gNMI\x12\x41\n\x0c\x43\x61pabilities\x12\x17.gnmi.CapabilityRequest\x1a\x18.gnmi.CapabilityResponse\x12*\n\x03Get\x12\x10.gnmi.GetRequest\x1a\x11.gnmi.GetResponse\x12*\n\x03Set\x12\x10.gnmi.SetRequest\x1a\x11.gnmi.SetResponse\x12@\n\tSubscribe\x12\x16.gnmi.SubscribeRequest\x1a\x17.gnmi.SubscribeResponse(\x01\x30\x01:3\n\x0cgnmi_service\x12\x1c.google.protobuf.FileOptions\x18\xe9\x07 \x01(\tBS\n\x15\x63om.github.gnmi.protoB\tGnmiProtoP\x01Z%github.com/openconfig/gnmi/proto/gnmi\xca>\x05\x30.8.0b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gnmi1.gnmi_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.FileOptions.RegisterExtension(gnmi_service)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\025com.github.gnmi.protoB\tGnmiProtoP\001Z%github.com/openconfig/gnmi/proto/gnmi\312>\0050.8.0'
  _UPDATE.fields_by_name['value']._options = None
  _UPDATE.fields_by_name['value']._serialized_options = b'\030\001'
  _TYPEDVALUE.fields_by_name['float_val']._options = None
  _TYPEDVALUE.fields_by_name['float_val']._serialized_options = b'\030\001'
  _TYPEDVALUE.fields_by_name['decimal_val']._options = None
  _TYPEDVALUE.fields_by_name['decimal_val']._serialized_options = b'\030\001'
  _PATH.fields_by_name['element']._options = None
  _PATH.fields_by_name['element']._serialized_options = b'\030\001'
  _PATHELEM_KEYENTRY._options = None
  _PATHELEM_KEYENTRY._serialized_options = b'8\001'
  _VALUE._options = None
  _VALUE._serialized_options = b'\030\001'
  _ERROR._options = None
  _ERROR._serialized_options = b'\030\001'
  _DECIMAL64._options = None
  _DECIMAL64._serialized_options = b'\030\001'
  _SUBSCRIBERESPONSE.fields_by_name['error']._options = None
  _SUBSCRIBERESPONSE.fields_by_name['error']._serialized_options = b'\030\001'
  _SETRESPONSE.fields_by_name['message']._options = None
  _SETRESPONSE.fields_by_name['message']._serialized_options = b'\030\001'
  _UPDATERESULT.fields_by_name['timestamp']._options = None
  _UPDATERESULT.fields_by_name['timestamp']._serialized_options = b'\030\001'
  _UPDATERESULT.fields_by_name['message']._options = None
  _UPDATERESULT.fields_by_name['message']._serialized_options = b'\030\001'
  _GETRESPONSE.fields_by_name['error']._options = None
  _GETRESPONSE.fields_by_name['error']._serialized_options = b'\030\001'
  _ENCODING._serialized_start=3347
  _ENCODING._serialized_end=3415
  _SUBSCRIPTIONMODE._serialized_start=3417
  _SUBSCRIPTIONMODE._serialized_end=3482
  _NOTIFICATION._serialized_start=110
  _NOTIFICATION._serialized_end=258
  _UPDATE._serialized_start=260
  _UPDATE._serialized_end=377
  _TYPEDVALUE._serialized_start=380
  _TYPEDVALUE._serialized_end=767
  _PATH._serialized_start=769
  _PATH._serialized_end=858
  _PATHELEM._serialized_start=860
  _PATHELEM._serialized_end=966
  _PATHELEM_KEYENTRY._serialized_start=924
  _PATHELEM_KEYENTRY._serialized_end=966
  _VALUE._serialized_start=968
  _VALUE._serialized_end=1024
  _ERROR._serialized_start=1026
  _ERROR._serialized_end=1104
  _DECIMAL64._serialized_start=1106
  _DECIMAL64._serialized_end=1156
  _SCALARARRAY._serialized_start=1158
  _SCALARARRAY._serialized_end=1206
  _SUBSCRIBEREQUEST._serialized_start=1209
  _SUBSCRIBEREQUEST._serialized_end=1366
  _POLL._serialized_start=1368
  _POLL._serialized_end=1374
  _SUBSCRIBERESPONSE._serialized_start=1377
  _SUBSCRIBERESPONSE._serialized_end=1545
  _SUBSCRIPTIONLIST._serialized_start=1548
  _SUBSCRIPTIONLIST._serialized_end=1889
  _SUBSCRIPTIONLIST_MODE._serialized_start=1832
  _SUBSCRIPTIONLIST_MODE._serialized_end=1870
  _SUBSCRIPTION._serialized_start=1892
  _SUBSCRIPTION._serialized_end=2051
  _QOSMARKING._serialized_start=2053
  _QOSMARKING._serialized_end=2082
  _SETREQUEST._serialized_start=2085
  _SETREQUEST._serialized_end=2254
  _SETRESPONSE._serialized_start=2257
  _SETRESPONSE._serialized_end=2429
  _UPDATERESULT._serialized_start=2432
  _UPDATERESULT._serialized_end=2634
  _UPDATERESULT_OPERATION._serialized_start=2573
  _UPDATERESULT_OPERATION._serialized_end=2634
  _GETREQUEST._serialized_start=2637
  _GETREQUEST._serialized_end=2916
  _GETREQUEST_DATATYPE._serialized_start=2857
  _GETREQUEST_DATATYPE._serialized_end=2916
  _GETRESPONSE._serialized_start=2918
  _GETRESPONSE._serialized_end=3045
  _CAPABILITYREQUEST._serialized_start=3047
  _CAPABILITYREQUEST._serialized_end=3106
  _CAPABILITYRESPONSE._serialized_start=3109
  _CAPABILITYRESPONSE._serialized_end=3279
  _MODELDATA._serialized_start=3281
  _MODELDATA._serialized_end=3345
  _GNMI._serialized_start=3485
  _GNMI._serialized_end=3712
# @@protoc_insertion_point(module_scope)
