import FepSketches.active_inference

/-! A bounded, exact two-step Boolean-history adapter for the paper's terminal
payoff. A whole observation history is one outcome of the upstream finite
channel. Normalizing terminal preferences across two prefixes adds log 2 to
upstream EFE; subtracting it recovers the paper objective. This is not the
upstream cumulative stagewise EFE, and does not certify floating-point Bayes. -/
namespace ActiveInferenceFormal
open FEP FEP.FiniteInformation FEP.ActiveInference
open scoped BigOperators
noncomputable section

/-- Two conditionally independent observations of one static Boolean state. -/
def twoStepHistory (first second : FiniteKernel Bool Bool) :
    FiniteKernel Bool (Bool × Bool) where
  mass state history := first state history.1 * second state history.2
  nonneg state history := mul_nonneg (first.nonneg _ _) (second.nonneg _ _)
  sum_one state := by
    rw [Fintype.sum_prod_type]
    simp_rw [← Finset.mul_sum, second.sum_one, mul_one]
    exact first.sum_one state

/-- Exact branch mass used by Python's two-step enumeration, including zeros. -/
theorem twoStep_history_predictive_mass (prior : FiniteLaw Bool)
    (first second : FiniteKernel Bool Bool) (history : Bool × Bool) :
    (twoStepHistory first second).predictive prior history =
      ∑ state, prior state * (first state history.1 * second state history.2) := rfl

/-- The positive-evidence posterior uses that same history likelihood. An
impossible history is not passed to a totalized posterior. -/
theorem twoStep_history_posterior_mass (prior : FiniteLaw Bool)
    (first second : FiniteKernel Bool Bool) (history : Bool × Bool)
    (h : 0 < (twoStepHistory first second).predictive prior history) (state : Bool) :
    (twoStepHistory first second).posterior prior history h state =
      prior state * (first state history.1 * second state history.2) /
        (twoStepHistory first second).predictive prior history := rfl

/-- Uniform prefix times terminal preference; this is normalized, unlike just
copying terminal mass onto every history. -/
def historyPreference (terminal : FiniteLaw Bool) : FiniteLaw (Bool × Bool) :=
  fairBoolLaw.product terminal

/-- A fixed two-action sequence becomes one history channel. The policy carrier
is singleton because the adapter evaluates one selected sequence at a time. -/
def historyModel (prior : FiniteLaw Bool) (channel : FiniteKernel Bool (Bool × Bool))
    (terminal : FiniteLaw Bool) : GenerativeModel Unit Bool (Bool × Bool) where
  initialState := prior
  transition _ := FiniteKernel.identity
  likelihood := channel
  preferences := historyPreference terminal
  policyPrior := FiniteLaw.pointMass ()

/-- The paper's terminal pragmatic value and full-history information value. -/
def terminalHistoryEFE (prior : FiniteLaw Bool)
    (channel : FiniteKernel Bool (Bool × Bool)) (terminal : FiniteLaw Bool) : ℝ :=
  -(∑ history, channel.predictive prior history * Real.log (terminal history.2)) -
    mutualInformation (channel.joint prior)

/-- Exact history-channel correspondence, with strictly positive terminal
preferences as required by Python. Zero-probability histories remain allowed. -/
theorem ℝ_twoStep_terminal_history_bridge (prior : FiniteLaw Bool)
    (channel : FiniteKernel Bool (Bool × Bool)) (terminal : FiniteLaw Bool)
    (hpositive : ∀ outcome, 0 < terminal outcome) :
    expectedFreeEnergy (historyModel prior channel terminal) () =
      terminalHistoryEFE prior channel terminal + Real.log 2 := by
  have hlog (history : Bool × Bool) :
      Real.log (historyPreference terminal history) =
        Real.log (terminal history.2) - Real.log 2 := by
    change Real.log ((1 / 2 : ℝ) * terminal history.2) = _
    rw [Real.log_mul (by norm_num) (ne_of_gt (hpositive _))]
    rw [Real.log_div (by norm_num) (by norm_num)]
    simp only [Real.log_one, zero_sub]
    ring
  have hpredict : predictedState (historyModel prior channel terminal) () = prior :=
    FiniteKernel.predictive_identity prior
  unfold expectedFreeEnergy pragmaticCost epistemicValue
  simp only [predictedOutcome, predictedJoint, hpredict]
  change crossEntropy (channel.predictive prior) (historyPreference terminal) -
    mutualInformation (channel.joint prior) = _
  unfold crossEntropy terminalHistoryEFE
  simp_rw [hlog, mul_sub]
  simp_rw [neg_mul]
  rw [Finset.sum_sub_distrib, Finset.sum_neg_distrib,
    Finset.sum_neg_distrib, ← Finset.sum_mul, (channel.predictive prior).sum_one]
  ring

/-- Concrete normalized two-stage channel, independent of the static state. -/
def fairHistoryChannel : FiniteKernel Bool (Bool × Bool) :=
  twoStepHistory fairBoolKernel fairBoolKernel

