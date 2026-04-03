# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aid_robot_msgs:srv/GetCurrentMap.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GetCurrentMap_Request(type):
    """Metaclass of message 'GetCurrentMap_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('aid_robot_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'aid_robot_msgs.srv.GetCurrentMap_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_current_map__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_current_map__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_current_map__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_current_map__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_current_map__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetCurrentMap_Request(metaclass=Metaclass_GetCurrentMap_Request):
    """Message class 'GetCurrentMap_Request'."""

    __slots__ = [
    ]

    _fields_and_field_types = {
    }

    SLOT_TYPES = (
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


# Import statements for member types

import builtins  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_GetCurrentMap_Response(type):
    """Metaclass of message 'GetCurrentMap_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('aid_robot_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'aid_robot_msgs.srv.GetCurrentMap_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_current_map__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_current_map__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_current_map__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_current_map__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_current_map__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetCurrentMap_Response(metaclass=Metaclass_GetCurrentMap_Response):
    """Message class 'GetCurrentMap_Response'."""

    __slots__ = [
        '_success',
        '_map_id',
        '_map_file',
        '_map_name',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'map_id': 'uint32',
        'map_file': 'string',
        'map_name': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.map_id = kwargs.get('map_id', int())
        self.map_file = kwargs.get('map_file', str())
        self.map_name = kwargs.get('map_name', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.success != other.success:
            return False
        if self.map_id != other.map_id:
            return False
        if self.map_file != other.map_file:
            return False
        if self.map_name != other.map_name:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def map_id(self):
        """Message field 'map_id'."""
        return self._map_id

    @map_id.setter
    def map_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'map_id' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'map_id' field must be an unsigned integer in [0, 4294967295]"
        self._map_id = value

    @builtins.property
    def map_file(self):
        """Message field 'map_file'."""
        return self._map_file

    @map_file.setter
    def map_file(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'map_file' field must be of type 'str'"
        self._map_file = value

    @builtins.property
    def map_name(self):
        """Message field 'map_name'."""
        return self._map_name

    @map_name.setter
    def map_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'map_name' field must be of type 'str'"
        self._map_name = value


class Metaclass_GetCurrentMap(type):
    """Metaclass of service 'GetCurrentMap'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('aid_robot_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'aid_robot_msgs.srv.GetCurrentMap')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__get_current_map

            from aid_robot_msgs.srv import _get_current_map
            if _get_current_map.Metaclass_GetCurrentMap_Request._TYPE_SUPPORT is None:
                _get_current_map.Metaclass_GetCurrentMap_Request.__import_type_support__()
            if _get_current_map.Metaclass_GetCurrentMap_Response._TYPE_SUPPORT is None:
                _get_current_map.Metaclass_GetCurrentMap_Response.__import_type_support__()


class GetCurrentMap(metaclass=Metaclass_GetCurrentMap):
    from aid_robot_msgs.srv._get_current_map import GetCurrentMap_Request as Request
    from aid_robot_msgs.srv._get_current_map import GetCurrentMap_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
