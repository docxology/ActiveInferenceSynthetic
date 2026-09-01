/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/

/-!
# Bayesian-mechanics geometry — the conservative solenoidal current

Formal counterpart to `src/free_energy_flow.py`, `src/trajectories.py`, and
`src/steady_state.py`. Everything is over the integers `ℤ`, which suffices for
the *structural* claims (they are polynomial identities and sign facts,
independent of the real-number completion); the Python side carries the
floating-point instances.

The Bayesian-mechanics flow is `f = (Q - Γ)∇F` with `Γ = γ·I` symmetric
(dissipative) and `Q = ω·[[0,1],[-1,0]]` antisymmetric (solenoidal). Here the
gradient `g = ∇F` is an arbitrary vector, so the results hold pointwise for any
free-energy landscape.

## Main results

* `solenoidal_orthogonal` — the solenoidal current `Q g` is orthogonal to the
  gradient `g`; it does no work against free energy (`§1`, `§3`).
* `flow_work_eq_dissipation` — the work of the full flow against `g` is exactly
  the dissipative part `-γ‖g‖²`; the solenoidal part contributes nothing, so
  free energy is non-increasing and the circulation is free.
* `detailed_balance_iff` — the solenoidal current vanishes (for a nonzero
  gradient) iff `ω = 0` (equilibrium / detailed balance).
* `entropyProduction_nonneg` and `entropyProduction_zero_iff` — the
  denominator-cleared entropy-production rate `γ·σ = 2ω²·precision` is
  nonnegative, and zero iff `ω = 0` (`§6`).
-/

namespace ActiveInferenceFormalℤ

/-- A 2-D vector over the integers (a point, a gradient, or a flow value). -/
structure Vec2 where
  x : Int
  y : Int
  deriving DecidableEq, Repr

namespace Vec2

/-- Euclidean inner product `u · v`. -/
def dot (u v : Vec2) : Int := u.x * v.x + u.y * v.y

/-- Squared norm `‖v‖² = v · v`, always nonnegative. -/
def normSq (v : Vec2) : Int := dot v v

/-- The solenoidal (antisymmetric) operator `Q = ω·[[0,1],[-1,0]]` applied to a
vector: `Q v = (ω·v_y, -ω·v_x)`. -/
def solenoidal (ω : Int) (v : Vec2) : Vec2 := ⟨ω * v.y, -(ω * v.x)⟩

/-- Pure dissipative descent `-Γ v = (-γ·v_x, -γ·v_y)`. -/
def dissipative (γ : Int) (v : Vec2) : Vec2 := ⟨-(γ * v.x), -(γ * v.y)⟩

/-- The full Bayesian-mechanics flow `f = (Q - Γ) g = Q g - Γ g`, evaluated at a
gradient `g = ∇F`. -/
def flow (γ ω : Int) (g : Vec2) : Vec2 :=
  ⟨ω * g.y + -(γ * g.x), -(ω * g.x) + -(γ * g.y)⟩

/-- `‖v‖² ≥ 0`: the squared norm is nonnegative. -/
theorem normSq_nonneg (v : Vec2) : 0 ≤ v.normSq := by
  have hx : 0 ≤ v.x * v.x := by
    rcases Int.le_total 0 v.x with h | h
    · exact Int.mul_nonneg h h
    · have h2 : 0 ≤ (-v.x) * (-v.x) := Int.mul_nonneg (by omega) (by omega)
      rwa [Int.neg_mul_neg] at h2
  have hy : 0 ≤ v.y * v.y := by
    rcases Int.le_total 0 v.y with h | h
    · exact Int.mul_nonneg h h
    · have h2 : 0 ≤ (-v.y) * (-v.y) := Int.mul_nonneg (by omega) (by omega)
      rwa [Int.neg_mul_neg] at h2
  simp only [normSq, dot]
  omega

/-- **The solenoidal current does no work.** `(Q g) · g = 0` for every gradient
`g` and every strength `ω`: the antisymmetric operator produces a flow
everywhere orthogonal to `g`, so it leaves free energy exactly unchanged. This
is the algebraic heart of "the circulation is conservative" (`§1`, `§3`). -/
theorem solenoidal_orthogonal (ω : Int) (g : Vec2) : dot (solenoidal ω g) g = 0 := by
  simp only [dot, solenoidal]
  rw [Int.neg_mul, show ω * g.y * g.x = ω * g.x * g.y from by ac_rfl,
    Int.add_right_neg]

