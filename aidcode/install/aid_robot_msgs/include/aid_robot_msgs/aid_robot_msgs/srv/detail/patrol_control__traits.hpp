// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:srv/PatrolControl.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__PATROL_CONTROL__TRAITS_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__PATROL_CONTROL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/srv/detail/patrol_control__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const PatrolControl_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: cmd
  {
    out << "cmd: ";
    rosidl_generator_traits::value_to_yaml(msg.cmd, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PatrolControl_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: cmd
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cmd: ";
    rosidl_generator_traits::value_to_yaml(msg.cmd, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PatrolControl_Request & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::PatrolControl_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::PatrolControl_Request & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::PatrolControl_Request>()
{
  return "aid_robot_msgs::srv::PatrolControl_Request";
}

template<>
inline const char * name<aid_robot_msgs::srv::PatrolControl_Request>()
{
  return "aid_robot_msgs/srv/PatrolControl_Request";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::PatrolControl_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::PatrolControl_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::PatrolControl_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const PatrolControl_Response & msg,
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
  const PatrolControl_Response & msg,
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

inline std::string to_yaml(const PatrolControl_Response & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::PatrolControl_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::PatrolControl_Response & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::PatrolControl_Response>()
{
  return "aid_robot_msgs::srv::PatrolControl_Response";
}

template<>
inline const char * name<aid_robot_msgs::srv::PatrolControl_Response>()
{
  return "aid_robot_msgs/srv/PatrolControl_Response";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::PatrolControl_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::PatrolControl_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::PatrolControl_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aid_robot_msgs::srv::PatrolControl>()
{
  return "aid_robot_msgs::srv::PatrolControl";
}

template<>
inline const char * name<aid_robot_msgs::srv::PatrolControl>()
{
  return "aid_robot_msgs/srv/PatrolControl";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::PatrolControl>
  : std::integral_constant<
    bool,
    has_fixed_size<aid_robot_msgs::srv::PatrolControl_Request>::value &&
    has_fixed_size<aid_robot_msgs::srv::PatrolControl_Response>::value
  >
{
};

template<>
struct has_bounded_size<aid_robot_msgs::srv::PatrolControl>
  : std::integral_constant<
    bool,
    has_bounded_size<aid_robot_msgs::srv::PatrolControl_Request>::value &&
    has_bounded_size<aid_robot_msgs::srv::PatrolControl_Response>::value
  >
{
};

template<>
struct is_service<aid_robot_msgs::srv::PatrolControl>
  : std::true_type
{
};

template<>
struct is_service_request<aid_robot_msgs::srv::PatrolControl_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aid_robot_msgs::srv::PatrolControl_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__PATROL_CONTROL__TRAITS_HPP_
