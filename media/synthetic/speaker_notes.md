# Active Inference Synthetic

*From beliefs to action: a worked introduction*

*Total duration: 20:00*

## A working map of active inference

**Objectives**
- Small executable models; explicit scientific boundaries

### Beat `b01` — 0:00
*Image: assets/slide_01.png*

> Why can the same probability landscape describe two different dynamical regimes? And when does learning improve a decision? This graphical abstract gives us a working map. At the top, compare stationary currents over the same density. In the middle, follow observation, inference, policy evaluation and action. At the bottom, keep specification, computation and proof distinct. This is the revised Synthetic manuscript; the linked release contains this paper and lecture, while Zenodo preserves the earlier published edition. In twenty minutes we will make these connections executable, using tested numerical models, selected Lean results and concrete model specifications. Read every result with its assumptions.

---

## Three questions, three mathematical objects

**Objectives**
- Inference, decision, and dynamics answer different questions

### Beat `b02` — 0:45
*Image: assets/slide_02.png*

> Keep three questions in view. What explains an observation? A posterior belief answers that inference question. Which action should come next? Expected free energy compares predicted outcomes using preferences and information gain. What maintains a stationary distribution? Drift, diffusion, current, and entropy production describe that dynamical regime. Variational and expected free energy are information theoretic quantities. Physical free energy needs a thermodynamic model and units. The shared vocabulary does not make these objects interchangeable. As you read the three cards, connect each question to its mathematical object.

---

## A generative model makes assumptions explicit

**Objectives**
- Prior × likelihood → joint distribution → posterior

### Beat `b03` — 1:21
*Image: assets/slide_03.png*

> Start with a hidden state and an observation. A prior describes uncertainty about the hidden state before the observation. A likelihood describes which observations each state tends to generate. Multiplying prior and likelihood produces the joint distribution. Summing over hidden states gives the evidence for the observed outcome. Bayes' rule then divides the appropriate joint probabilities by that evidence. In the repository's finite models, conditional distributions are stored in columns, so each column must sum to one. This orientation matters: transposing a plausible looking matrix can change the entire model. The examples reject invalid probabilities and impossible observations, instead of silently replacing them with an arbitrary belief.

---

## Variational free energy bounds surprise

**Objectives**
- F[q] = surprise + KL(q || posterior)

### Beat `b04` — 2:06
*Image: assets/slide_04.png*

> Now introduce a candidate belief, called q. Variational free energy compares this belief with the generative model after an observation has arrived. One decomposition is complexity minus accuracy: divergence from the prior, minus expected log likelihood. A second decomposition is especially revealing. Free energy equals the observation's surprise plus the divergence between the candidate belief and the exact posterior. Because this divergence is nonnegative on the stated support domain, free energy bounds surprise from above. When the candidate belief equals the posterior, the gap closes. This is an identity within the model. It does not say that every physical system computes Bayes' rule, or that minimizing an arbitrary scalar makes a system intelligent.

---

## Read the belief update as a numerical experiment

**Objectives**
- A closed-form posterior supplies an independent numerical oracle

### Beat `b05` — 2:48
*Image: assets/slide_05.png*

> Read the belief figure from left to right. The categorical belief moves from a uniform assignment toward the exact posterior. Free energy approaches the surprise reference line. The gap is posterior divergence. Check the answer independently using Bayes' rule and the complexity minus accuracy calculation. Their agreement supplies a numerical oracle. The descent algorithm needs safeguards and convergence checks. A lower bound by itself cannot guarantee convergence. Check the updates against the exact posterior. The changing belief and the shrinking gap should tell the same story.

---

## One landscape, two components of motion

**Objectives**
- Dissipative descent + solenoidal motion along contours

### Beat `b06` — 3:30
*Image: assets/slide_06.png*

> We now switch from a discrete belief to a continuous, two dimensional model state. The Gaussian contours define a dimensionless stationary potential, Phi. This is a function of coordinates, distinct from the variational functional of a recognition distribution. The drift is Q minus Gamma, acting on the gradient of Phi. Gamma supplies dissipation; antisymmetric Q supplies tangential motion. Along the noise-free drift, the potential decreases because the gradient is orthogonal to its solenoidal component. That geometric identity does not mean circulation has zero physical cost. Connecting these coordinates to beliefs, or scaling this potential to energy in joules, requires additional assumptions. Keep those bridges visible.

---

## A spiral is a drift trajectory, not a steady state

**Objectives**
- A deterministic spiral relaxes; a steady state describes an ensemble

### Beat `b07` — 4:16
*Image: assets/slide_07.png*

