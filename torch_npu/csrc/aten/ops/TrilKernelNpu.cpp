#include "torch_npu/csrc/framework/utils/OpAdapter.h"
#include "torch_npu/csrc/aten/NPUNativeFunctions.h"

namespace at_npu {
namespace native {
at::Tensor& tril_out_nocheck(const at::Tensor& self, int64_t diagonal, at::Tensor& result) {
  OpCommand cmd;
  cmd.Name("Tril")
      .Input(self)
      .Output(result)
      .Attr("diagonal", diagonal)
      .Run();
  return result;
}

at::Tensor& NPUNativeFunctions::tril_out(const at::Tensor& self, int64_t diagonal, at::Tensor& result) {
  OpPreparation::CheckOut(
      {self},
      result,
      self);

  if (!NpuUtils::check_match(&result)) {
    at::Tensor contiguousResult = NpuUtils::format_contiguous(result);
    tril_out_nocheck(self, diagonal, contiguousResult);
    NpuUtils::format_fresh_view(result, contiguousResult);
  } else {
    tril_out_nocheck(self, diagonal, result);
  }

  return result;
}

at::Tensor NPUNativeFunctions::tril(const at::Tensor& self, int64_t diagonal) {
  auto is_last_two_dims = [&self]() {
      auto selfStorage = torch_npu::NPUBridge::GetNpuStorageImpl(self)->get_npu_desc().storage_sizes_;
      if (selfStorage.size() <= 1) {
          return false;
      }

      return true;
  };
  TORCH_CHECK(is_last_two_dims(), "tril require tensor should be last two dims");
  at::Tensor result = OpPreparation::ApplyTensor(self);
  tril_out_nocheck(self, diagonal, result);

  return result;
}

at::Tensor& NPUNativeFunctions::tril_(at::Tensor& self, int64_t diagonal) {
  NPUNativeFunctions::tril_out(self, diagonal, self);

  return self;
}
} // namespace native
} // namespace at_npu