/-- Repeated uninformative observations carry zero state information. -/
theorem fair_history_information_zero :
    mutualInformation (fairHistoryChannel.joint fairBoolLaw) = 0 := by
  have hjoint : fairHistoryChannel.joint fairBoolLaw =
      fairBoolLaw.product (fairBoolLaw.product fairBoolLaw) := by
    apply FiniteLaw.ext_mass
    funext x
    change (1 / 2 : ℝ) * (1 / 2 * (1 / 2)) = _
    rfl
  rw [hjoint]
  exact mutualInformation_product_eq_zero _ _

/-- Paper EFE for two fair uninformative observations has only one terminal
cost, log 2. This is a zero-information boundary with positive pragmatic cost. -/
theorem fair_terminal_history_value :
    terminalHistoryEFE fairBoolLaw fairHistoryChannel fairBoolLaw = Real.log 2 := by
  unfold terminalHistoryEFE
  rw [fair_history_information_zero]
  have hlog : Real.log (1 / 2 : ℝ) = -Real.log 2 := by
    rw [Real.log_div (by norm_num) (by norm_num)]
    simp
  change -(∑ history : Bool × Bool,
    fairHistoryChannel.predictive fairBoolLaw history * Real.log (1 / 2)) - 0 = _
  rw [← Finset.sum_mul, (fairHistoryChannel.predictive fairBoolLaw).sum_one, hlog]
  ring

/-- A genuinely static state, with observations independent of it. -/
def staticFairModel : GenerativeModel Bool Bool Bool where
  initialState := fairBoolLaw
  transition _ := FiniteKernel.identity
  likelihood := fairBoolKernel
  preferences := fairBoolLaw
  policyPrior := fairBoolLaw

/-- Upstream stagewise EFE accumulates two costs in this same uninformative
experiment. It differs from the paper even without information-gain effects. -/
theorem cumulative_terminal_counterexample :
    cumulativeExpectedFreeEnergy staticFairModel [false, false] ≠
      terminalHistoryEFE fairBoolLaw fairHistoryChannel fairBoolLaw := by
  have hstate : predictedState staticFairModel false = fairBoolLaw :=
    FiniteKernel.predictive_identity fairBoolLaw
  have hefe : expectedFreeEnergy staticFairModel false = entropy fairBoolLaw := by
    calc
      _ = expectedFreeEnergy (symmetricBoolModel fairBoolLaw) false := by
        unfold expectedFreeEnergy pragmaticCost epistemicValue predictedOutcome predictedJoint
        rw [hstate, symmetricBoolModel_predictedState]
        rfl
      _ = _ := symmetricBoolModel_expectedFreeEnergy _ _
  have hentropy : entropy fairBoolLaw = Real.log 2 := by
    unfold entropy
    rw [Fintype.sum_bool]
    simp only [fairBoolLaw, Real.negMulLog]
    rw [Real.log_div (by norm_num) (by norm_num)]
    simp only [Real.log_one]
    ring
  rw [fair_terminal_history_value]
  rw [staticState_cumulativeEFE_decomposition staticFairModel _ (fun _ => rfl)]
  simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, hefe, hentropy]
  have hpos : 0 < Real.log 2 := Real.log_pos (by norm_num)
  linarith

/-- Repeating a perfect observation creates only two possible histories. -/
def revealingHistoryChannel : FiniteKernel Bool (Bool × Bool) :=
  twoStepHistory FiniteKernel.identity FiniteKernel.identity

/-- Positive-information boundary: two repeated perfect observations reveal
exactly one fair bit, not two independent bits of state information. -/
theorem revealing_history_information :
    mutualInformation (revealingHistoryChannel.joint fairBoolLaw) = Real.log 2 := by
  norm_num [mutualInformation, finiteKL, revealingHistoryChannel, twoStepHistory,
    FiniteKernel.identity, FiniteKernel.deterministic, FiniteKernel.joint,
    FiniteLaw.product, FiniteLaw.fstMarginal, FiniteLaw.sndMarginal,
    fairBoolLaw, Fintype.sum_prod_type, Fintype.sum_bool, InformationTheory.klFun]
  ring

/-- With fair terminal preferences, one bit of information cancels the
terminal cost. Zero-mass off-diagonal histories are included in this witness. -/
theorem revealing_terminal_history_value :
    terminalHistoryEFE fairBoolLaw revealingHistoryChannel fairBoolLaw = 0 := by
  unfold terminalHistoryEFE
  rw [revealing_history_information]
  change -(∑ history : Bool × Bool,
    revealingHistoryChannel.predictive fairBoolLaw history * Real.log (1 / 2)) -
      Real.log 2 = 0
  rw [← Finset.sum_mul, (revealingHistoryChannel.predictive fairBoolLaw).sum_one,
    Real.log_div (by norm_num) (by norm_num)]
  simp
end
end ActiveInferenceFormal