> The trajectory figure integrates those drift fields. With no solenoidal term, the path relaxes radially toward the mode. With circulation, the path spirals inward while the landscape still decreases. The numerical integrator is a fixed step fourth order Runge Kutta method, checked against the available linear closed form. Two cautions make the picture more useful. First, total rotation depends on the chosen time window; angular velocity is the more intrinsic diagnostic in this isotropic example. Second, both deterministic trajectories relax toward the mode. The spiral does not depict a particle moving forever on a stable orbit. A non-equilibrium steady state is an ensemble property of the corresponding stochastic model, which we examine next.

---

## Watch a transient density relax

**Objectives**
- A displaced ensemble mean relaxes while covariance stays fixed

### Beat `b08` — 5:07
*Image: assets/slide_08.png*

> Add matched diffusion to the linear drift. The stationary covariance is inverse precision in both regimes. To see a transient, begin with that covariance but displace the Gaussian mean. The contour cloud now changes position: its mean follows the relaxing drift, radially on the left and spirally on the right. The clock is model time, not an inference iteration. This moving density is not stationary, even though the coefficients are constant. Individual noisy paths would fluctuate; these contours show the ensemble distribution. A stationary density instead stops changing with time. It may nevertheless support a probability current. The next animation isolates that different question.

---

## The same stationary density, different currents

**Objectives**
- Stationary: divergence-free current. Equilibrium: zero current.

### Beat `b09` — 5:54
*Image: assets/slide_09.png*

> Here every frame is a stationary model with the same Gaussian density. We sweep a known drive parameter; this clock is not physical time. The arrows are probability current, not individual particle trajectories. At zero drive the current vanishes everywhere and detailed balance holds in this even-coordinate model. On either side, the arrows circulate with zero divergence. Reversing drive reverses circulation while preserving the density, and the entropy-production curve depends on its square. Notice that current vanishes at the mode even in the driven regime. One zero arrow therefore cannot establish equilibrium. A histogram sees the shared density; temporal and reversal statistics distinguish the processes.

---

## Entropy production: what the formula measures

**Objectives**
- Irreversibility is model-specific; physical units require assumptions

### Beat `b10` — 6:41
*Image: assets/slide_10.png*

> Entropy production measures the difference between forward and reversed path statistics. For this elliptic, stationary diffusion with even coordinates, the current formula gives twice squared drive times precision, divided by dissipation. Positive precision and dissipation are essential. Momentum variables, a reversed magnetic field or a different reverse protocol require a separate analysis; a circulating phase-space current is not universally dissipative. Nonzero drive establishes non-equilibrium here, not automatically far from equilibrium. Scaling the informational rate to entropy or power requires temperature, Boltzmann's constant and a compatible physical model. This simulation does not measure metabolism or a computer's energy budget. The paper cites stationary diffusion theory and stochastic thermodynamics for these distinctions.

---

## The Markov blanket is a conditional statement

**Objectives**
- Marginal dependence can coexist with conditional independence

### Beat `b11` — 7:33
*Image: assets/slide_11.png*

> We now ask how a model separates a system from its surroundings. The Markov blanket example partitions variables into external, sensory, active, and internal roles. The defining statistical condition is that external and internal states become independent after conditioning on the blanket variables. This allows marginal dependence and conditional independence to coexist. The figure makes that contrast visible: ordinary correlations can connect external and internal variables, while a particular entry of the Gaussian precision matrix is zero. For a nonsingular Gaussian distribution, that zero identifies conditional independence given the remaining variables. The model therefore demonstrates a precise screening relation, rather than a literal wall separating two independent parts of the world.

---

## What a blanket does not establish

**Objectives**
- Statistical screening alone does not establish causal direction

### Beat `b12` — 8:22
*Image: assets/slide_12.png*

> Statistical screening alone does not assign causal direction or prove that internal states represent external states. Those claims require additional dynamical or interventional assumptions. Here we can establish something precise: conditioning on the full blanket removes the relevant Gaussian dependence. Conditioning on only part need not do so. Compare the marginal and conditional panels before moving on. A blanket is useful because the conditioning statement can be tested; it is not a literal wall or a certificate of cognition.

---

## A native Gaussian bridge has its own model

**Objectives**
- Formal transfer binds one specified matrix and conditioning rule

### Beat `b13` — 8:55
*Image: assets/slide_13.png*

> The revised blanket figure also separates a canonical Gaussian model selected for its formal correspondence. Its precision matrix has four on the diagonal, negative one on the blanket connections, and zero direct external to internal coupling. This is a distinct model from the original numerical example. The added panel makes the distinction explicit instead of silently transferring a theorem between different matrices. Conditional Gaussian calculations expose the screened relation, while a perturbed direct connection supplies a counterexample. Matching a concrete probability model to a formal statement requires this level of specificity: variable order, precision entries, conditioning variables, and the exact property being claimed.

---

## Act before the outcome is known

