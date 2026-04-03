// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:srv/GetDockPose.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__GET_DOCK_POSE__TRAITS_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__GET_DOCK_POSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/srv/detail/get_dock_pose__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetDockPose_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: map_id
  {
    out << "map_id: ";
    rosidl_generator_traits::value_to_yaml(msg.map_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetDockPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: map_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "map_id: ";
    rosidl_generator_traits::value_to_yaml(msg.map_id, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetDockPose_Request & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::GetDockPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::GetDockPose_Request & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::GetDockPose_Request>()
{
  return "aid_robot_msgs::srv::GetDockPose_Request";
}

template<>
inline const char * name<aid_robot_msgs::srv::GetDockPose_Request>()
{
  return "aid_robot_msgs/srv/GetDockPose_Request";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::GetDockPose_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::GetDockPose_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<aid_robot_msgs::srv::GetDockPose_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'point'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetDockPose_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: point
  {
    out << "point: ";
    to_flow_style_yaml(msg.point, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetDockPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "point:\n";
    to_block_style_yaml(msg.point, out, indentation + 2);
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

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetDockPose_Response & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::GetDockPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::GetDockPose_Response & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::GetDockPose_Response>()
{
  return "aid_robot_msgs::srv::GetDockPose_Response";
}

template<>
inline const char * name<aid_robot_msgs::srv::GetDockPose_Response>()
{
  return "aid_robot_msgs/srv/GetDockPose_Response";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::GetDockPose_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::GetDockPose_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::GetDockPose_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aid_robot_msgs::srv::GetDockPose>()
{
  return "aid_robot_msgs::srv::GetDockPose";
}

template<>
inline const char * name<aid_robot_msgs::srv::GetDockPose>()
{
  return "aid_robot_msgs/srv/GetDockPose";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::GetDockPose>
  : std::integral_constant<
    bool,
    has_fixed_size<aid_robot_msgs::srv::GetDockPose_Request>::value &&
    has_fixed_size<aid_robot_msgs::srv::GetDockPose_Response>::value
  >
{
};

template<>
struct has_bounded_size<aid_robot_msgs::srv::GetDockPose>
  : std::integral_constant<
    bool,
    has_bounded_size<aid_robot_msgs::srv::GetDockPose_Request>::value &&
    has_bounded_size<aid_robot_msgs::srv::GetDockPose_Response>::value
  >
{
};

template<>
struct is_service<aid_robot_msgs::srv::GetDockPose>
  : std::true_type
{
};

template<>
struct is_service_request<aid_robot_msgs::srv::GetDockPose_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aid_robot_msgs::srv::GetDockPose_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__GET_DOCK_POSE__TRAITS_HPP_
