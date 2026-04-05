import asyncio
import torch
import time
import logging
from typing import List

#Setup logging for Termux output
logging.basicConfig(level=logging.INFO,format='[%(levelname)s]%(message)s')

class SwarmEngine:
    def __init__(self,agents):
        self.agents = agents
        self.memory_buffer = torch.zeros((1,128))
        self.latencies = []

    def _optimize_signal(self,tensor:torch.Tensor):
        """Sparse pruning to keep the NPU/CPU lean"""

        if tensor is None:
            return torch.zeros((1,128))

        with torch.no_grad():
            return tensor*(torch.abs(tensor)>0.1).float()

    async def _execute_with_timer(self,agent,task):
        """Precision timing for sub-50ms proof"""

        start_ns = time.perf_counter_ns()

        try:
            refined_mem = self._optimize_signal(self.memory_buffer)

            result = await agent.process(task,refined_mem)

            duration = (time.perf_counter_ns()-start_ns)/1_000_000

            return result,duration

        except Exception as e:
            return e,0

    async def run_benchmark_cycle(self,tasks:List[str]):
        """The high-frequency Mission Loop"""

        print(f"\n---Initializing Veritas BenchMarking---")

        for task in tasks:
            execution_pool = [self._execute_with_timer(a,task) for a in self.agents]

            responses = await asyncio.gather(*execution_pool)

            total_cycle_latencies = []

            for i,(res,latency) in enumerate(responses):
                role = self.agents[i].role

                if isinstance(res,Exception):
                    logging.error(f"Agent{role} failed:{res}")
                else:
                    self.memory_buffer = res
                    total_cycle_latencies.append(latency)

                    print(f"|{role.ljust(10)}|Latency: {latency:.2f}ms| Status:OK")

            if total_cycle_latencies:
                avg = sum(total_cycle_latencies)/len(total_cycle_latencies)
                self.latencies.append(avg)

        if self.latencies:
            final_avg = sum(self.latencies)/len(self.latencies)
            print("-"*45)

            print(f"FINAL AVERAGE LATENCY: {final_avg:.2f}ms")

            print(f"PERFORMANCE RATING: {'ELITE' if final_avg<50 else 'OPTIMIZE'}")
            print("-"*45)

class Specialist:
    def __init__(self,role):
        self.role = role

    async def process(self,ctx,mem):
        torch.randn(1,128)

if __name__ == "__main__":

    swarm = [Specialist("Doctor"), Specialist("Economist")]

    engine = SwarmEngine(swarm)

    mission_tasks = ["Analyze Bio-Threat","Model Market Shock"]

    asyncio.run(engine.run_benchmark_cycle(mission_tasks))


