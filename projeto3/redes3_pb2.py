# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: redes3.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='redes3.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0credes3.proto\"\x1a\n\x07\x43ommand\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\"\x1c\n\rListenRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x12\n\x03Log\x12\x0b\n\x03log\x18\x01 \x01(\t\"\x06\n\x04Void2Q\n\x06Redes3\x12#\n\x0f\x65xecute_command\x12\x08.Command\x1a\x04.Log\"\x00\x12\"\n\x06listen\x12\x0e.ListenRequest\x1a\x04.Log\"\x00\x30\x01\x62\x06proto3')
)




_COMMAND = _descriptor.Descriptor(
  name='Command',
  full_name='Command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='Command.command', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=16,
  serialized_end=42,
)


_LISTENREQUEST = _descriptor.Descriptor(
  name='ListenRequest',
  full_name='ListenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ListenRequest.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=72,
)


_LOG = _descriptor.Descriptor(
  name='Log',
  full_name='Log',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='log', full_name='Log.log', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=74,
  serialized_end=92,
)


_VOID = _descriptor.Descriptor(
  name='Void',
  full_name='Void',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=100,
)

DESCRIPTOR.message_types_by_name['Command'] = _COMMAND
DESCRIPTOR.message_types_by_name['ListenRequest'] = _LISTENREQUEST
DESCRIPTOR.message_types_by_name['Log'] = _LOG
DESCRIPTOR.message_types_by_name['Void'] = _VOID
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Command = _reflection.GeneratedProtocolMessageType('Command', (_message.Message,), dict(
  DESCRIPTOR = _COMMAND,
  __module__ = 'redes3_pb2'
  # @@protoc_insertion_point(class_scope:Command)
  ))
_sym_db.RegisterMessage(Command)

ListenRequest = _reflection.GeneratedProtocolMessageType('ListenRequest', (_message.Message,), dict(
  DESCRIPTOR = _LISTENREQUEST,
  __module__ = 'redes3_pb2'
  # @@protoc_insertion_point(class_scope:ListenRequest)
  ))
_sym_db.RegisterMessage(ListenRequest)

Log = _reflection.GeneratedProtocolMessageType('Log', (_message.Message,), dict(
  DESCRIPTOR = _LOG,
  __module__ = 'redes3_pb2'
  # @@protoc_insertion_point(class_scope:Log)
  ))
_sym_db.RegisterMessage(Log)

Void = _reflection.GeneratedProtocolMessageType('Void', (_message.Message,), dict(
  DESCRIPTOR = _VOID,
  __module__ = 'redes3_pb2'
  # @@protoc_insertion_point(class_scope:Void)
  ))
_sym_db.RegisterMessage(Void)



_REDES3 = _descriptor.ServiceDescriptor(
  name='Redes3',
  full_name='Redes3',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=102,
  serialized_end=183,
  methods=[
  _descriptor.MethodDescriptor(
    name='execute_command',
    full_name='Redes3.execute_command',
    index=0,
    containing_service=None,
    input_type=_COMMAND,
    output_type=_LOG,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='listen',
    full_name='Redes3.listen',
    index=1,
    containing_service=None,
    input_type=_LISTENREQUEST,
    output_type=_LOG,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_REDES3)

DESCRIPTOR.services_by_name['Redes3'] = _REDES3

# @@protoc_insertion_point(module_scope)