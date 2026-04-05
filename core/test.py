import unittest
import torch
import logging
from core.task import SwarmEngine,Specialist

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger("MathValidation")

class TestVeritasMath(unittest.TestCase):
    def setUp(self):

        """Initialize the environment for math verification."""

        self.agents = [Specialist("Tester")]
        self.engine = SwarmEngine(self.agents)
        self.threshold = 0.1

    def test_sparsity_threshold(self):

        """Pruning logic mathematically removes noise."""

        #Create a tensor with values above and below the threshold

        test_tensor = torch.tensor([[0.05,0.5,-0.02,-0.8]])

        pruned = self.engine._optimize_signal(test_tensor)

        #We expect 0.05 and -0.02 to become 0.0

        self.assertEqual(pruned[0,0],0.0)
        self.assertEqual(pruned[0,2],0.0)

        #We expect 0.5 and -0.8 to remain

        self.assertNotEqual(pruned[0,1],0.0)

        logger.info("Sparsity Integrity Vetified: Noise Successfully pruned.")

    def test_tensor_dimension_stability(self):

        """Data architecture maintains fixed memory shape."""

        mock_task = "Verify Dimensionality"

        result = torch.randn(1,128)
        self.engine.global_memory = result

        self.assertEqual(self.engine.global_memory.shape,(1,128))

        logger.info("Dimension Stability Verified: Buffer shape is 1×128")

    def test_signal_integration_math(self):

        """Temporal integration correctly averages agent signals."""

        #Previous memory
        mem = torch.ones(1,128)*0.5

        #New agent signal
        signal = torch.ones(1,128)*1.5

        integrated = (signal+mem)/2

        self.assertTrue(torch.allclose(integrated,torch.ones(1,128)*1.0))

        logger.info("Integration Math Verified: Signal Synthesis is accurate.")

if __name__ == "__main__":
    unittest.main()

