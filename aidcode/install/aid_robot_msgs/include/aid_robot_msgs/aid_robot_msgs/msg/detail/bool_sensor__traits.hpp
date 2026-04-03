// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:msg/BoolSensor.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__BOOL_SENSOR__TRAITS_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__BOOL_SENSOR__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/msg/detail/bool_sensor__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace aid_robot_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const BoolSensor & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: triggered
  {
    out << "triggered: ";
    rosidl_generator_traits::value_to_yaml(msg.triggered, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const BoolSensor & msg,
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

  // member: triggered
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "triggered: ";
    rosidl_generator_traits::value_to_yaml(msg.triggered, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const BoolSensor & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::msg::BoolSensor & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::msg::BoolSensor & msg)
{
  return aid_robot_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::msg::BoolSensor>()
{
  return "aid_robot_msgs::msg::BoolSensor";
}

template<>
inline const char * name<aid_robot_msgs::msg::BoolSensor>()
{
  return "aid_robot_msgs/msg/BoolSensor";
}

template<>
struct has_fixed_size<aid_robot_msgs::msg::BoolSensor>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<aid_robot_msgs::msg::BoolSensor>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<aid_robot_msgs::msg::BoolSensor>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__BOOL_SENSOR__TRAITS_HPP_
