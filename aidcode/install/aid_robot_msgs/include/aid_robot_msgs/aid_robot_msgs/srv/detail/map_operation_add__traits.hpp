// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:srv/MapOperationAdd.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__MAP_OPERATION_ADD__TRAITS_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__MAP_OPERATION_ADD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/srv/detail/map_operation_add__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MapOperationAdd_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: map_name
  {
    out << "map_name: ";
    rosidl_generator_traits::value_to_yaml(msg.map_name, out);
    out << ", ";
  }

  // member: map_file
  {
    out << "map_file: ";
    rosidl_generator_traits::value_to_yaml(msg.map_file, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MapOperationAdd_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: map_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "map_name: ";
    rosidl_generator_traits::value_to_yaml(msg.map_name, out);
    out << "\n";
  }

  // member: map_file
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "map_file: ";
    rosidl_generator_traits::value_to_yaml(msg.map_file, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MapOperationAdd_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace aid_robot_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aid_robot_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aid_robot_msgs::srv::MapOperationAdd_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::MapOperationAdd_Request & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::MapOperationAdd_Request>()
{
  return "aid_robot_msgs::srv::MapOperationAdd_Request";
}

template<>
inline const char * name<aid_robot_msgs::srv::MapOperationAdd_Request>()
{
  return "aid_robot_msgs/srv/MapOperationAdd_Request";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::MapOperationAdd_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::MapOperationAdd_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::MapOperationAdd_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MapOperationAdd_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MapOperationAdd_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MapOperationAdd_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace aid_robot_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aid_robot_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aid_robot_msgs::srv::MapOperationAdd_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::MapOperationAdd_Response & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::MapOperationAdd_Response>()
{
  return "aid_robot_msgs::srv::MapOperationAdd_Response";
}

template<>
inline const char * name<aid_robot_msgs::srv::MapOperationAdd_Response>()
{
  return "aid_robot_msgs/srv/MapOperationAdd_Response";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::MapOperationAdd_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::MapOperationAdd_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::MapOperationAdd_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aid_robot_msgs::srv::MapOperationAdd>()
{
  return "aid_robot_msgs::srv::MapOperationAdd";
}

template<>
inline const char * name<aid_robot_msgs::srv::MapOperationAdd>()
{
  return "aid_robot_msgs/srv/MapOperationAdd";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::MapOperationAdd>
  : std::integral_constant<
    bool,
    has_fixed_size<aid_robot_msgs::srv::MapOperationAdd_Request>::value &&
    has_fixed_size<aid_robot_msgs::srv::MapOperationAdd_Response>::value
  >
{
};

template<>
struct has_bounded_size<aid_robot_msgs::srv::MapOperationAdd>
  : std::integral_constant<
    bool,
    has_bounded_size<aid_robot_msgs::srv::MapOperationAdd_Request>::value &&
    has_bounded_size<aid_robot_msgs::srv::MapOperationAdd_Response>::value
  >
{
};

template<>
struct is_service<aid_robot_msgs::srv::MapOperationAdd>
  : std::true_type
{
};

template<>
struct is_service_request<aid_robot_msgs::srv::MapOperationAdd_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aid_robot_msgs::srv::MapOperationAdd_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__MAP_OPERATION_ADD__TRAITS_HPP_
