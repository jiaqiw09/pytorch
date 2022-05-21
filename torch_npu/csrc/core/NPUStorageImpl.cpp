#include "torch_npu/csrc/core/NPUStorageImpl.h"

#ifdef USE_GRAPH_MODE
#include <torch_npu/csrc/framework/graph/util/NPUGraphContextManager.h>
#endif

namespace torch_npu {

NPUStorageImpl::NPUStorageImpl(
    use_byte_size_t use_byte_size,
    size_t size_bytes,
    at::DataPtr data_ptr,
    at::Allocator* allocator,
    bool resizable) : c10::StorageImpl(
      use_byte_size,
      size_bytes,
      at::DataPtr(std::move(data_ptr)),
      allocator,
      resizable)
{
#ifdef USE_GRAPH_MODE    
    npu_graph_desc = std::make_unique<NpuGraphDesc>();
#endif
}

void NPUStorageImpl::release_resources() {
  StorageImpl::release_resources();
#ifdef USE_GRAPH_MODE  
  if (this->npu_graph_desc != nullptr) {
    at_npu::native::NpuGraphContextManager::GetInstance().EraseOutputStorage(
        this->device().index(), this->get_npu_graph_desc().unique_id);
  }
#endif
}
}