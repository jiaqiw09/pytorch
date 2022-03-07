# Copyright (c) 2020, Huawei Technologies.All rights reserved.
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

import torch
import torch_npu
import numpy as np

from torch_npu.testing.testcase import TestCase, run_tests
from torch_npu.testing.common_utils import create_common_tensor

class TestUpsamleTrilinear3D(TestCase):
    def get_shapeFormat(self):
        shape_format2 = [
            [[np.float32, -1, (5, 3, 2, 6, 4)], [10, 10, 10]],
            [[np.float32, -1, (2, 3, 6, 2, 4)], [10, 10, 10]],
        ]
        return shape_format2    

    def cpu_op_exec(self, input1, size):
        output = torch.nn.functional.interpolate(input1, size, mode="trilinear")
        output = output.numpy()
        return output

    def npu_op_exec(self, input1, size):
        output = torch.nn.functional.interpolate(input1, size, mode="trilinear")
        output = output.to("cpu")
        output = output.numpy()
        return output

    def cpu_op_scale_exec(self, input1, size):
        output = torch.nn.functional.interpolate(input1, scale_factor=size, mode="trilinear")
        output = output.numpy()
        return output

    def npu_op_scale_exec(self, input1, size):
        output = torch.nn.functional.interpolate(input1, scale_factor=size, mode="trilinear")
        output = output.to("cpu")
        output = output.numpy()
        return output

    def test_upsample_trilinear3d_shape_format(self, device="npu"):
        shape_format2 = self.get_shapeFormat()
        for item in shape_format2:
            cpu_input2, npu_input2 = create_common_tensor(item[0], 0, 50)
            if cpu_input2 == torch.float16:
                cpu_input2 = cpu_input2.to(torch.float32)

            size = item[1]
            cpu_output = self.cpu_op_exec(cpu_input2, size)
            npu_output = self.npu_op_exec(npu_input2, size)
            cpu_output = cpu_output.astype(npu_output.dtype)
            self.assertRtolEqual(cpu_output, npu_output)

    def test_upsample_trilinear3d_shape_format_scale(self, device="npu"):
        shape_format2 = self.get_shapeFormat()
        for item in shape_format2:
            cpu_input2, npu_input2 = create_common_tensor(item[0], 0, 50)
            if cpu_input2 == torch.float16:
                cpu_input2 = cpu_input2.to(torch.float32)

            size = item[1]
            cpu_output = self.cpu_op_scale_exec(cpu_input2, size)
            npu_output = self.npu_op_scale_exec(npu_input2, size)
            cpu_output = cpu_output.astype(npu_output.dtype)
            self.assertRtolEqual(cpu_output, npu_output)

if __name__ == "__main__":
    run_tests()