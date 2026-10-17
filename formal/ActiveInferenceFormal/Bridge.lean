module

@[expose] public section
/-!
# Paper-to-library correspondence

Synthetic owns tested examples and the paper; fep_formal owns generic proofs.

* Perception/VFE: src/generative_model.py; FEP.ActiveInference and
  FEP.FiniteInformation, selected in Information.lean.
* Action/EFE: src/expected_free_energy.py; FEP.ActiveInference, selected in
  Information.lean. A finite minimizer is not a proof of softmax implementation.
* Flow/NESS: src/free_energy_flow.py, src/trajectories.py, src/steady_state.py;
  FEP.NessFlow, selected in Geometry.lean.
* Blanket: GaussianBlanket.lean transports the canonical upstream four-axis
  precision to the second Python fixture, proving native Gaussian conditional
  independence and nonzero marginal covariance. The original diagonal-2.5
  fixture is a separate numerical example, not covered by that theorem.
* Planning: Planning.lean gives an exact two-step Boolean-history channel;
  normalized history preferences add log 2 to the terminal-payoff objective.
  Removing that constant matches terminal pragmatic value minus full-history
  mutual information. A static, uninformative counterexample proves upstream
  stagewise cumulative EFE is different; repeating a perfect observation
  carries only one bit of information. Neither theorem certifies the Python
  floating-point recursion or an observation-adaptive policy tree.

Finite laws, floating-point arrays, OU diffusions, and conditional measures
are distinct carriers. Record normalization, support, sign conventions and
hypotheses for each claimed match. Numerical tests and native Lean evidence
remain separate. See docs/positioning.md for the maintained navigation map.
-/
