// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:srv/PathNav.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__PATH_NAV__TRAITS_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__PATH_NAV__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/srv/detail/path_nav__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'path'
#include "nav_msgs/msg/detail/path__traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const PathNav_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: path
  {
    out << "path: ";
    to_flow_style_yaml(msg.path, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PathNav_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "path:\n";
    to_block_style_yaml(msg.path, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PathNav_Request & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::PathNav_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::PathNav_Request & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::PathNav_Request>()
{
  return "aid_robot_msgs::srv::PathNav_Request";
}

template<>
inline const char * name<aid_robot_msgs::srv::PathNav_Request>()
{
  return "aid_robot_msgs/srv/PathNav_Request";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::PathNav_Request>
  : std::integral_constant<bool, has_fixed_size<nav_msgs::msg::Path>::value> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::PathNav_Request>
  : std::integral_constant<bool, has_bounded_size<nav_msgs::msg::Path>::value> {};

template<>
struct is_message<aid_robot_msgs::srv::PathNav_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const PathNav_Response & msg,
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
  const PathNav_Response & msg,
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

inline std::string to_yaml(const PathNav_Response & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::PathNav_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::PathNav_Response & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::PathNav_Response>()
{
  return "aid_robot_msgs::srv::PathNav_Response";
}

template<>
inline const char * name<aid_robot_msgs::srv::PathNav_Response>()
{
  return "aid_robot_msgs/srv/PathNav_Response";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::PathNav_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::PathNav_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::PathNav_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aid_robot_msgs::srv::PathNav>()
{
  return "aid_robot_msgs::srv::PathNav";
}

template<>
inline const char * name<aid_robot_msgs::srv::PathNav>()
{
  return "aid_robot_msgs/srv/PathNav";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::PathNav>
  : std::integral_constant<
    bool,
    has_fixed_size<aid_robot_msgs::srv::PathNav_Request>::value &&
    has_fixed_size<aid_robot_msgs::srv::PathNav_Response>::value
  >
{
};

template<>
struct has_bounded_size<aid_robot_msgs::srv::PathNav>
  : std::integral_constant<
    bool,
    has_bounded_size<aid_robot_msgs::srv::PathNav_Request>::value &&
    has_bounded_size<aid_robot_msgs::srv::PathNav_Response>::value
  >
{
};

template<>
struct is_service<aid_robot_msgs::srv::PathNav>
  : std::true_type
{
};

template<>
struct is_service_request<aid_robot_msgs::srv::PathNav_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aid_robot_msgs::srv::PathNav_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__PATH_NAV__TRAITS_HPP_
