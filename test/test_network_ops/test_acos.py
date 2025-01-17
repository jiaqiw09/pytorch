import torch
import numpy as np

from torch_npu.testing.testcase import TestCase, run_tests
from torch_npu.testing.common_utils import create_common_tensor


class TestAcos(TestCase):
    def cpu_op_exec(self, input_para):
        output = torch.acos(input_para) 
        output = output.numpy()
        return output
 
    def npu_op_exec(self, input_para):
        output = torch.acos(input_para) 
        output = output.to("cpu") 
        output = output.numpy()
        return output  
        
    def test_acos_common_shape_format(self, device="npu"):
        shape_format = [
                [[np.float32, -1, 1]],
                [[np.float32, -1, (64, 10)]], 
                [[np.float32, -1, (32, 1, 3)]]
        ]
        for item in shape_format:
            cpu_input, npu_input = create_common_tensor(item[0], -1, 1)
            cpu_output = self.cpu_op_exec(cpu_input)
            npu_output = self.npu_op_exec(npu_input)
            self.assertRtolEqual(cpu_output, npu_output)

    def test_acos_float16_shape_format(self, device="npu"):
        def cpu_op_exec_fp16(input_para):
            input_para = input_para.to(torch.float32)
            output = torch.acos(input_para)
            output = output.numpy()
            output = output.astype(np.float16)
            return output

        shape_format = [
                [[np.float16, -1, 1]], 
                [[np.float16, -1, (64, 10)]],    
                [[np.float16, -1, (31, 1, 3)]]
        ] 
        for item in shape_format:
            cpu_input, npu_input = create_common_tensor(item[0], -1, 1)
            cpu_output = cpu_op_exec_fp16(cpu_input)
            npu_output = self.npu_op_exec(npu_input)
            self.assertRtolEqual(cpu_output, npu_output)  


if __name__ == "__main__":
    run_tests()
        
