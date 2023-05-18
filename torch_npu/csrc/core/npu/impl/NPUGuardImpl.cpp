#include "torch_npu/csrc/core/npu/impl/NPUGuardImpl.h"
#include "torch_npu/csrc/core/NPUStorageImpl.h"

namespace c10_npu {

namespace impl {

constexpr c10::DeviceType NPUGuardImpl::static_type;

C10_REGISTER_GUARD_IMPL(PrivateUse1, NPUGuardImpl);

#define REGISTER_PRIVATEUSE1_BACKEND(name)                                                      \
  int rename_privateuse1_backend() {                                                            \
    c10::register_privateuse1_backend(#name);                                                   \    
    c10::SetStorageImplCreate(c10::DeviceType::PrivateUse1, &torch_npu::make_npu_storage_impl); \
    return 0;                                                                                   \
  }                                                                                             \
  static const int _temp_##name = rename_privateuse1_backend();

REGISTER_PRIVATEUSE1_BACKEND(npu)

} // namespace impl

} // namespace c10_npu
