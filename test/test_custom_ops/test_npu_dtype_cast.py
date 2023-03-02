# Copyright (c) 2023 Huawei Technologies Co., Ltd
# All rights reserved.
#
# Licensed under the BSD 3-Clause License  (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import torch

import torch_npu
from torch_npu.testing.testcase import TestCase, run_tests
from torch_npu.testing.common_utils import create_common_tensor


class TestDtypeCast(TestCase):

    def supported_op_exec(self, input1, dst_dtype):
        output = input1.to(dst_dtype)
        return output.cpu().detach()

    def custom_op_exec(self, input1, dst_dtype):
        output = torch_npu.npu_dtype_cast(input1, dst_dtype)
        return output.cpu().detach()

    def test_npu_dtype_cast(self, device="npu"):
        item = [np.float32, 0, (64, 10)]
        _, npu_input = create_common_tensor(item, -1, 1)
        dst_dtype = torch.float16

        supported_output = self.supported_op_exec(npu_input, dst_dtype)
        custom_output = self.custom_op_exec(npu_input, dst_dtype)
        self.assertRtolEqual(supported_output, custom_output)


if __name__ == "__main__":
    run_tests()