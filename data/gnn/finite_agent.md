## GNNSection
ActInfPOMDP

## GNNVersionAndFlags
GNN v1.1

## ModelName
Synthetic finite cue and bet channels

## ModelAnnotation
Static hidden state, two observations and two available observation channels.
Rows of A_cue and A_bet are outcomes; columns are hidden states.
C_probs is a normalized preference law; C_log is its natural logarithm.
This specifies the one-step EFE example, not a state-dependent payout or
adaptive commitment model. B is the identity for both actions.

## StateSpaceBlock
s[2,type=float]
o[2,type=int]
A_cue[2,2,type=float]
A_bet[2,2,type=float]
D[2,type=float]
C_probs[2,type=float]
C_log[2,type=float]
u[1,type=int]
G[2,type=float]

## Connections
D>s
s>o
A_cue>o
A_bet>o
C_log>G
G>u

## InitialParameterization
A_cue={(0.9,0.1),(0.1,0.9)}
A_bet={(0.85,0.85),(0.15,0.15)}
D={(0.5,0.5)}
C_probs={(0.5,0.5)}

## Equations
C_log = ln(C_probs)
q(o|u) = A_u D
q(s|o,u) = A_u[o,s] D[s] / q(o|u)
G(u) = -E_q[C_log(o)] - I_q(s;o|u)
B_u = I_2

## Time
Discrete
Static

## Footer
The local bridge verifies parsed arrays against Synthetic demos. This is not
a claim that a generic GNN execution backend implements this EFE convention.
