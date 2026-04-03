# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aid_robot_msgs:srv/DrawPicture.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_DrawPicture_Request(type):
    """Metaclass of message 'DrawPicture_Request'."""

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
                'aid_robot_msgs.srv.DrawPicture_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__draw_picture__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__draw_picture__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__draw_picture__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__draw_picture__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__draw_picture__request

            from aid_robot_msgs.msg import Rectangle
            if Rectangle.__class__._TYPE_SUPPORT is None:
                Rectangle.__class__.__import_type_support__()

            from aid_robot_msgs.msg import StartToEndPoint
            if StartToEndPoint.__class__._TYPE_SUPPORT is None:
                StartToEndPoint.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class DrawPicture_Request(metaclass=Metaclass_DrawPicture_Request):
    """Message class 'DrawPicture_Request'."""

    __slots__ = [
        '_frame_id',
        '_type',
        '_map_id',
        '_data',
        '_rectangle_array',
    ]

    _fields_and_field_types = {
        'frame_id': 'string',
        'type': 'string',
        'map_id': 'uint32',
        'data': 'sequence<aid_robot_msgs/StartToEndPoint>',
        'rectangle_array': 'sequence<aid_robot_msgs/Rectangle>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['aid_robot_msgs', 'msg'], 'StartToEndPoint')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['aid_robot_msgs', 'msg'], 'Rectangle')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.frame_id = kwargs.get('frame_id', str())
        self.type = kwargs.get('type', str())
        self.map_id = kwargs.get('map_id', int())
        self.data = kwargs.get('data', [])
        self.rectangle_array = kwargs.get('rectangle_array', [])

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
        if self.frame_id != other.frame_id:
            return False
        if self.type != other.type:
            return False
        if self.map_id != other.map_id:
            return False
        if self.data != other.data:
            return False
        if self.rectangle_array != other.rectangle_array:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def frame_id(self):
        """Message field 'frame_id'."""
        return self._frame_id

    @frame_id.setter
    def frame_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'frame_id' field must be of type 'str'"
        self._frame_id = value

    @builtins.property  # noqa: A003
    def type(self):  # noqa: A003
        """Message field 'type'."""
        return self._type

    @type.setter  # noqa: A003
    def type(self, value):  # noqa: A003
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'type' field must be of type 'str'"
        self._type = value

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
    def data(self):
        """Message field 'data'."""
        return self._data

    @data.setter
    def data(self, value):
        if __debug__:
            from aid_robot_msgs.msg import StartToEndPoint
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, StartToEndPoint) for v in value) and
                 True), \
                "The 'data' field must be a set or sequence and each value of type 'StartToEndPoint'"
        self._data = value

    @builtins.property
    def rectangle_array(self):
        """Message field 'rectangle_array'."""
        return self._rectangle_array

    @rectangle_array.setter
    def rectangle_array(self, value):
        if __debug__:
            from aid_robot_msgs.msg import Rectangle
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, Rectangle) for v in value) and
                 True), \
                "The 'rectangle_array' field must be a set or sequence and each value of type 'Rectangle'"
        self._rectangle_array = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_DrawPicture_Response(type):
    """Metaclass of message 'DrawPicture_Response'."""

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
                'aid_robot_msgs.srv.DrawPicture_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__draw_picture__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__draw_picture__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__draw_picture__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__draw_picture__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__draw_picture__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class DrawPicture_Response(metaclass=Metaclass_DrawPicture_Response):
    """Message class 'DrawPicture_Response'."""

    __slots__ = [
        '_success',
        '_message',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'message': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.message = kwargs.get('message', str())

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
        if self.message != other.message:
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
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'message' field must be of type 'str'"
        self._message = value


class Metaclass_DrawPicture(type):
    """Metaclass of service 'DrawPicture'."""

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
                'aid_robot_msgs.srv.DrawPicture')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__draw_picture

            from aid_robot_msgs.srv import _draw_picture
            if _draw_picture.Metaclass_DrawPicture_Request._TYPE_SUPPORT is None:
                _draw_picture.Metaclass_DrawPicture_Request.__import_type_support__()
            if _draw_picture.Metaclass_DrawPicture_Response._TYPE_SUPPORT is None:
                _draw_picture.Metaclass_DrawPicture_Response.__import_type_support__()


class DrawPicture(metaclass=Metaclass_DrawPicture):
    from aid_robot_msgs.srv._draw_picture import DrawPicture_Request as Request
    from aid_robot_msgs.srv._draw_picture import DrawPicture_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
