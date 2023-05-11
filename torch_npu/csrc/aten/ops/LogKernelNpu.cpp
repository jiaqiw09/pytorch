#include "torch_npu/csrc/framework/utils/OpAdapter.h"
#include "torch_npu/csrc/aten/NPUNativeFunctions.h"

namespace at_npu {
namespace native {
namespace {

at::Tensor& log_out_npu_nocheck(at::Tensor& result, const at::Tensor& self) {
  OpCommand cmd;
  cmd.Name("Log")
      .Input(self)
      .Output(result)
      .Attr("base", (float)-1)
      .Attr("scale", (float)1)
      .Attr("shift", (float)0)
      .Run();

  return result;
}

} // namespace

at::Tensor& NPUNativeFunctions::log_out(const at::Tensor& self, at::Tensor& result) {
  if (!result.is_same(self)) {
    OpPreparation::CheckOut(
        {self},
        result,
        ACL_FORMAT_ND,
        self.scalar_type(),
        self.sizes());
  }

  OpPipeWithDefinedOut pipe;
  return pipe.CheckMemory({self}, {result})
   .Func([&self](at::Tensor& result){log_out_npu_nocheck(result, self);})
   .Call(result);
}

at::Tensor NPUNativeFunctions::log(const at::Tensor& self) {
  // construct the output tensor of the NPU
  at::Tensor result = OpPreparation::ApplyTensor(self);

  // calculate the output result of the NPU
  log_out_npu_nocheck(result, self);

  return result;
}

at::Tensor& NPUNativeFunctions::log_(at::Tensor& self) {
  NPUNativeFunctions::log_out(self, self);

  return self;
}

} // namespace native
} // namespace at_npu