**Objectives**
- G(action) = − pragmatic value − epistemic value

### Beat `b14` — 9:38
*Image: assets/slide_14.png*

> Perception evaluates beliefs after an observation. Decision making evaluates possible observations before they arrive. Each candidate action has an outcome model. Combine that model with the present belief to predict outcomes. Then score the action using expected free energy. Our score is negative pragmatic value minus epistemic value. The pragmatic term averages log preferences over predicted outcomes. The epistemic term measures expected information gain about hidden states. These are distinct contributions to one objective. Lower expected free energy is preferred. The chosen likelihoods, preferences and available actions determine the resulting behavior. Read the two terms separately before comparing the bars.

---

## Preferences shift the explore-exploit balance

**Objectives**
- Preferences change the balance within one declared objective

### Beat `b15` — 10:24
*Image: assets/slide_15.png*

> The one step example compares an informative cue with an uninformative bet. With flat preferences, pragmatic values are equal, so the cue wins through information gain. Concentrate preferences enough, and the rewarding bet wins. The same score changes the balance without a separate exploration switch. These supplied matrices expose a mechanism, rather than explaining every intelligent action. Before leaving the figure, identify which bar changes when preferences change and which term describes information.

---

## Expected information gain has a concrete meaning

**Objectives**
- Information gain averages posterior changes over possible outcomes

### Beat `b16` — 10:58
*Image: assets/slide_16.png*

> To understand the epistemic term, imagine following each possible observation separately. For each observation, update the prior belief using Bayes' rule. Measure how far that posterior moves from the prior using relative entropy. Then average those changes with the predicted observation probabilities. This is the expected information gain, equal here to mutual information between the hidden state and the outcome. An observation independent of the hidden state leaves the posterior unchanged and contributes zero information. An informative observation can contribute positive information even before we know which outcome will occur. Notice the support conditions: impossible observations cannot be treated as ordinary posterior updates, and a logarithm involving zero probability requires an explicit convention.

---

## Planning evaluates whole observation branches

**Objectives**
- Terminal preference + cumulative information over observation histories

### Beat `b17` — 11:52
*Image: assets/slide_17.png*

> The planning example extends actions into short, fixed sequences. Each policy induces a distribution over observation sequences. Follow every possible branch, update the posterior along that branch, and average the evaluated contributions. The pragmatic term concerns the terminal outcome. The epistemic term scores information across the whole observation sequence. This is one specific planning objective. Other active inference models may use different objectives. Here the horizon and outcome spaces are small, so we can enumerate branches exactly. There is no sampling uncertainty. Longer horizons grow combinatorially. This exact calculation is an explanatory reference, not a claim of scalable planning.

---

## When information changes a decision

**Objectives**
- Information in nats; contingent decision value in utility units

### Beat `b18` — 12:42
*Image: assets/slide_18.png*

> Information gain and decision value answer different questions. Consider two equally likely states and two commitments, each paying one utility unit only when it matches the state. Without a cue, the best expected payoff is one half. A ninety percent reliable cue followed by the matching commitment raises expected payoff to point nine. The gross value of information is point four; subtracting a point fifteen observation cost leaves point two five. Watch the cue accuracy sweep: decision value changes in utility units, while mutual information changes in nats. An informative cue can have zero decision value when payoffs do not depend on the hidden state. Exhaustive enumeration of all finite feedback policies independently checks the calculation. This comparison assumes a fixed state, known likelihood and utilities, and unchanged available actions. Next we connect such contingent commitments to the perception-action loop.

---

## Close the perception-action loop

**Objectives**
- Select → observe → update → re-evaluate → commit

### Beat `b19` — 13:43
*Image: assets/slide_19.png*

> The synthetic agent demonstration makes actions and outcomes sequential. Initially, the agent is uncertain which hidden context holds. It can obtain a cue or choose a commitment action. After selecting an initial action, it receives one explicitly specified observation and updates its belief by Bayes' rule. It then evaluates the available commitment actions again under the posterior. The environment gives those commitments state dependent consequences: choosing the action that matches the hidden context produces reward, while choosing the other produces loss. This creates a setting in which information can change the next decision. The small example is deliberately transparent. It is a two stage model with supplied probabilities, not a trained general purpose autonomous system.

---

## A useful control removes information

**Objectives**
- An independent cue carries observations, but no context information

### Beat `b20` — 14:28
*Image: assets/slide_20.png*

> The informative cue identifies the hidden context, allowing different observations to lead to different commitment decisions. Compare that with a cue replaced by a fair coin independent of context. The coin still generates observations, but those observations carry no information about the hidden state. The posterior consequently stays at the prior, and any change in behavior cannot be credited to learning the context. This comparison separates receiving a signal from receiving useful evidence. It also separates rerunning a decision rule from genuinely observation dependent behavior. The repository represents branches explicitly, making both the informative case and its counterexample reproducible. Neither the selected branch nor its clean outcome should be mistaken for a population estimate of real world agent performance.

