# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file_storage.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="file_storage.proto",
    package="aea.mobix.file_storage.v0_1_0",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x12\x66ile_storage.proto\x12\x1d\x61\x65\x61.mobix.file_storage.v0_1_0"\xbf\x08\n\x12\x46ileStorageMessage\x12Q\n\x03\x65nd\x18\x05 \x01(\x0b\x32\x42.aea.mobix.file_storage.v0_1_0.FileStorageMessage.End_PerformativeH\x00\x12U\n\x05\x65rror\x18\x06 \x01(\x0b\x32\x44.aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_PerformativeH\x00\x12\x65\n\rfile_download\x18\x07 \x01(\x0b\x32L.aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Download_PerformativeH\x00\x12\x61\n\x0b\x66ile_upload\x18\x08 \x01(\x0b\x32J.aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Upload_PerformativeH\x00\x1a\xeb\x01\n\tErrorCode\x12]\n\nerror_code\x18\x01 \x01(\x0e\x32I.aea.mobix.file_storage.v0_1_0.FileStorageMessage.ErrorCode.ErrorCodeEnum"\x7f\n\rErrorCodeEnum\x12\x18\n\x14UNSUPPORTED_PROTOCOL\x10\x00\x12\x12\n\x0e\x44\x45\x43ODING_ERROR\x10\x01\x12\x13\n\x0fINVALID_MESSAGE\x10\x02\x12\x15\n\x11UNSUPPORTED_SKILL\x10\x03\x12\x14\n\x10INVALID_DIALOGUE\x10\x04\x1aJ\n\x18\x46ile_Upload_Performative\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\x0c\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\x1a\x41\n\x1a\x46ile_Download_Performative\x12\x12\n\naccess_url\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\x1a\x93\x02\n\x12\x45rror_Performative\x12O\n\nerror_code\x18\x01 \x01(\x0b\x32;.aea.mobix.file_storage.v0_1_0.FileStorageMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12g\n\nerror_data\x18\x03 \x03(\x0b\x32S.aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative.ErrorDataEntry\x1a\x30\n\x0e\x45rrorDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x02\x38\x01\x1a\x12\n\x10\x45nd_PerformativeB\x0e\n\x0cperformativeb\x06proto3'
    ),
)


_FILESTORAGEMESSAGE_ERRORCODE_ERRORCODEENUM = _descriptor.EnumDescriptor(
    name="ErrorCodeEnum",
    full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.ErrorCode.ErrorCodeEnum",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="UNSUPPORTED_PROTOCOL",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="DECODING_ERROR", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="INVALID_MESSAGE",
            index=2,
            number=2,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="UNSUPPORTED_SKILL",
            index=3,
            number=3,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="INVALID_DIALOGUE",
            index=4,
            number=4,
            serialized_options=None,
            type=None,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=557,
    serialized_end=684,
)
_sym_db.RegisterEnumDescriptor(_FILESTORAGEMESSAGE_ERRORCODE_ERRORCODEENUM)


_FILESTORAGEMESSAGE_ERRORCODE = _descriptor.Descriptor(
    name="ErrorCode",
    full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.ErrorCode",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="error_code",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.ErrorCode.error_code",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[_FILESTORAGEMESSAGE_ERRORCODE_ERRORCODEENUM,],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=449,
    serialized_end=684,
)

_FILESTORAGEMESSAGE_FILE_UPLOAD_PERFORMATIVE = _descriptor.Descriptor(
    name="File_Upload_Performative",
    full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Upload_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="content",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Upload_Performative.content",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="filename",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Upload_Performative.filename",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="key",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Upload_Performative.key",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=686,
    serialized_end=760,
)

_FILESTORAGEMESSAGE_FILE_DOWNLOAD_PERFORMATIVE = _descriptor.Descriptor(
    name="File_Download_Performative",
    full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Download_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="access_url",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Download_Performative.access_url",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="content",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Download_Performative.content",
            index=1,
            number=2,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=762,
    serialized_end=827,
)

