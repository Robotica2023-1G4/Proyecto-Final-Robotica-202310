// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from proyecto_interfaces:msg/Banner.idl
// generated code does not contain a copyright notice

#ifndef PROYECTO_INTERFACES__MSG__DETAIL__BANNER__TRAITS_HPP_
#define PROYECTO_INTERFACES__MSG__DETAIL__BANNER__TRAITS_HPP_

#include "proyecto_interfaces/msg/detail/banner__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<proyecto_interfaces::msg::Banner>()
{
  return "proyecto_interfaces::msg::Banner";
}

template<>
inline const char * name<proyecto_interfaces::msg::Banner>()
{
  return "proyecto_interfaces/msg/Banner";
}

template<>
struct has_fixed_size<proyecto_interfaces::msg::Banner>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<proyecto_interfaces::msg::Banner>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<proyecto_interfaces::msg::Banner>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PROYECTO_INTERFACES__MSG__DETAIL__BANNER__TRAITS_HPP_
