// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:srv/PointGet.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__POINT_GET__TRAITS_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__POINT_GET__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/srv/detail/point_get__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const PointGet_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: data_type
  {
    out << "data_type: ";
    rosidl_generator_traits::value_to_yaml(msg.data_type, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PointGet_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: data_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "data_type: ";
    rosidl_generator_traits::value_to_yaml(msg.data_type, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PointGet_Request & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::PointGet_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::PointGet_Request & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::PointGet_Request>()
{
  return "aid_robot_msgs::srv::PointGet_Request";
}

template<>
inline const char * name<aid_robot_msgs::srv::PointGet_Request>()
{
  return "aid_robot_msgs/srv/PointGet_Request";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::PointGet_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::PointGet_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::PointGet_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'message'
#include "aid_robot_msgs/msg/detail/aid_pose__traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const PointGet_Response & msg,
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
    to_flow_style_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PointGet_Response & msg,
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
    out << "message:\n";
    to_block_style_yaml(msg.message, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PointGet_Response & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::PointGet_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::PointGet_Response & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::PointGet_Response>()
{
  return "aid_robot_msgs::srv::PointGet_Response";
}

template<>
inline const char * name<aid_robot_msgs::srv::PointGet_Response>()
{
  return "aid_robot_msgs/srv/PointGet_Response";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::PointGet_Response>
  : std::integral_constant<bool, has_fixed_size<aid_robot_msgs::msg::AidPose>::value> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::PointGet_Response>
  : std::integral_constant<bool, has_bounded_size<aid_robot_msgs::msg::AidPose>::value> {};

template<>
struct is_message<aid_robot_msgs::srv::PointGet_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aid_robot_msgs::srv::PointGet>()
{
  return "aid_robot_msgs::srv::PointGet";
}

template<>
inline const char * name<aid_robot_msgs::srv::PointGet>()
{
  return "aid_robot_msgs/srv/PointGet";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::PointGet>
  : std::integral_constant<
    bool,
    has_fixed_size<aid_robot_msgs::srv::PointGet_Request>::value &&
    has_fixed_size<aid_robot_msgs::srv::PointGet_Response>::value
  >
{
};

template<>
struct has_bounded_size<aid_robot_msgs::srv::PointGet>
  : std::integral_constant<
    bool,
    has_bounded_size<aid_robot_msgs::srv::PointGet_Request>::value &&
    has_bounded_size<aid_robot_msgs::srv::PointGet_Response>::value
  >
{
};

template<>
struct is_service<aid_robot_msgs::srv::PointGet>
  : std::true_type
{
};

template<>
struct is_service_request<aid_robot_msgs::srv::PointGet_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aid_robot_msgs::srv::PointGet_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__POINT_GET__TRAITS_HPP_
