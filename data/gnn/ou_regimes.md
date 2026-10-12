## GNNSection
ContinuousStateSpace

## GNNVersionAndFlags
GNN v1.1

## ModelName
Synthetic matched-density OU regimes

## ModelAnnotation
Specification of the continuous two-dimensional OU demonstration. Coordinates
are even under time reversal. D_ou is the diffusion matrix; Q_ou is an
antisymmetric drive, NOT a process-noise covariance. No discrete POMDP backend
execution is asserted. Compare equilibrium and NESS by selecting omega_zero
or omega_driven, holding precision and dissipation fixed.

## StateSpaceBlock
x[2,type=float]
precision[1,type=float]
gamma[1,type=float]
omega_zero[1,type=float]
omega_driven[1,type=float]
P_ou[2,2,type=float]
Gamma_ou[2,2,type=float]
Q_ou[2,2,type=float]
D_ou[2,2,type=float]
rho[1,type=float]
j[2,type=float]

## Connections
precision>P_ou
gamma>Gamma_ou
Gamma_ou>D_ou
P_ou>rho
x>rho
Q_ou>j
P_ou>j
rho>j
x>j

## InitialParameterization
precision=1.0
gamma=1.0
omega_zero=0.0
omega_driven=2.4

## Equations
P_ou = precision * I_2
Gamma_ou = gamma * I_2
Q_ou = omega * [[0,1],[-1,0]]
D_ou = Gamma_ou
dx = (Q_ou - Gamma_ou) P_ou x dt + sqrt(2 D_ou) dW
Phi = 0.5 x^T P_ou x
rho = Z^(-1) exp(-Phi)
j = Q_ou P_ou x rho
sigma = 2 omega^2 precision / gamma

## Time
Continuous
Dynamic

## ActInfOntologyAnnotation
x=ContinuousState
rho=StationaryDensity
j=ProbabilityCurrent

## Footer
Synthetic owns numerical semantics and tests. GNN parsing checks representation,
not stochastic execution, time reversal, theorem validity or physical adequacy.
