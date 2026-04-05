import torch
import torch.nn as nn
import torch.nn.functional as F

class VeritasConsensus(nn.Module):
    def __init__(self,num_agents : int, temperature: float = 1.0):
        super().__init__()

        self.authority_weights = nn.Parameter(
             torch.tensor([1.2,0.5,1.1])
        )

        self.temperature = temperature

    def forward(self,confidences:torch.tensor):

        if confidences.dim() == 1:
            confidences= confidences.unsqueeze(0)

        weighted = self.authority_weights*confidences

        scaled = weighted/self.temperature

        probabilities = F.softmax(scaled,dim=-1)

        return probabilities

    def route_outputs(
     self,
     agent_outputs : torch.tensor,
     routing_probs : torch.tensor
     ):

        routing_probs = routing_probs.unsqueeze(-1)

        combined_output = torch.sum(agent_outputs*routing_probs,dim =0)

        return combined_output

    def entropy_loss(self,probs: torch.tensor):

        entropy = -torch.sum(probs*torch.log(probs + 1e-8), dim= -1)

        return entropy.mean()

    def update_authority(self,agent_idx: int, outcome_correct : bool):

        with torch.no_grad():
            if not outcome_correct:
                self.authority_weights[agent_idx] *= 0.9
            else:
                self.authority.weights[agent_idx] += 0.05

if __name__ == "__main__":

    model= VeritasConsensus(num_agents = 3,temperature = 1.0)

    confidences = torch.tensor([0.9,0.4,0.85])

    routing_probs = model(confidences)

    print("Routing Probabilities")
    print(routing_probs)

    agent_outputs =torch.tensor([
          [0.9,0.1,0.2,0.3],
          [0.2,0.8,0.1,0.4],
          [0.7,0.3,0.6,0.5]
    ])

    agent_outputs = agent_outputs.unsqueeze(0)

    final_output= model.route_outputs(agent_outputs,routing_probs)

    print("\nFinal Route Output:")
    print(final_output)

    print("\nAuthority Before Update:")
    print(model.authority_weights.data)

    model.update_authority(agent_idx = 2,outcome_correct = False)

    print("\nAuthority After Penalty:")
    print(model.authority_weights.data)

    new_probs = model(confidences)

    print("\nUpdated Routing Probabilities:")
    print(new_probs)

