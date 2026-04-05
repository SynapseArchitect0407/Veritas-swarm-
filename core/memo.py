import torch
import time
from collections import deque
from typing import List,Dict,Any,Optional

class VeritasMemory:
    def __init__(self,capacity: int=10,embedding_dim : int= 128):

        self.capacity = capacity
        self.embedding_dim = embedding_dim

        self.thought_buffer = deque(maxlen=capacity)

        self.state_matrix = torch.zeros((capacity,embedding_dim))
        self.cursor = 0

    def add_thought(self,content:str,importance : float =1.0):

        timestamp = time.time()
        thought_entry = {
                 "content"    : content,
                 "ts"         : timestamp,
                 "importance" : importance
        }

        self.thought_buffer.append(thought_entry)

        new_vector = torch.randn(1,self.embedding_dim)*importance

        self.state_matrix[self.cursor] = new_vector

        self.cursor = (self.cursor+1)%self.capacity

    def get_context_summary(self):
        if len(self.thought_buffer) == 0:
            return torch.zeros(1,self.embedding_dim)

        weights = torch.linspace(0.5,1.0,steps = len(self.thought_buffer))

        active_memory = self.state_matrix[:len(self.thought_buffer)]
        weighted_memory = active_memory*weights.unsqueeze(1)

        return torch.mean(weighted_memory,dim=0)

    def clear_entropy(self):
        self.thought_buffer.clear()
        self.state_matrix.zero_()
        self.cursor = 0
        print("[VERITAS-MEMORY] Entropy cleared. State reset for new mission")

    def debug_dump(self):
        print(f"\n---Current Memory State(Capacity:{self.capacity})---")

        for i,thought in enumerate(self.thought_buffer):
            age = round(time.time() -thought['ts'],2)
            print(f" [{i}] {thought['content'][:40]}...(Age:{age}s)")

#---INTEGRATION EXAMPLE---
if __name__ == "__main__":
    brain = VeritasMemory(capacity=5)

    events = [
     "Patient data privacy protocols reviewed.",
     "Insurance billing code 77 detected.",
     "Conflict found in surgery scheduling.",
     "Pharmacy inventory levels updated.",
     "Emergency ward capacity at 90%.",
     "NEW MISSION : Analyze legal contract.",
   ]

    for event in events:
        print(f"Processing: {event}")
        brain.add_thought(event,importance = 0.9)
        time.sleep(0.1)

    brain.debug_dump()

    summary_vector= brain.get_context_summary()
    print(f"\n Context Summary Tensor Shape:{summary_vector.shape}")

    brain.clear_entropy()

