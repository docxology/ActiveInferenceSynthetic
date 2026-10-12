"""Build focused scientific plates with explicit reading order and model roles."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

__all__ = ["build_slide"]

GUIDES = [
    (
        "THE CENTRAL QUESTION",
        "When does learning change a choice?",
        [
            "Beliefs explain observations",
            "Preferences evaluate outcomes",
            "Current distinguishes dynamics",
        ],
    ),
    (
        "KEEP THE OBJECTS DISTINCT",
        "Three questions; three objects",
        [
            "Inference: posterior belief",
            "Decision: expected free energy",
            "Dynamics: density and current",
        ],
    ),
    (
        "BUILD THE MODEL",
        "Prior × likelihood → posterior",
        ["Declare hidden states", "Specify how observations arise", "Condition on actual evidence"],
    ),
    (
        "READ THE GAP",
        "F[q] = surprise + posterior KL",
        [
            "The curve approaches its bound",
            "The gap is belief error",
            "The identity needs its support domain",
        ],
    ),
    (
        "CHECK THE ANSWER",
        "Compare belief with exact Bayes",
        [
            "Uniform starting belief",
            "Posterior calculated independently",
            "Descent needs convergence checks",
        ],
    ),
    (
        "READ THE FLOW",
        "Downhill + along-contour motion",
        [
            "Dissipation lowers the landscape",
            "Antisymmetry gives tangent motion",
            "Both terms belong to the drift",
        ],
    ),
    (
        "FOLLOW THE TRAJECTORY",
        "A spiral still relaxes",
        [
            "Paths approach the mode",
            "Rotation depends on the time window",
            "Steady state describes an ensemble",
        ],
    ),
    (
        "WATCH THE TRANSIENT",
        "Changing density is not stationarity",
        ["Mean starts displaced", "Covariance stays fixed", "Contours show an ensemble"],
    ),
    (
        "SWEEP THE DRIVE",
        "A parameter sweep is not a time trajectory",
        [
            "Equilibrium: current zero everywhere",
            "NESS: divergence-free circulation",
            "Density stays the same across this sweep",
        ],
    ),
    (
        "KEEP THE UNITS",
        "Irreversibility in a specified model",
        [
            "Circulation reversal preserves cost",
            "Physical units need conventions",
            "Positive rate does not prove cognition",
        ],
    ),
    (
        "CONDITION ON THE BLANKET",
        "Marginal ≠ conditional dependence",
        [
            "External and internal can correlate",
            "Full conditioning removes dependence",
            "Gaussian precision exposes screening",
        ],
    ),
    (
        "TEST THE BOUNDARY",
        "Screening is a statistical statement",
        [
            "Partial conditioning may not screen",
            "Causal direction needs more assumptions",
            "Representation is a separate claim",
        ],
    ),
    (
        "MATCH THE EXACT MODEL",
        "One native Gaussian bridge",
        [
            "A distinct specified precision matrix",
            "Conditioned cross-covariance is zero",
            "Perturbation supplies a counterexample",
        ],
    ),
    (
        "SCORE POSSIBLE ACTIONS",
        "G = − pragmatic − epistemic",
        [
            "Predict outcomes before observing",
            "Preferences score desirable outcomes",
            "Information scores posterior change",
        ],
    ),
    (
        "CHANGE PREFERENCES",
        "The same objective changes the choice",
        [
            "Flat preference: cue wins",
            "Concentrated preference: bet wins",
            "Matrices define this demonstration",
        ],
    ),
    (
        "AVERAGE OVER OBSERVATIONS",
        "Information gain is expected updating",
        [
            "Predict every possible observation",
            "Condition a posterior for each",
            "Average divergence from the prior",
        ],
    ),
    (
        "FOLLOW WHOLE HISTORIES",
        "Terminal value + history information",
        [
            "Enumerate each observation branch",
            "Update beliefs along the branch",
            "Average after evaluating the branch",
        ],
    ),
    (
        "CHECK INSTRUMENTAL VALUE",
        "Information can change a commitment",
        [
            "Compare immediate and feedback choices",
            "Subtract the observation cost",
            "Keep utility and nats separate",
        ],
    ),
    (
        "CLOSE THE LOOP",
        "Observe → update → choose again",
        [
            "Commitment has state-dependent payoff",
            "A cue changes the posterior",
            "A later decision uses that evidence",
        ],
    ),
    (
        "REMOVE THE INFORMATION",
        "Observation alone is not learning",
        [
            "Replace the cue with a fair coin",
            "The posterior remains the prior",
            "Useful evidence changes beliefs",
        ],
    ),
    (
        "TRACE THE TWO DIRECTIONS",
        "Predict down; condition upward",
        [
            "Context predicts hidden state",
            "State predicts observation",
            "Joint conditioning revises both levels",
        ],
    ),
    (
        "FIND THE MISSING LINK",
        "An uninformative channel blocks updating",
        [
            "Inspect both conditional models",
            "Check by direct joint enumeration",
            "Finite conditioning is not a neural claim",
        ],
    ),
    (
        "LINK THE EVIDENCE",
        "Theorem → model → interpretation",
        [
            "Lean checks the stated hypotheses",
            "Numerics need a model correspondence",
            "Scientific meaning needs justification",
        ],
    ),
    (
        "NORMALIZE THE HISTORY",
        "An explicit bridge preserves ranking",
        [
            "Treat observations as one outcome",
            "Normalize terminal preferences",
            "The added constant is policy-independent",
        ],
    ),
    (
        "READ THE SPECIFICATIONS",
        "Parsing checks representation; execution needs a bridge",
        [
            "Outcome rows; state columns",
            "Drive Q_ou is not noise covariance",
            "Wrong parameters and dimensions fail",
        ],
    ),
    (
        "YOUR NEXT STEP",
        "Reproduce one model; change one assumption",
        [
            "Synthetic: paper and Python examples",
            "FEP_Formal: pinned Lean reference",
            "GNN: optional model specification",
        ],
    ),
]

CROPS = {
    3: (0.50, 0.08, 1.00, 1.00),
    4: (0.00, 0.08, 0.48, 1.00),
    10: (0.00, 0.10, 0.66, 1.00),
    11: (0.33, 0.10, 0.66, 1.00),
    12: (0.66, 0.10, 1.00, 1.00),
    13: (0.00, 0.10, 0.48, 1.00),
    14: (0.49, 0.10, 1.00, 1.00),
    18: (0.00, 0.10, 0.67, 1.00),
    19: (0.66, 0.10, 1.00, 1.00),
    21: (0.00, 0.10, 0.67, 1.00),
}


def build_slide(root: Path, index: int, title: str, figure: str, section: str) -> Image.Image:
    """Compose a readable scientific slide with a source-faithful publication cover."""
    import json

    from lecturecreate.visuals.qr import qr_image

    font_path = root / "assets/DejaVuSans.ttf"

    def font(size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(str(font_path), size)

    def wrapped(text: str, size: int, width: int) -> str:
        lines, current = [], ""
        for word in text.split():
            candidate = (current + " " + word).strip()
            if draw.textbbox((0, 0), candidate, font=font(size))[2] > width:
                if not current:
                    raise ValueError(f"Unbreakable slide text: {word}")
                lines.append(current)
                current = word
            else:
                current = candidate
        return "\n".join([*lines, current])

    ink, teal, orange = "#163d43", "#007d82", "#b34e27"
    plate = Image.new("RGB", (1920, 1080), "#faf9f4")
    draw = ImageDraw.Draw(plate)
    if index == 0:
        publication = json.loads((root / "publication.json").read_text())
        primary = publication["primary"]
        with Image.open(root / "assets/paper_cover.png") as image:
            cover = ImageOps.contain(image.convert("RGB"), (780, 916))
        x, y = 84 + (780 - cover.width) // 2, 68 + (916 - cover.height) // 2
        draw.rectangle((x + 8, y + 8, x + cover.width + 8, y + cover.height + 8), fill="#deded7")
        plate.paste(cover, (x, y))
        draw.text((948, 92), primary["display_label"], font=font(23), fill=teal)
        heading = wrapped(primary["title"], 48, 880)
        draw.multiline_text((948, 152), heading, font=font(48), spacing=13, fill=ink)
        draw.text((948, 416), "Active Inference Synthetic", font=font(31), fill=ink)
        draw.multiline_text(
            (948, 472),
            "A worked introduction to beliefs,\ndecisions and dynamics",
            font=font(30),
            spacing=9,
            fill=ink,
        )
        for j, link in enumerate(publication["links"][:2]):
            yy = 600 + j * 210
            plate.paste(qr_image(link["url"], 164, quiet=4).convert("RGB"), (948, yy))
            draw.text((1140, yy + 12), link["label"], font=font(28), fill=ink)
            draw.multiline_text(
                (1140, yy + 65),
                wrapped(link["display_url"], 26, 650),
                font=font(26),
                spacing=8,
                fill="#b91c1c",
            )
        draw.text(
            (84, 1022),
            "PDF cover reproduced without changing its content",
            font=font(20),
            fill="#526b70",
        )
        draw.text(
            (948, 1022),
            "Scan in the video or click in the slide PDF",
            font=font(20),
            fill="#526b70",
        )
        return plate

    group = (
        "Inference"
        if index <= 4
        else "Dynamics"
        if index <= 9
        else "Statistical boundaries"
        if index <= 12
        else "Decision and control"
        if index <= 19
        else "Hierarchy"
        if index <= 21
        else "Formal transfer"
        if index <= 24
        else "Resources"
    )
    draw.text(
        (64, 30), f"ACTIVE INFERENCE SYNTHETIC   /   {group.upper()}", font=font(22), fill=teal
    )
    title_size = 52
    while draw.textbbox((0, 0), title, font=font(title_size))[2] > 1780:
        title_size -= 1
    if title_size < 36:
        raise ValueError(f"Title is too long: {title}")
    draw.text((64, 82), title, font=font(title_size), fill=ink)
    draw.line((64, 164, 1856, 164), fill="#cbd9d5", width=2)
    label, takeaway, guides = GUIDES[index]
    draw.rectangle((64, 210, 1290, 895), fill="white")
    draw.line((1322, 228, 1322, 867), fill="#cbd9d5", width=2)
    draw.text((1360, 236), "READ THE RESULT", font=font(23), fill=teal)
    for j, guide in enumerate(guides):
        yy = 328 + j * 173
        draw.line((1360, yy, 1406, yy), fill=orange, width=5)
        draw.multiline_text(
            (1360, yy + 22), wrapped(guide, 32, 468), font=font(32), spacing=12, fill=ink
        )
    if figure != "none":
        with Image.open(root / "sources/figures" / figure) as original:
            image = original.convert("RGB")
            if index in CROPS:
                w, h = image.size
                left, top, right, bottom = CROPS[index]
                image = image.crop(
                    (round(left * w), round(top * h), round(right * w), round(bottom * h))
                )
            fitted = ImageOps.contain(image, (1166, 620))
            plate.paste(fitted, (64 + (1226 - fitted.width) // 2, 243 + (620 - fitted.height) // 2))
    elif index == 22:
        source = (root / "sources/formal/ActiveInferenceFormal/Thermodynamics.lean").read_text()
        code = source[source.index("theorem finite_path_integral_fluctuation"):].split("\n\n")[0]
        draw.text((98, 285), "ACTUAL LEAN DECLARATION / PINNED FEP_FORMAL",
                  font=font(27), fill=teal)
        for line_index, line in enumerate(code.splitlines()):
            draw.text((98, 350 + line_index * 45), line, font=font(25), fill=ink)
    elif index == 24:
        for xx, name, heading in ((98, "ou_regimes.md", "CONTINUOUS OU"),
                                  (715, "finite_agent.md", "FINITE CUE / BET")):
            source = (root / "sources" / name).read_text()
            parameters = source.split("## InitialParameterization\n", 1)[1]
            parameters = parameters.split("\n##", 1)[0]
            draw.text((xx, 300), heading, font=font(27), fill=teal)
            draw.text((xx, 355), name, font=font(24), fill=orange)
            declaration = (
                "x[2,type=float]" if name == "ou_regimes.md" else "A_cue[2,2,type=float]"
            )
            if declaration not in source:
                raise ValueError(
                    "Displayed GNN declaration is absent from the frozen specification"
                )
            draw.text((xx, 400), declaration, font=font(22), fill=ink)
            for line_index, line in enumerate(parameters.strip().splitlines()):
                draw.text((xx, 440 + line_index * 55), line, font=font(22), fill=ink)
        draw.text((98, 755), "Upstream parser + exact demo values + dimension checks",
                  font=font(28), fill=ink)
        draw.text((98, 810), "Negative controls: wrong gamma and state dimension reject",
                  font=font(27), fill=teal)
    elif index == 25:
        rows = [
            ("Prove", "fep_formal"),
            ("Specify", "Generalized_Notation_Notation"),
            ("Define", "Active_Inference_Ontology"),
            ("Learn", "fundamentals"),
            ("Study", "courses"),
            ("Compute", "cognitive"),
            ("Explore", "ActiveInferenceJournal"),
        ]
        draw.text((98, 253), "github.com/ActiveInferenceInstitute/", font=font(27), fill=teal)
        for j, (role, name) in enumerate(rows):
            yy = 333 + j * 74
            draw.text((98, yy), role, font=font(29), fill=ink)
            draw.text((292, yy), name, font=font(29), fill=teal)
            draw.line((98, yy + 53, 1230, yy + 53), fill="#e1e8e4", width=1)
    else:
        nodes = {
            1: [
                ("INFERENCE", "What explains an observation?", "Posterior belief"),
                ("DECISION", "Which action comes next?", "Expected free energy"),
                ("DYNAMICS", "What is stationary?", "Density and current"),
            ],
            2: [
                ("PRIOR", "Before observing", "p(x)"),
                ("LIKELIHOOD", "How observations arise", "p(o | x)"),
                ("POSTERIOR", "After observing", "p(x | o)"),
            ],
            15: [
                ("PREDICT", "Possible observations", "q(o | action)"),
                ("CONDITION", "A posterior for each", "q(x | o, action)"),
                ("AVERAGE", "Weight every outcome", "Information gain"),
            ],
            22: [
                ("THEOREM", "Hypotheses and conclusion", "Lean kernel check"),
                ("MODEL", "The specified carrier", "Numerical oracle"),
                ("CLAIM", "Qualified interpretation", "Scientific evidence"),
            ],
            24: [
                ("SUPPORT", "Zero probabilities", "Declare conventions"),
                ("CARRIER", "Mathematical objects", "Match the model"),
                ("TRANSFER", "Specified conclusion", "Test the boundary"),
            ],
        }.get(index)
        if nodes is None:
            raise ValueError(f"No conceptual composition for chapter {index + 1}")
        for j, (heading, body, detail) in enumerate(nodes):
            xx = 98 + j * 395
            draw.text((xx, 360), heading, font=font(30), fill=teal)
            draw.multiline_text(
                (xx, 448), wrapped(body, 32, 344), font=font(32), spacing=13, fill=ink
            )
            draw.multiline_text(
                (xx, 650), wrapped(detail, 28, 344), font=font(28), spacing=10, fill=orange
            )
            if j < 2:
                draw.line((xx + 365, 340, xx + 365, 755), fill="#d7e2dd", width=2)
    draw.text((64, 929), label, font=font(22), fill=teal)
    draw.text((64, 967), takeaway, font=font(36), fill=ink)
    draw.text((64, 1030), f"Source: Synthetic / {section}", font=font(20), fill="#526b70")
    draw.text((1735, 1030), f"{index + 1:02d} / 26", font=font(20), fill="#526b70")
    draw.rectangle((0, 1071, round(1920 * (index + 1) / 26), 1080), fill=teal)
    return plate
