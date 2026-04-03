# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aid_robot_msgs:srv/FindBestVelocity.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_FindBestVelocity_Request(type):
    """Metaclass of message 'FindBestVelocity_Request'."""

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
                'aid_robot_msgs.srv.FindBestVelocity_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__find_best_velocity__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__find_best_velocity__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__find_best_velocity__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__find_best_velocity__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__find_best_velocity__request

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FindBestVelocity_Request(metaclass=Metaclass_FindBestVelocity_Request):
    """Message class 'FindBestVelocity_Request'."""

    __slots__ = [
        '_header',
        '_max_angular_velocity',
        '_max_speed',
        '_len',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'max_angular_velocity': 'float',
        'max_speed': 'float',
        'len': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.max_angular_velocity = kwargs.get('max_angular_velocity', float())
        self.max_speed = kwargs.get('max_speed', float())
        self.len = kwargs.get('len', float())

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
        if self.header != other.header:
            return False
        if self.max_angular_velocity != other.max_angular_velocity:
            return False
        if self.max_speed != other.max_speed:
            return False
        if self.len != other.len:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def max_angular_velocity(self):
        """Message field 'max_angular_velocity'."""
        return self._max_angular_velocity

    @max_angular_velocity.setter
    def max_angular_velocity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'max_angular_velocity' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'max_angular_velocity' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._max_angular_velocity = value

    @builtins.property
    def max_speed(self):
        """Message field 'max_speed'."""
        return self._max_speed

    @max_speed.setter
    def max_speed(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'max_speed' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'max_speed' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._max_speed = value

    @builtins.property  # noqa: A003
    def len(self):  # noqa: A003
        """Message field 'len'."""
        return self._len

    @len.setter  # noqa: A003
    def len(self, value):  # noqa: A003
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'len' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'len' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._len = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_FindBestVelocity_Response(type):
    """Metaclass of message 'FindBestVelocity_Response'."""

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
                'aid_robot_msgs.srv.FindBestVelocity_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__find_best_velocity__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__find_best_velocity__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__find_best_velocity__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__find_best_velocity__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__find_best_velocity__response

            from geometry_msgs.msg import Twist
            if Twist.__class__._TYPE_SUPPORT is None:
                Twist.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FindBestVelocity_Response(metaclass=Metaclass_FindBestVelocity_Response):
    """Message class 'FindBestVelocity_Response'."""

    __slots__ = [
        '_cmd_vel',
        '_success',
        '_msg',
    ]

    _fields_and_field_types = {
        'cmd_vel': 'geometry_msgs/Twist',
        'success': 'boolean',
        'msg': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from geometry_msgs.msg import Twist
        self.cmd_vel = kwargs.get('cmd_vel', Twist())
        self.success = kwargs.get('success', bool())
        self.msg = kwargs.get('msg', str())

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
        if self.cmd_vel != other.cmd_vel:
            return False
        if self.success != other.success:
            return False
        if self.msg != other.msg:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def cmd_vel(self):
        """Message field 'cmd_vel'."""
        return self._cmd_vel

    @cmd_vel.setter
    def cmd_vel(self, value):
        if __debug__:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'cmd_vel' field must be a sub message of type 'Twist'"
        self._cmd_vel = value

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
    def msg(self):
        """Message field 'msg'."""
        return self._msg

    @msg.setter
    def msg(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'msg' field must be of type 'str'"
        self._msg = value


class Metaclass_FindBestVelocity(type):
    """Metaclass of service 'FindBestVelocity'."""

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
                'aid_robot_msgs.srv.FindBestVelocity')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__find_best_velocity

            from aid_robot_msgs.srv import _find_best_velocity
            if _find_best_velocity.Metaclass_FindBestVelocity_Request._TYPE_SUPPORT is None:
                _find_best_velocity.Metaclass_FindBestVelocity_Request.__import_type_support__()
            if _find_best_velocity.Metaclass_FindBestVelocity_Response._TYPE_SUPPORT is None:
                _find_best_velocity.Metaclass_FindBestVelocity_Response.__import_type_support__()


class FindBestVelocity(metaclass=Metaclass_FindBestVelocity):
    from aid_robot_msgs.srv._find_best_velocity import FindBestVelocity_Request as Request
    from aid_robot_msgs.srv._find_best_velocity import FindBestVelocity_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
