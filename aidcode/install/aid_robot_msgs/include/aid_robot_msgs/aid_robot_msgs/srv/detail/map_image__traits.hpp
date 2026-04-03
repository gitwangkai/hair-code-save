// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:srv/MapImage.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__MAP_IMAGE__TRAITS_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__MAP_IMAGE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/srv/detail/map_image__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MapImage_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MapImage_Request & msg,
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MapImage_Request & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::MapImage_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::MapImage_Request & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::MapImage_Request>()
{
  return "aid_robot_msgs::srv::MapImage_Request";
}

template<>
inline const char * name<aid_robot_msgs::srv::MapImage_Request>()
{
  return "aid_robot_msgs/srv/MapImage_Request";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::MapImage_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::MapImage_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<aid_robot_msgs::srv::MapImage_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'map'
#include "nav_msgs/msg/detail/occupancy_grid__traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MapImage_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: map
  {
    out << "map: ";
    to_flow_style_yaml(msg.map, out);
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
  const MapImage_Response & msg,
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

  // member: map
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "map:\n";
    to_block_style_yaml(msg.map, out, indentation + 2);
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

inline std::string to_yaml(const MapImage_Response & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::srv::MapImage_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::MapImage_Response & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::MapImage_Response>()
{
  return "aid_robot_msgs::srv::MapImage_Response";
}

template<>
inline const char * name<aid_robot_msgs::srv::MapImage_Response>()
{
  return "aid_robot_msgs/srv/MapImage_Response";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::MapImage_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::MapImage_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::MapImage_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aid_robot_msgs::srv::MapImage>()
{
  return "aid_robot_msgs::srv::MapImage";
}

template<>
inline const char * name<aid_robot_msgs::srv::MapImage>()
{
  return "aid_robot_msgs/srv/MapImage";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::MapImage>
  : std::integral_constant<
    bool,
    has_fixed_size<aid_robot_msgs::srv::MapImage_Request>::value &&
    has_fixed_size<aid_robot_msgs::srv::MapImage_Response>::value
  >
{
};

template<>
struct has_bounded_size<aid_robot_msgs::srv::MapImage>
  : std::integral_constant<
    bool,
    has_bounded_size<aid_robot_msgs::srv::MapImage_Request>::value &&
    has_bounded_size<aid_robot_msgs::srv::MapImage_Response>::value
  >
{
};

template<>
struct is_service<aid_robot_msgs::srv::MapImage>
  : std::true_type
{
};

template<>
struct is_service_request<aid_robot_msgs::srv::MapImage_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aid_robot_msgs::srv::MapImage_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__MAP_IMAGE__TRAITS_HPP_