_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY = _descriptor.Descriptor(
    name="ErrorDataEntry",
    full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative.ErrorDataEntry",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="key",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative.ErrorDataEntry.key",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative.ErrorDataEntry.value",
            index=1,
            number=2,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=_b("8\001"),
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1057,
    serialized_end=1105,
)

_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE = _descriptor.Descriptor(
    name="Error_Performative",
    full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="error_code",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative.error_code",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="error_msg",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative.error_msg",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="error_data",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative.error_data",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY,],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=830,
    serialized_end=1105,
)

_FILESTORAGEMESSAGE_END_PERFORMATIVE = _descriptor.Descriptor(
    name="End_Performative",
    full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.End_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1107,
    serialized_end=1125,
)

_FILESTORAGEMESSAGE = _descriptor.Descriptor(
    name="FileStorageMessage",
    full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="end",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.end",
            index=0,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="error",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.error",
            index=1,
            number=6,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="file_download",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.file_download",
            index=2,
            number=7,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="file_upload",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.file_upload",
            index=3,
            number=8,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[
        _FILESTORAGEMESSAGE_ERRORCODE,
        _FILESTORAGEMESSAGE_FILE_UPLOAD_PERFORMATIVE,
        _FILESTORAGEMESSAGE_FILE_DOWNLOAD_PERFORMATIVE,
        _FILESTORAGEMESSAGE_ERROR_PERFORMATIVE,
        _FILESTORAGEMESSAGE_END_PERFORMATIVE,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="performative",
            full_name="aea.mobix.file_storage.v0_1_0.FileStorageMessage.performative",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=54,
    serialized_end=1141,
)

_FILESTORAGEMESSAGE_ERRORCODE.fields_by_name[
    "error_code"
].enum_type = _FILESTORAGEMESSAGE_ERRORCODE_ERRORCODEENUM
_FILESTORAGEMESSAGE_ERRORCODE.containing_type = _FILESTORAGEMESSAGE
_FILESTORAGEMESSAGE_ERRORCODE_ERRORCODEENUM.containing_type = (
    _FILESTORAGEMESSAGE_ERRORCODE
)
_FILESTORAGEMESSAGE_FILE_UPLOAD_PERFORMATIVE.containing_type = _FILESTORAGEMESSAGE
_FILESTORAGEMESSAGE_FILE_DOWNLOAD_PERFORMATIVE.containing_type = _FILESTORAGEMESSAGE
_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY.containing_type = (
    _FILESTORAGEMESSAGE_ERROR_PERFORMATIVE
)
_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE.fields_by_name[
    "error_code"
].message_type = _FILESTORAGEMESSAGE_ERRORCODE
_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE.fields_by_name[
    "error_data"
].message_type = _FILESTORAGEMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY
_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE.containing_type = _FILESTORAGEMESSAGE
_FILESTORAGEMESSAGE_END_PERFORMATIVE.containing_type = _FILESTORAGEMESSAGE
_FILESTORAGEMESSAGE.fields_by_name[
    "end"
].message_type = _FILESTORAGEMESSAGE_END_PERFORMATIVE
_FILESTORAGEMESSAGE.fields_by_name[
    "error"
].message_type = _FILESTORAGEMESSAGE_ERROR_PERFORMATIVE
_FILESTORAGEMESSAGE.fields_by_name[
    "file_download"
].message_type = _FILESTORAGEMESSAGE_FILE_DOWNLOAD_PERFORMATIVE
_FILESTORAGEMESSAGE.fields_by_name[
    "file_upload"
].message_type = _FILESTORAGEMESSAGE_FILE_UPLOAD_PERFORMATIVE
_FILESTORAGEMESSAGE.oneofs_by_name["performative"].fields.append(
    _FILESTORAGEMESSAGE.fields_by_name["end"]
)
_FILESTORAGEMESSAGE.fields_by_name[
    "end"
].containing_oneof = _FILESTORAGEMESSAGE.oneofs_by_name["performative"]
_FILESTORAGEMESSAGE.oneofs_by_name["performative"].fields.append(
    _FILESTORAGEMESSAGE.fields_by_name["error"]
)
_FILESTORAGEMESSAGE.fields_by_name[
    "error"
].containing_oneof = _FILESTORAGEMESSAGE.oneofs_by_name["performative"]
_FILESTORAGEMESSAGE.oneofs_by_name["performative"].fields.append(
    _FILESTORAGEMESSAGE.fields_by_name["file_download"]
)
_FILESTORAGEMESSAGE.fields_by_name[
    "file_download"
].containing_oneof = _FILESTORAGEMESSAGE.oneofs_by_name["performative"]
_FILESTORAGEMESSAGE.oneofs_by_name["performative"].fields.append(
    _FILESTORAGEMESSAGE.fields_by_name["file_upload"]
)
_FILESTORAGEMESSAGE.fields_by_name[
    "file_upload"
].containing_oneof = _FILESTORAGEMESSAGE.oneofs_by_name["performative"]
DESCRIPTOR.message_types_by_name["FileStorageMessage"] = _FILESTORAGEMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FileStorageMessage = _reflection.GeneratedProtocolMessageType(
    "FileStorageMessage",
    (_message.Message,),
    dict(
        ErrorCode=_reflection.GeneratedProtocolMessageType(
            "ErrorCode",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FILESTORAGEMESSAGE_ERRORCODE,
                __module__="file_storage_pb2"
                # @@protoc_insertion_point(class_scope:aea.mobix.file_storage.v0_1_0.FileStorageMessage.ErrorCode)
            ),
        ),
        File_Upload_Performative=_reflection.GeneratedProtocolMessageType(
            "File_Upload_Performative",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FILESTORAGEMESSAGE_FILE_UPLOAD_PERFORMATIVE,
                __module__="file_storage_pb2"
                # @@protoc_insertion_point(class_scope:aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Upload_Performative)
            ),
        ),
        File_Download_Performative=_reflection.GeneratedProtocolMessageType(
            "File_Download_Performative",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FILESTORAGEMESSAGE_FILE_DOWNLOAD_PERFORMATIVE,
                __module__="file_storage_pb2"
                # @@protoc_insertion_point(class_scope:aea.mobix.file_storage.v0_1_0.FileStorageMessage.File_Download_Performative)
            ),
        ),
        Error_Performative=_reflection.GeneratedProtocolMessageType(
            "Error_Performative",
            (_message.Message,),
            dict(
                ErrorDataEntry=_reflection.GeneratedProtocolMessageType(
                    "ErrorDataEntry",
                    (_message.Message,),
                    dict(
                        DESCRIPTOR=_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY,
                        __module__="file_storage_pb2"
                        # @@protoc_insertion_point(class_scope:aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative.ErrorDataEntry)
                    ),
                ),
                DESCRIPTOR=_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE,
                __module__="file_storage_pb2"
                # @@protoc_insertion_point(class_scope:aea.mobix.file_storage.v0_1_0.FileStorageMessage.Error_Performative)
            ),
        ),
        End_Performative=_reflection.GeneratedProtocolMessageType(
            "End_Performative",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FILESTORAGEMESSAGE_END_PERFORMATIVE,
                __module__="file_storage_pb2"
                # @@protoc_insertion_point(class_scope:aea.mobix.file_storage.v0_1_0.FileStorageMessage.End_Performative)
            ),
        ),
        DESCRIPTOR=_FILESTORAGEMESSAGE,
        __module__="file_storage_pb2"
        # @@protoc_insertion_point(class_scope:aea.mobix.file_storage.v0_1_0.FileStorageMessage)
    ),
)
_sym_db.RegisterMessage(FileStorageMessage)
_sym_db.RegisterMessage(FileStorageMessage.ErrorCode)
_sym_db.RegisterMessage(FileStorageMessage.File_Upload_Performative)
_sym_db.RegisterMessage(FileStorageMessage.File_Download_Performative)
_sym_db.RegisterMessage(FileStorageMessage.Error_Performative)
_sym_db.RegisterMessage(FileStorageMessage.Error_Performative.ErrorDataEntry)
_sym_db.RegisterMessage(FileStorageMessage.End_Performative)


_FILESTORAGEMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY._options = None
# @@protoc_insertion_point(module_scope)
