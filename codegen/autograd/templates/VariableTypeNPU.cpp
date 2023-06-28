#include <torch/csrc/autograd/VariableTypeUtils.h>

#include <c10/core/impl/TorchDispatchModeTLS.h>
#include <ATen/core/TorchDispatchUtils.h>
#include <ATen/SparseCsrTensorUtils.h>
#include <ATen/RedispatchFunctions.h>
#include <torch/library.h>

#include "torch_npu/csrc/aten/NPUNativeFunctions.h"
#include "torch_npu/csrc/aten/VariableType.h"
#include "torch_npu/csrc/framework/autograd/FunctionsManual.h"


// ${generated_comment}

// NOTE [Sharded File]: on this file's split-into-shards state
//
// Back in the good old days, VariableType.cpp was generated as one
// file with every function in it, and everything was great and
// simple.
//
// However, this file was also very large (over 36,000 lines), and
// compiling it was very slow, and in fact was a significant
// bottleneck for incremental rebuilds. To address this, we now
// generate the file split across multiple shards, named
// VariableType_0.cpp and so on, which can be compiled in parallel.
//
// For ease of inspection and debugging, so that it's not necessary to
// go rooting around in multiple files, we also generate all the
// functions together in VariableTypeEverything.cpp. This generated
// file is only for convenience; it's not actually used in the
// build. If the file you're looking at now is one of the shards, you
// may want to switch over to the Everything variant to make you
// grepping smoother.

using namespace at;
using namespace at_npu::autograd::generated;
using namespace at_npu::autograd::generated::details;

namespace at_npu { namespace autograd {

namespace VariableType {
namespace{
  C10_UNUSED void reset_grad_accumulator(Variable & self) {
    AutogradMeta* meta = torch::autograd::impl::get_autograd_meta(self);
    if (meta != nullptr) {
      meta->grad_accumulator_.reset();
    }
  }
}

${npu_method_definitions}
} // namespace VariableType

namespace {

TORCH_LIBRARY_IMPL(aten, AutogradPrivateUse1, m) {
  ${wrapper_registrations}
}

}

}} // namespace at_npu::autograd
