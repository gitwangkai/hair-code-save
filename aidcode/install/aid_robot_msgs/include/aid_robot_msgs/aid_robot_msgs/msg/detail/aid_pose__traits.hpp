// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:msg/AidPose.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_POSE__TRAITS_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_POSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/msg/detail/aid_pose__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace aid_robot_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const AidPose & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: name
  {
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AidPose & msg,
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

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AidPose & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace aid_robot_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aid_robot_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aid_robot_msgs::msg::AidPose & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::msg::AidPose & msg)
{
  return aid_robot_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::msg::AidPose>()
{
  return "aid_robot_msgs::msg::AidPose";
}

template<>
inline const char * name<aid_robot_msgs::msg::AidPose>()
{
  return "aid_robot_msgs/msg/AidPose";
}

template<>
struct has_fixed_size<aid_robot_msgs::msg::AidPose>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::msg::AidPose>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::msg::AidPose>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_POSE__TRAITS_HPP_
