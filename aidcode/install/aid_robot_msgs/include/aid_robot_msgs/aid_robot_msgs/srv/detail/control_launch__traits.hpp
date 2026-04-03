// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:srv/ControlLaunch.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__CONTROL_LAUNCH__TRAITS_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__CONTROL_LAUNCH__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/srv/detail/control_launch__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ControlLaunch_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: launch_file
  {
    out << "launch_file: ";
    rosidl_generator_traits::value_to_yaml(msg.launch_file, out);
    out << ", ";
  }

  // member: parameter
  {
    out << "parameter: ";
    rosidl_generator_traits::value_to_yaml(msg.parameter, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ControlLaunch_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: launch_file
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "launch_file: ";
    rosidl_generator_traits::value_to_yaml(msg.launch_file, out);
    out << "\n";
  }

  // member: parameter
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "parameter: ";
    rosidl_generator_traits::value_to_yaml(msg.parameter, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ControlLaunch_Request & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::ControlLaunch_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::ControlLaunch_Request & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::ControlLaunch_Request>()
{
  return "aid_robot_msgs::srv::ControlLaunch_Request";
}

template<>
inline const char * name<aid_robot_msgs::srv::ControlLaunch_Request>()
{
  return "aid_robot_msgs/srv/ControlLaunch_Request";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::ControlLaunch_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::ControlLaunch_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::ControlLaunch_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ControlLaunch_Response & msg,
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
  const ControlLaunch_Response & msg,
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

inline std::string to_yaml(const ControlLaunch_Response & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::ControlLaunch_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::ControlLaunch_Response & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::ControlLaunch_Response>()
{
  return "aid_robot_msgs::srv::ControlLaunch_Response";
}

template<>
inline const char * name<aid_robot_msgs::srv::ControlLaunch_Response>()
{
  return "aid_robot_msgs/srv/ControlLaunch_Response";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::ControlLaunch_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::ControlLaunch_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::ControlLaunch_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aid_robot_msgs::srv::ControlLaunch>()
{
  return "aid_robot_msgs::srv::ControlLaunch";
}

template<>
inline const char * name<aid_robot_msgs::srv::ControlLaunch>()
{
  return "aid_robot_msgs/srv/ControlLaunch";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::ControlLaunch>
  : std::integral_constant<
    bool,
    has_fixed_size<aid_robot_msgs::srv::ControlLaunch_Request>::value &&
    has_fixed_size<aid_robot_msgs::srv::ControlLaunch_Response>::value
  >
{
};

template<>
struct has_bounded_size<aid_robot_msgs::srv::ControlLaunch>
  : std::integral_constant<
    bool,
    has_bounded_size<aid_robot_msgs::srv::ControlLaunch_Request>::value &&
    has_bounded_size<aid_robot_msgs::srv::ControlLaunch_Response>::value
  >
{
};

template<>
struct is_service<aid_robot_msgs::srv::ControlLaunch>
  : std::true_type
{
};

template<>
struct is_service_request<aid_robot_msgs::srv::ControlLaunch_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aid_robot_msgs::srv::ControlLaunch_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__CONTROL_LAUNCH__TRAITS_HPP_
