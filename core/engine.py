import torch
import time
import torch.nn.functional as F

class SwarmState:
    def __init__(self,dimension : int = 128):
        self.dim = dimension
        self.data = torch.randn(1,self.dim)
        self._normalize

    def _normalize(self):
        norm = torch.norm(self.data)
        if norm > 0:
            self.data = self.data/norm

    def get_energy(self):
        return torch.norm(self.data).item()


class ConsensusRouter:
    def __init__(self):
        pass

    def calculate_trust(self,state_vector,agent_vector):
         similarity= torch.dot(state_vector.flatten(),agent_vector.flatten())
         return similarity.item()


def initialize_latent_brain(dim=128):
    brain = torch.randn(1,dim)
    brain = F.normalize(brain,p=2,dim=-1)
    return brain

def stochastic_nudge_apply(brain,strength=0.01):
    nudge= torch.randn_like(brain)*strength
    new_brain = brain+nudge
    new_brain= F.normalize(new_brain,p=2,dim=-1)
    return new_brain


class SwarmOrchaestrator:
    def __init__(self,num_agents=5,dim=128):
        self.agents=torch.randn(num_agents,dim)
        self.agents=F.normalize(self.agents,p=2,dim=-1)

    def get_consensus(self,input_data):
        input_data=F.normalize(input_data,p=2,dim=-1)
        scores= torch.matmul(self.agents,input_data.T)
        weights = F.softmax(scores,dim=0)
        consensus= torch.matmul(weights.T,self.agents)
        consensus= F.normalize(consensus,p=2,dim=-1)
        return consensus


class TemporalMemory:
    def __init__(self,decay_rate=0.01):
        self.decay_rate= decay_rate
        self.last_check_time= time.time()

    def apply_fade_time(self,brain_state):
        current_time= time.time()
        time_passed= current_time-self.last_check_time
        faded_factor= torch.exp(torch.tensor(self.decay_rate*time_passed))
        faded_brain= brain_state*faded_factor
        self.last_check_time = current_time
        return F.normalize(faded_brain,p=2,dim=-1)

if __name__=="__main__":
    engine = SwarmState()
    print(f" Vector Energy: {engine.get_energy():.4f}")


    v1 = torch.tensor([1.0,0.0])
    v2 = torch.tensor([1.0,0.0])

    router= ConsensusRouter()
    trust= router.calculate_trust(v1,v2)
    print(f" Trust score(Perfect Match): {trust}")


    my_brain= initialize_latent_brain()
    print(f" Start energy {torch.norm(my_brain).item():.2f}")

    nudged_brain= stochastic_nudge_apply(my_brain)
    print(f"Energy after nudge and repair: {torch.norm(nudged_brain).item():.2f}")


    swarm= SwarmOrchaestrator()
    question= torch.randn(1,128)

    super_answer= swarm.get_consensus(question)
    print(f"Swarm Orchaestrator Energy: {torch.norm(super_answer).item():.2f}")


    memory= TemporalMemory(decay_rate=0.5)
    brain= torch.randn(1,128)
    brain= F.normalize(brain,p=2,dim=-1)

    print("Waiting 2 seconds for the eraser to work")
    time.sleep(2)

    faded_brain= memory.apply_fade_time(brain)
    print(f"Energy after fade and repair: {torch.norm(faded_brain).item():.2f}")