/-- **Free-energy descent rate.** The work of the full flow against the gradient
is exactly the dissipative term `-γ‖g‖²`; the solenoidal part contributes
nothing. Since `‖g‖² ≥ 0`, along the flow `dF/dt = g · f = -γ‖g‖² ≤ 0` for
`γ ≥ 0`: free energy is non-increasing, and the circulation is "free". -/
theorem flow_work_eq_dissipation (γ ω : Int) (g : Vec2) :
    dot (flow γ ω g) g = -(γ * g.normSq) := by
  show (ω * g.y + -(γ * g.x)) * g.x + (-(ω * g.x) + -(γ * g.y)) * g.y
     = -(γ * (g.x * g.x + g.y * g.y))
  rw [Int.add_mul, Int.add_mul, Int.neg_mul, Int.neg_mul, Int.neg_mul, Int.mul_add,
    show ω * g.y * g.x = ω * g.x * g.y from by ac_rfl,
    show γ * (g.x * g.x) = γ * g.x * g.x from by ac_rfl,
    show γ * (g.y * g.y) = γ * g.y * g.y from by ac_rfl]
  omega

/-- **Detailed balance iff no solenoid.** For a nonzero gradient, the solenoidal
current vanishes exactly when `ω = 0`. Equilibrium (detailed balance) is
precisely the absence of the antisymmetric drive. -/
theorem detailed_balance_iff (ω : Int) (g : Vec2) (hg : g ≠ ⟨0, 0⟩) :
    solenoidal ω g = ⟨0, 0⟩ ↔ ω = 0 := by
  constructor
  · intro h
    obtain ⟨gx, gy⟩ := g
    simp only [solenoidal, Vec2.mk.injEq] at h
    obtain ⟨h1, h2⟩ := h            -- h1 : ω * gy = 0, h2 : -(ω * gx) = 0
    have h2' : ω * gx = 0 := by omega
    rcases Int.mul_eq_zero.mp h1 with hω | hgy
    · exact hω
    · rcases Int.mul_eq_zero.mp h2' with hω | hgx
      · exact hω
      · exact absurd (show (⟨gx, gy⟩ : Vec2) = ⟨0, 0⟩ by subst hgx; subst hgy; rfl) hg
  · intro h; subst h; simp [solenoidal, Int.zero_mul]

/-- The denominator-cleared entropy-production rate `γ·σ = 2·ω²·precision`
(section 6 gives `σ = 2ω²·precision/γ`; clearing `γ` keeps everything integral).
-/
def entropyProduction (precision ω : Int) : Int := 2 * (ω * ω) * precision

/-- **Entropy production is nonnegative** for a nonnegative precision — the
second-law-flavoured statement that the steady state cannot destroy entropy. -/
theorem entropyProduction_nonneg (precision ω : Int) (hp : 0 ≤ precision) :
    0 ≤ entropyProduction precision ω := by
  have hωω : 0 ≤ ω * ω := by
    rcases Int.le_total 0 ω with h | h
    · exact Int.mul_nonneg h h
    · have h2 : 0 ≤ (-ω) * (-ω) := Int.mul_nonneg (by omega) (by omega)
      rwa [Int.neg_mul_neg] at h2
  have h2 : (0 : Int) ≤ 2 := by decide
  exact Int.mul_nonneg (Int.mul_nonneg h2 hωω) hp

/-- **Entropy production vanishes iff detailed balance.** For a strictly positive
precision, the entropy-production rate is zero exactly when `ω = 0`: the
sustained current — and its irreversible cost — is present precisely out of
equilibrium. -/
theorem entropyProduction_zero_iff (precision ω : Int) (hp : 0 < precision) :
    entropyProduction precision ω = 0 ↔ ω = 0 := by
  simp only [entropyProduction]
  constructor
  · intro h
    -- 2 * (ω*ω) * precision = 0 and precision > 0 ⟹ ω*ω = 0 ⟹ ω = 0
    have hωω : ω * ω = 0 := by
      rcases Int.mul_eq_zero.mp h with h' | h'
      · rcases Int.mul_eq_zero.mp h' with h2 | h2
        · exact absurd h2 (by decide)
        · exact h2
      · omega
    rcases Int.mul_eq_zero.mp hωω with h' | h' <;> exact h'
  · intro h; subst h; simp

end Vec2

end ActiveInferenceFormalℤ
