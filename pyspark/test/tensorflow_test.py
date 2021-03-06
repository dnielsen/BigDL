#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from bigdl.nn.layer import *
from bigdl.optim.optimizer import *
from bigdl.util.common import *
import numpy as np
import unittest
import shutil
import tempfile


class TestTensorflow(unittest.TestCase):

    def setUp(self):
        sparkConf = create_spark_conf()
        self.sc = SparkContext(master="local[4]", appName="test model",
                               conf=sparkConf)
        init_engine()

    def tearDown(self):
        self.sc.stop()

    def test_load_and_save(self):
        linear = Linear(10, 2)()
        sigmoid = Sigmoid()(linear)
        softmax = SoftMax().set_name("output")(sigmoid)
        model_original = Model([linear], [softmax])
        input = np.random.random((4, 10))

        temp = tempfile.mkdtemp()

        model_original.save_tensorflow([("input", [4, 10])], temp + "/model.pb")

        model_loaded = Model.load_tensorflow(temp + "/model.pb", ["input"], ["output"])
        expected_output = model_original.forward(input)
        output = model_loaded.forward(input)
        self.assertTrue(np.allclose(output,
                                    expected_output, atol=1e-6, rtol=0))


if __name__ == "__main__":
    unittest.main()
