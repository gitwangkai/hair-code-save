// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:msg/AidPoses.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_POSES__TRAITS_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_POSES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/msg/detail/aid_poses__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'poses'
#include "aid_robot_msgs/msg/detail/aid_pose__traits.hpp"

namespace aid_robot_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const AidPoses & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: poses
  {
    if (msg.poses.size() == 0) {
      out << "poses: []";
    } else {
      out << "poses: [";
      size_t pending_items = msg.poses.size();
      for (auto item : msg.poses) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AidPoses & msg,
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

  // member: poses
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.poses.size() == 0) {
      out << "poses: []\n";
    } else {
      out << "poses:\n";
      for (auto item : msg.poses) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AidPoses & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::msg::AidPoses & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::msg::AidPoses & msg)
{
  return aid_robot_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::msg::AidPoses>()
{
  return "aid_robot_msgs::msg::AidPoses";
}

template<>
inline const char * name<aid_robot_msgs::msg::AidPoses>()
{
  return "aid_robot_msgs/msg/AidPoses";
}

template<>
struct has_fixed_size<aid_robot_msgs::msg::AidPoses>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::msg::AidPoses>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::msg::AidPoses>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_POSES__TRAITS_HPP_