---

## Hierarchical inference predicts down and updates up

**Objectives**
- Context → state → observation; condition the joint to infer upward

### Beat `b21` — 15:18
*Image: assets/slide_21.png*

> The hierarchy example adds a second hidden level. Context influences a lower level state, and that state influences an observation. Top down prediction starts with the context prior, propagates it through the state given context distribution, and then through the observation given state distribution. Bottom up inference conditions the full joint distribution on an actual observation. Marginalizing the resulting posterior joint gives revised beliefs at both hidden levels. This is exact finite Bayesian conditioning, so the model provides an unusually clear reference for what a hierarchical update means. The hierarchy is about the factorization of a probability model. It does not require us to assume a particular neural architecture, predictive coding implementation, or learning algorithm.

---

## Learn from the limits of a hierarchy

**Objectives**
- Hierarchical conditioning is exact; neural implementation is not assumed

### Beat `b22` — 16:08
*Image: assets/slide_22.png*

> A lower level observation can revise higher level context through the conditional model. If either connecting channel is uninformative, evidence cannot recover the missing link. Direct enumeration of the joint distribution independently checks the posterior marginals. This validates finite conditioning, not a biological implementation, learned parameters, or an automatic benefit from greater depth. Trace the figure downward for prediction, then upward for inference, and identify the channel each step needs.

---

## Finite path proofs state their support conditions

**Objectives**
- Finite path fluctuation identity: normalized laws and positive support

### Beat `b23` — 16:42
*Image: assets/slide_23.png*

> The revised formal layer imports finite path thermodynamics from the same pinned FEP Formal library. A protocol supplies normalized forward and aligned reverse path laws, with an involutive reversal. Their Kullback Leibler divergence is nonnegative. With strictly positive forward and reverse support, the expected exponential of minus the path log ratio equals one. The displayed Lean declaration makes those support hypotheses explicit. This is a finite path-space identity, not a proof of the continuous Ornstein Uhlenbeck entropy-production rate. A physical interpretation also requires the correct reverse protocol. Lean checks the stated proposition; numerical correspondence and scientific interpretation remain separate checks. Our local wrappers preserve that boundary.

---

## A history channel bridges planning objectives

**Objectives**
- History-channel normalization adds a policy-independent constant

### Beat `b24` — 17:30
*Image: assets/slide_24.png*

> There is also a precise route from the two step planner to a one channel formal information statement. Treat the pair of observations as one history outcome. Its likelihood is the product of the two action likelihoods conditional on the hidden state. Normalize the history preference using the terminal preference and the number of possible first observations. In this binary example, that normalization introduces an additive natural logarithm of two into the expected free energy. The constant preserves policy ranking. This construction does not identify the local terminal objective with a sum of repeatedly applied one step objectives. The channel and preference normalization are part of the bridge.

---

## GNN specifications meet numerical checks

**Objectives**
- GNN parsing checks exact model parameters; it is not backend execution

### Beat `b25` — 18:17
*Image: assets/slide_25.png*

> The repository now includes two Generalized Notation Notation specifications. The continuous file declares a two dimensional state, precision, dissipation, drive alternatives, diffusion and current. Q underscore OU is antisymmetric drive, not a process-noise covariance. The finite file declares cue and bet channels, a prior and normalized preferences; rows are outcomes and columns are states. An optional bridge uses the real upstream parser, checks exact values and dimensions against our numerical demos, and rejects deliberately wrong dissipation or state dimension. Parsing does not execute a simulation backend. Nor does it transport a Lean theorem automatically. Record support, orientation, units and control assumptions before extending the model.

---

## Your map of the Institute ecosystem

**Objectives**
- Synthetic teaches; FEP_Formal proves; GNN specifies models

### Beat `b26` — 19:10
*Image: assets/slide_26.png*

> Choose the next resource by your question. Synthetic supplies the paper, Python package and teaching experiments. FEP Formal supplies the pinned mathematical library. GNN supplies model specification tools. Our optional parser bridge is separate from the ordinary numerical runtime. The Active Inference Ontology supports terminology. Fundamentals and courses support study. Cognitive supplies examples of computational models. Active Inference Journal connects videos with searchable transcripts. The release links this revised paper, lecture, slides, captions and reproducibility sources. The earlier published paper remains archived on Zenodo. Start with one model, change one assumption, and test a failure case. Specification communicates. Computation evaluates. Proof establishes a proposition. Scientific interpretation requires evidence.

---

*Generated from 'Active Inference Synthetic' — 26 beat(s) across 26 section(s).*