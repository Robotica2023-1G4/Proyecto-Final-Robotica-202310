// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from proyecto_interfaces:srv/StartPerceptionTest.idl
// generated code does not contain a copyright notice

#ifndef PROYECTO_INTERFACES__SRV__DETAIL__START_PERCEPTION_TEST__TRAITS_HPP_
#define PROYECTO_INTERFACES__SRV__DETAIL__START_PERCEPTION_TEST__TRAITS_HPP_

#include "proyecto_interfaces/srv/detail/start_perception_test__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<proyecto_interfaces::srv::StartPerceptionTest_Request>()
{
  return "proyecto_interfaces::srv::StartPerceptionTest_Request";
}

template<>
inline const char * name<proyecto_interfaces::srv::StartPerceptionTest_Request>()
{
  return "proyecto_interfaces/srv/StartPerceptionTest_Request";
}

template<>
struct has_fixed_size<proyecto_interfaces::srv::StartPerceptionTest_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<proyecto_interfaces::srv::StartPerceptionTest_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<proyecto_interfaces::srv::StartPerceptionTest_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<proyecto_interfaces::srv::StartPerceptionTest_Response>()
{
  return "proyecto_interfaces::srv::StartPerceptionTest_Response";
}

template<>
inline const char * name<proyecto_interfaces::srv::StartPerceptionTest_Response>()
{
  return "proyecto_interfaces/srv/StartPerceptionTest_Response";
}

template<>
struct has_fixed_size<proyecto_interfaces::srv::StartPerceptionTest_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<proyecto_interfaces::srv::StartPerceptionTest_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<proyecto_interfaces::srv::StartPerceptionTest_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<proyecto_interfaces::srv::StartPerceptionTest>()
{
  return "proyecto_interfaces::srv::StartPerceptionTest";
}

template<>
inline const char * name<proyecto_interfaces::srv::StartPerceptionTest>()
{
  return "proyecto_interfaces/srv/StartPerceptionTest";
}

template<>
struct has_fixed_size<proyecto_interfaces::srv::StartPerceptionTest>
  : std::integral_constant<
    bool,
    has_fixed_size<proyecto_interfaces::srv::StartPerceptionTest_Request>::value &&
    has_fixed_size<proyecto_interfaces::srv::StartPerceptionTest_Response>::value
  >
{
};

template<>
struct has_bounded_size<proyecto_interfaces::srv::StartPerceptionTest>
  : std::integral_constant<
    bool,
    has_bounded_size<proyecto_interfaces::srv::StartPerceptionTest_Request>::value &&
    has_bounded_size<proyecto_interfaces::srv::StartPerceptionTest_Response>::value
  >
{
};

template<>
struct is_service<proyecto_interfaces::srv::StartPerceptionTest>
  : std::true_type
{
};

template<>
struct is_service_request<proyecto_interfaces::srv::StartPerceptionTest_Request>
  : std::true_type
{
};

template<>
struct is_service_response<proyecto_interfaces::srv::StartPerceptionTest_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PROYECTO_INTERFACES__SRV__DETAIL__START_PERCEPTION_TEST__TRAITS_HPP_
