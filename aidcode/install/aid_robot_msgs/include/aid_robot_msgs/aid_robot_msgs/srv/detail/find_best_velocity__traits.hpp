// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:srv/FindBestVelocity.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__TRAITS_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/srv/detail/find_best_velocity__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const FindBestVelocity_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: max_angular_velocity
  {
    out << "max_angular_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.max_angular_velocity, out);
    out << ", ";
  }

  // member: max_speed
  {
    out << "max_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.max_speed, out);
    out << ", ";
  }

  // member: len
  {
    out << "len: ";
    rosidl_generator_traits::value_to_yaml(msg.len, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FindBestVelocity_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: max_angular_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "max_angular_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.max_angular_velocity, out);
    out << "\n";
  }

  // member: max_speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "max_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.max_speed, out);
    out << "\n";
  }

  // member: len
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "len: ";
    rosidl_generator_traits::value_to_yaml(msg.len, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FindBestVelocity_Request & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::FindBestVelocity_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::FindBestVelocity_Request & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::FindBestVelocity_Request>()
{
  return "aid_robot_msgs::srv::FindBestVelocity_Request";
}

template<>
inline const char * name<aid_robot_msgs::srv::FindBestVelocity_Request>()
{
  return "aid_robot_msgs/srv/FindBestVelocity_Request";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::FindBestVelocity_Request>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::FindBestVelocity_Request>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<aid_robot_msgs::srv::FindBestVelocity_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'cmd_vel'
#include "geometry_msgs/msg/detail/twist__traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const FindBestVelocity_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: cmd_vel
  {
    out << "cmd_vel: ";
    to_flow_style_yaml(msg.cmd_vel, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: msg
  {
    out << "msg: ";
    rosidl_generator_traits::value_to_yaml(msg.msg, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FindBestVelocity_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: cmd_vel
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cmd_vel:\n";
    to_block_style_yaml(msg.cmd_vel, out, indentation + 2);
  }

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: msg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "msg: ";
    rosidl_generator_traits::value_to_yaml(msg.msg, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FindBestVelocity_Response & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::FindBestVelocity_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::FindBestVelocity_Response & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::FindBestVelocity_Response>()
{
  return "aid_robot_msgs::srv::FindBestVelocity_Response";
}

template<>
inline const char * name<aid_robot_msgs::srv::FindBestVelocity_Response>()
{
  return "aid_robot_msgs/srv/FindBestVelocity_Response";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::FindBestVelocity_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::FindBestVelocity_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::FindBestVelocity_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aid_robot_msgs::srv::FindBestVelocity>()
{
  return "aid_robot_msgs::srv::FindBestVelocity";
}

template<>
inline const char * name<aid_robot_msgs::srv::FindBestVelocity>()
{
  return "aid_robot_msgs/srv/FindBestVelocity";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::FindBestVelocity>
  : std::integral_constant<
    bool,
    has_fixed_size<aid_robot_msgs::srv::FindBestVelocity_Request>::value &&
    has_fixed_size<aid_robot_msgs::srv::FindBestVelocity_Response>::value
  >
{
};

template<>
struct has_bounded_size<aid_robot_msgs::srv::FindBestVelocity>
  : std::integral_constant<
    bool,
    has_bounded_size<aid_robot_msgs::srv::FindBestVelocity_Request>::value &&
    has_bounded_size<aid_robot_msgs::srv::FindBestVelocity_Response>::value
  >
{
};

template<>
struct is_service<aid_robot_msgs::srv::FindBestVelocity>
  : std::true_type
{
};

template<>
struct is_service_request<aid_robot_msgs::srv::FindBestVelocity_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aid_robot_msgs::srv::FindBestVelocity_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__TRAITS_HPP_
