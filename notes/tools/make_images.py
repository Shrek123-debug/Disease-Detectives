import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, FancyArrowPatch, Polygon

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
for f in ["Arial.ttf", "Arial Bold.ttf", "Arial Italic.ttf"]:
    p = "/System/Library/Fonts/Supplemental/" + f
    if os.path.exists(p):
        fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Arial"
plt.rcParams["axes.unicode_minus"] = False

BLUE, ORANGE, GREEN, RED, GRAY, PURPLE = "#2b6cb0", "#dd8a1f", "#2f9e5b", "#c53030", "#6b7280", "#7c4dbb"
LBLUE, LORANGE, LGREEN, LRED, LGRAY, LPURPLE = "#dbeafe", "#fde8c8", "#d5f0df", "#fbd5d5", "#eceff3", "#e9defa"


def new(w, h, title, sub=None):
    fig = plt.figure(figsize=(w, h), dpi=250)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.text(w / 2, h - 0.25, title, ha="center", va="center", fontsize=15, fontweight="bold")
    if sub:
        ax.text(w / 2, h - 0.52, sub, ha="center", va="center", fontsize=9.5, color=GRAY)
    return fig, ax


def box(ax, x, y, w, h, txt="", fc="white", ec="black", fs=10, bold=False, lw=1.2, color="black", ha="center", va="center", pad=0):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw))
    if txt:
        tx = x + w / 2 if ha == "center" else x + 0.08
        ax.text(tx, y + h / 2, txt, ha=ha, va=va, fontsize=fs, fontweight="bold" if bold else "normal", color=color, linespacing=1.25)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=250, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print("saved", name)


# ---------------------------------------------------------------- 01 exposure 2x2
def img01():
    a, b, c, d = 30, 20, 10, 40
    N = a + b + c + d
    ill, well = a + c, b + d
    ar1, ar0 = a / (a + b), c / (c + d)
    rr = ar1 / ar0
    orr = a * d / (b * c)
    rd = ar1 - ar0
    af = (rr - 1) / rr
    ea, eb, ec_, ed = (a + b) * ill / N, (a + b) * well / N, (c + d) * ill / N, (c + d) * well / N
    chi = sum((o - e) ** 2 / e for o, e in [(a, ea), (b, eb), (c, ec_), (d, ed)])
    W, H = 9.6, 7.0
    fig, ax = new(W, H, "Exposure 2x2 table (outbreak / cohort)", "Rows = exposed or not.  Columns = got sick or not.  Example: 100 people at a picnic ate (or skipped) the potato salad.")
    # table
    x0, y0, cw, ch = 1.6, 3.35, 1.15, 0.75
    ax.text(x0 + cw, y0 + 3 * ch + 0.1, "Ill", ha="center", fontsize=11, fontweight="bold")
    ax.text(x0 + 2 * cw, y0 + 3 * ch + 0.1, "Well", ha="center", fontsize=11, fontweight="bold")
    ax.text(x0 + 3 * cw, y0 + 3 * ch + 0.1, "Total", ha="center", fontsize=11, fontweight="bold")
    # coordinates: columns x0+0.5cw ... use cells
    cells = [(0, 0, f"a = {a}", LORANGE), (1, 0, f"b = {b}", LBLUE), (0, 1, f"c = {c}", LBLUE), (1, 1, f"d = {d}", LORANGE)]
    for (cx, ry, t, col) in [(0, 2, f"a = {a}", LORANGE), (1, 2, f"b = {b}", LBLUE), (0, 1, f"c = {c}", LBLUE), (1, 1, f"d = {d}", LORANGE)]:
        box(ax, x0 + 0.5 * cw + cx * cw, y0 + ry * ch - 0.0, cw, ch, t, fc=col, fs=12, bold=True)
    # rewrite: simpler explicit layout
    ax.cla(); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.text(W / 2, H - 0.25, "Exposure 2x2 table (outbreak / cohort)", ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(W / 2, H - 0.52, "Rows = exposed or not.  Columns = got sick or not.  Example: 100 people at a picnic, some ate the potato salad.", ha="center", fontsize=9.2, color=GRAY)
    X, Y, cw, ch = 1.9, 4.1, 1.1, 0.8
    heads = ["Ill", "Well", "Total"]
    for i, h in enumerate(heads):
        ax.text(X + (i + 0.5) * cw, Y + 2 * ch + 0.22, h, ha="center", fontsize=11, fontweight="bold")
    rows = [("Ate salad\n(exposed)", [a, b, a + b], [LORANGE, LBLUE, LGRAY]), ("Did not eat\n(unexposed)", [c, d, c + d], [LBLUE, LORANGE, LGRAY])]
    letters = [["a", "b"], ["c", "d"]]
    for r, (lab, vals, cols) in enumerate(rows):
        yy = Y + (1 - r) * ch
        ax.text(X - 0.1, yy + ch / 2, lab, ha="right", va="center", fontsize=10, fontweight="bold")
        for k in range(3):
            t = f"{letters[r][k]} = {vals[k]}" if k < 2 else f"{vals[k]}"
            box(ax, X + k * cw, yy, cw, ch, t, fc=cols[k], fs=12, bold=True)
    yy = Y - ch
    ax.text(X - 0.1, yy + ch / 2, "Total", ha="right", va="center", fontsize=10, fontweight="bold")
    for k, v in enumerate([ill, well, N]):
        box(ax, X + k * cw, yy, cw, ch, str(v), fc=LGRAY, fs=12, bold=True)
    # right: formulas
    fx = 5.6
    lines = [
        ("Attack rate (exposed) = a/(a+b)", f"= {a}/{a + b} = {ar1 * 100:.0f}%", BLUE),
        ("Attack rate (unexposed) = c/(c+d)", f"= {c}/{c + d} = {ar0 * 100:.0f}%", BLUE),
        ("Risk ratio  RR = AR exposed / AR unexposed", f"= {ar1 * 100:.0f}/{ar0 * 100:.0f} = {rr:.1f}", RED),
        ("Odds ratio  OR = (a x d) / (b x c)", f"= ({a}x{d})/({b}x{c}) = {orr:.1f}", RED),
        ("Risk difference = AR exp - AR unexp", f"= {ar1 * 100:.0f}% - {ar0 * 100:.0f}% = {rd * 100:.0f} points", GREEN),
        ("Attributable fraction (exposed) = (RR-1)/RR", f"= ({rr:.1f}-1)/{rr:.1f} = {af * 100:.1f}%", GREEN),
    ]
    yy = H - 1.05
    for t, v, col in lines:
        ax.text(fx, yy, t, fontsize=9.6, fontweight="bold", color=col, va="center")
        ax.text(fx + 0.15, yy - 0.26, v, fontsize=10.5, va="center")
        yy -= 0.62
    # bottom: meaning + chi square
    ax.text(0.35, 2.0, "What the numbers mean", fontsize=11, fontweight="bold")
    mean = [
        f"RR = {rr:.1f}: salad eaters were {rr:.1f} times as likely to get sick.  RR = 1 means no link; RR > 1 = risk factor; RR < 1 = protective.",
        f"AF = {af * 100:.1f}%: about {af * 100:.0f}% of illness among salad eaters is blamed on the salad.",
        f"Chi-square: expected for each cell = (row total x column total) / N.   Expected a = {a + b} x {ill}/{N} = {ea:.0f}, b = {eb:.0f}, c = {ec_:.0f}, d = {ed:.0f}.",
        f"Chi-square = sum of (observed - expected)^2 / expected = 10^2/{ea:.0f} + 10^2/{eb:.0f} + 10^2/{ec_:.0f} + 10^2/{ed:.0f} = {chi:.2f}.",
        f"df = (rows-1)(columns-1) = 1.  Critical value at p = 0.05 is 3.84.  {chi:.2f} > 3.84, so the link is statistically significant.",
        "Use OR (not RR) when the study is case-control.  OR is about equal to RR only when the disease is rare.",
    ]
    yy = 1.65
    for m in mean:
        ax.text(0.35, yy, "- " + m, fontsize=8.6, va="center")
        yy -= 0.27
    save(fig, "01_exposure_2x2.png")


# ---------------------------------------------------------------- 02 diagnostic 2x2
def img02():
    TP, FP, FN, TN = 90, 50, 10, 850
    N = TP + FP + FN + TN
    sick, healthy = TP + FN, FP + TN
    sens, spec = TP / sick, TN / healthy
    ppv, npv = TP / (TP + FP), TN / (TN + FN)
    prev = sick / N
    acc = (TP + TN) / N
    W, H = 11.2, 7.0
    fig, ax = new(W, H, "Diagnostic (screening) test 2x2 table", "Columns = truth.  Rows = what the test said.  Example: 1,000 people screened.")
    X, Y, cw, ch = 2.0, 3.7, 1.3, 0.85
    ax.text(X + cw / 2, Y + 2 * ch + 0.45, "Truly sick", ha="center", fontsize=10.5, fontweight="bold")
    ax.text(X + 1.5 * cw, Y + 2 * ch + 0.45, "Truly healthy", ha="center", fontsize=10.5, fontweight="bold")
    ax.text(X + 2.5 * cw, Y + 2 * ch + 0.45, "Total", ha="center", fontsize=10.5, fontweight="bold")
    data = [("Test positive (+)", [("TP", TP, LGREEN), ("FP", FP, LRED), (None, TP + FP, LGRAY)]),
            ("Test negative (-)", [("FN", FN, LRED), ("TN", TN, LGREEN), (None, FN + TN, LGRAY)])]
    for r, (lab, row) in enumerate(data):
        yy = Y + (1 - r) * ch
        ax.text(X - 0.1, yy + ch / 2, lab, ha="right", va="center", fontsize=10, fontweight="bold")
        for k, (nm, v, col) in enumerate(row):
            t = f"{nm} = {v}" if nm else str(v)
            box(ax, X + k * cw, yy, cw, ch, t, fc=col, fs=12, bold=True)
    yy = Y - ch
    ax.text(X - 0.1, yy + ch / 2, "Total", ha="right", va="center", fontsize=10, fontweight="bold")
    for k, v in enumerate([sick, healthy, N]):
        box(ax, X + k * cw, yy, cw, ch, str(v), fc=LGRAY, fs=12, bold=True)
    # column brackets
    ax.annotate("", xy=(X + 0.5 * cw, Y + 2 * ch + 0.25), xytext=(X + 0.5 * cw, Y + 2 * ch + 0.25))
    ax.text(X + 0.5 * cw, Y - ch - 0.3, "Sensitivity:\ngo DOWN this column", ha="center", va="top", fontsize=8.5, color=BLUE, fontweight="bold")
    ax.text(X + 1.5 * cw, Y - ch - 0.3, "Specificity:\ngo DOWN this column", ha="center", va="top", fontsize=8.5, color=BLUE, fontweight="bold")
    ax.text(X + 3 * cw + 0.12, Y + 1.5 * ch, "PPV goes ACROSS\nthis row", ha="left", va="center", fontsize=8.5, color=PURPLE, fontweight="bold")
    ax.text(X + 3 * cw + 0.12, Y + 0.5 * ch, "NPV goes ACROSS\nthis row", ha="left", va="center", fontsize=8.5, color=PURPLE, fontweight="bold")
    # formulas right
    fx = 7.5
    items = [
        ("Sensitivity = TP/(TP+FN)", f"= {TP}/{sick} = {sens * 100:.0f}%", BLUE, "of the SICK, % the test catches"),
        ("Specificity = TN/(TN+FP)", f"= {TN}/{healthy} = {spec * 100:.1f}%", BLUE, "of the HEALTHY, % the test clears"),
        ("PPV = TP/(TP+FP)", f"= {TP}/{TP + FP} = {ppv * 100:.1f}%", PURPLE, "of POSITIVES, % really sick"),
        ("NPV = TN/(TN+FN)", f"= {TN}/{TN + FN} = {npv * 100:.1f}%", PURPLE, "of NEGATIVES, % really healthy"),
    ]
    yy = H - 1.0
    for t, v, col, note in items:
        ax.text(fx, yy, t, fontsize=9.4, fontweight="bold", color=col, va="center")
        ax.text(fx, yy - 0.23, v, fontsize=9.5, va="center")
        ax.text(fx, yy - 0.43, note, fontsize=8.2, va="center", color=GRAY)
        yy -= 0.78
    ax.text(0.3, 1.95, "Rules and meaning", fontsize=11, fontweight="bold")
    notes = [
        f"Prevalence = sick/total = {sick}/{N} = {prev * 100:.0f}%.  Accuracy = (TP+TN)/N = {acc * 100:.1f}%.",
        "Sensitivity and specificity do NOT change with prevalence.  PPV rises and NPV falls when prevalence rises.",
        f"PPV is only {ppv * 100:.0f}% even with a good test because the disease is rare (many healthy people give false positives: {FP}).",
        f"False-negative rate = 1 - sensitivity = {FN}/{sick} = {FN / sick * 100:.0f}%.   False-positive rate = 1 - specificity = {FP}/{healthy} = {FP / healthy * 100:.1f}%.",
        f"Likelihood ratio + = sens/(1-spec) = {sens:.2f}/{1 - spec:.3f} = {sens / (1 - spec):.1f}.   LR - = (1-sens)/spec = {1 - sens:.2f}/{spec:.3f} = {(1 - sens) / spec:.2f}.",
        "SnNout: high Sensitivity, Negative result rules OUT.   SpPin: high Specificity, Positive result rules IN.",
        "Testing in series (both must be +) raises specificity.  Testing in parallel (either +) raises sensitivity.",
    ]
    yy = 1.65
    for m in notes:
        ax.text(0.3, yy, "- " + m, fontsize=8.6, va="center")
        yy -= 0.24
    save(fig, "02_diagnostic_2x2.png")


# ---------------------------------------------------------------- 03 case-control
def img03():
    a, b, c, d = 30, 15, 10, 25
    orr = a * d / (b * c)
    W, H = 9.6, 6.6
    fig, ax = new(W, H, "Case-control and matched-pair tables", "Case-control: pick people by DISEASE first, then look back at exposure.  Only the odds ratio is valid.")
    ax.text(2.6, H - 0.9, "Unmatched case-control (40 cases, 40 controls)", fontsize=10.5, fontweight="bold", ha="center")
    X, Y, cw, ch = 1.4, 3.3, 1.15, 0.75
    ax.text(X + 0.5 * cw, Y + 2 * ch + 0.2, "Cases", ha="center", fontsize=10.5, fontweight="bold")
    ax.text(X + 1.5 * cw, Y + 2 * ch + 0.2, "Controls", ha="center", fontsize=10.5, fontweight="bold")
    for r, (lab, vals, ls) in enumerate([("Exposed", [a, b], ["a", "b"]), ("Unexposed", [c, d], ["c", "d"])]):
        yy = Y + (1 - r) * ch
        ax.text(X - 0.1, yy + ch / 2, lab, ha="right", va="center", fontsize=10, fontweight="bold")
        for k in range(2):
            box(ax, X + k * cw, yy, cw, ch, f"{ls[k]} = {vals[k]}", fc=LORANGE if (r == k) else LBLUE, fs=12, bold=True)
    ax.text(2.6, 2.95, f"Odds ratio OR = (a x d) / (b x c)\n= ({a} x {d}) / ({b} x {c}) = {a * d} / {b * c} = {orr:.1f}", ha="center", va="top", fontsize=10.5, fontweight="bold", color=RED)
    ax.text(0.4, 2.35, f"Meaning: cases had {orr:.0f} times the odds of exposure\ncompared with controls.\nOdds of exposure in cases = a/c = {a}/{c} = {a / c:.0f}.\nOdds of exposure in controls = b/d = {b}/{d} = {b / d:.1f}.\nOR = {a / c:.0f} / {b / d:.1f} = {orr:.1f}.\nNEVER report an attack rate, incidence or RR from a\ncase-control study (researcher chose the case:control ratio).", fontsize=8.8, va="top", linespacing=1.4)

    # matched pairs
    pa, pb, pc, pd = 10, 20, 5, 15  # case exp & ctrl exp; case exp & ctrl not; case not & ctrl exp; neither
    ax.text(7.2, H - 0.9, "Matched pairs (50 case-control pairs)", fontsize=10.5, fontweight="bold", ha="center")
    X2, Y2 = 5.6, 3.3
    ax.text(X2 + cw, Y2 + 2 * ch + 0.45, "Control", ha="center", fontsize=10, fontweight="bold")
    ax.text(X2 + 0.5 * cw, Y2 + 2 * ch + 0.17, "exposed", ha="center", fontsize=9)
    ax.text(X2 + 1.5 * cw, Y2 + 2 * ch + 0.17, "unexposed", ha="center", fontsize=9)
    ax.text(X2 - 0.1, Y2 + 1.5 * ch + 0.0, "Case\nexposed", ha="right", va="center", fontsize=9.5, fontweight="bold")
    ax.text(X2 - 0.1, Y2 + 0.5 * ch, "Case\nunexposed", ha="right", va="center", fontsize=9.5, fontweight="bold")
    box(ax, X2, Y2 + ch, cw, ch, f"{pa} pairs\nboth exposed", fc=LGRAY, fs=8.5)
    box(ax, X2 + cw, Y2 + ch, cw, ch, f"b = {pb}", fc=LORANGE, fs=12, bold=True)
    box(ax, X2, Y2, cw, ch, f"c = {pc}", fc=LORANGE, fs=12, bold=True)
    box(ax, X2 + cw, Y2, cw, ch, f"{pd} pairs\nneither", fc=LGRAY, fs=8.5)
    ax.text(7.2, 2.95, f"Matched OR = b / c = {pb} / {pc} = {pb / pc:.1f}", ha="center", va="top", fontsize=10.5, fontweight="bold", color=RED)
    ax.text(5.2, 2.35, "Only DISCORDANT pairs (the two orange cells) count.\nb = case exposed but control not.\nc = control exposed but case not.\nGray cells are ignored.\nMcNemar chi-square = (b - c)^2 / (b + c)\n= (20 - 5)^2 / 25 = 9.0  (more than 3.84, significant).", fontsize=8.8, va="top", linespacing=1.4)
    ax.text(0.4, 0.55, "Why the study is chosen: rare disease or many exposures to test -> case-control (cheap, quick).  Common disease or many outcomes -> cohort.", fontsize=8.8, va="center", color=GRAY)
    save(fig, "03_case_control.png")


# ---------------------------------------------------------------- 04 which measure
def img04():
    W, H = 9.6, 6.3
    fig, ax = new(W, H, "Which measure do I calculate?", "Start with the study type, then read across.")
    rows = [
        ("Outbreak / cohort\n(follow exposed and unexposed)", "Attack rate, Risk ratio (RR),\nrisk difference, attributable fraction", LORANGE),
        ("Case-control\n(start with sick vs not sick)", "Odds ratio (OR) only\n(never RR, never incidence)", LBLUE),
        ("Cross-sectional survey\n(snapshot in time)", "Prevalence, prevalence ratio\n(or prevalence odds ratio)", LGREEN),
        ("Randomized trial / vaccine study", "RR, Vaccine efficacy = 1 - RR,\nARR, NNT = 1/ARR", LPURPLE),
        ("Follow people over time\n(person-time known)", "Incidence rate = new cases / person-time", LRED),
        ("Population comparison\n(different age structures)", "Age-adjusted rates (direct) or\nSMR = observed / expected (indirect)", LGRAY),
    ]
    y = H - 1.15
    for left, right, col in rows:
        box(ax, 0.4, y - 0.6, 4.1, 0.7, left, fc=col, fs=10, bold=True)
        ax.add_patch(FancyArrowPatch((4.55, y - 0.25), (5.05, y - 0.25), arrowstyle="-|>", mutation_scale=14, color="black", lw=1.5))
        box(ax, 5.1, y - 0.6, 4.1, 0.7, right, fc="white", fs=10)
        y -= 0.78
    save(fig, "04_which_measure.png")


# ---------------------------------------------------------------- 05 epi curves
def img05():
    W, H = 9.6, 7.5
    fig, ax = new(W, H, "Epidemic curve shapes", "x-axis = day of symptom onset, y-axis = number of new cases")
    ax.axis("off")
    specs = [
        ("Point source (one exposure)", [0, 1, 3, 8, 12, 9, 5, 2, 1, 0], "One sharp peak, ALL cases within one incubation period.\nExample: one church supper.", BLUE),
        ("Continuous common source", [0, 2, 6, 9, 10, 9, 10, 9, 10, 9, 8, 6, 3], "Rises, then a long flat plateau lasting longer than one\nincubation period.  Example: contaminated well in use.", ORANGE),
        ("Intermittent common source", [0, 5, 1, 0, 6, 0, 3, 0, 0, 7, 1, 0], "Irregular peaks, no pattern; exposure comes and goes.\nExample: a restaurant with a sometimes-contaminated dish.", GREEN),
        ("Propagated (person to person)", [1, 2, 1, 0, 0, 4, 6, 4, 0, 0, 10, 16, 12, 4], "Successive waves, each one incubation period apart and\nbigger than the last.  Example: measles.", RED),
    ]
    pos = [(0.55, 4.0), (5.2, 4.0), (0.55, 0.95), (5.2, 0.95)]
    for (title, vals, desc, col), (x, y) in zip(specs, pos):
        a = fig.add_axes([x / W, (y + 0.95) / H, 3.9 / W, 1.5 / H])
        a.bar(range(len(vals)), vals, width=0.9, color=col, edgecolor="black", lw=0.6)
        a.set_xticks([]); a.set_yticks([])
        for s in ["top", "right"]:
            a.spines[s].set_visible(False)
        a.set_title(title, fontsize=10.5, fontweight="bold", loc="left")
        ax.text(x, y + 0.7, desc, fontsize=8.4, va="top")
    ax.text(0.55, 0.62, "Exposure window (point source): first case onset - maximum incubation  to  last case onset - minimum incubation.\n"
                        "Example: first onset day 10, last onset day 20, incubation 2 to 6 days -> exposure between day 10-6 = day 4 and day 20-2 = day 18.\n"
                        "Mean/median incubation: peak day of curve minus median incubation = best guess of the exposure day.", fontsize=8.6, va="top")
    save(fig, "05_epi_curves.png")


# ---------------------------------------------------------------- 06 herd immunity
def img06():
    fig = plt.figure(figsize=(9.6, 5.8), dpi=250)
    fig.text(0.5, 0.955, "Herd immunity threshold (HIT) and R0", ha="center", fontsize=15, fontweight="bold")
    fig.text(0.5, 0.915, "HIT = 1 - 1/R0 : the share of the population that must be immune so each case infects fewer than 1 other person.", ha="center", fontsize=9.2, color=GRAY)
    a = fig.add_axes([0.08, 0.30, 0.5, 0.55])
    r = np.linspace(1, 18, 200)
    a.plot(r, (1 - 1 / r) * 100, color=BLUE, lw=2)
    pts = [("Flu (1.3)", 1.3), ("Original COVID (3)", 3), ("Smallpox (6)", 6), ("Measles (15)", 15)]
    for nm, v in pts:
        h = (1 - 1 / v) * 100
        a.plot(v, h, "o", color=RED)
        a.annotate(f"{nm}\nHIT {h:.0f}%", (v, h), textcoords="offset points", xytext=(6, -26 if v > 1.5 else 6), fontsize=8)
    a.set_xlabel("R0 (average people infected by one case in a fully susceptible population)", fontsize=8.5)
    a.set_ylabel("HIT (% immune needed)", fontsize=9)
    a.set_ylim(0, 100); a.set_xlim(1, 18); a.grid(alpha=0.3)
    fig.text(0.62, 0.82, "Worked examples", fontsize=11, fontweight="bold")
    ex = ["R0 = 2:  HIT = 1 - 1/2 = 50%", "R0 = 4:  HIT = 1 - 1/4 = 75%", "R0 = 5:  HIT = 1 - 1/5 = 80%", "R0 = 15: HIT = 1 - 1/15 = 93%",
          "", "Vaccine with efficacy VE:", "coverage needed = HIT / VE", "R0 = 5 (HIT 80%), VE = 0.90:", "coverage = 0.80 / 0.90 = 89%",
          "", "Effective reproduction number:", "Re = R0 x (fraction susceptible)", "R0 = 5, 60% immune: Re = 5 x 0.4 = 2", "Re < 1 -> outbreak shrinks."]
    for i, t in enumerate(ex):
        fig.text(0.62, 0.77 - i * 0.043, t, fontsize=9, fontweight="bold" if t.endswith(":") else "normal")
    fig.text(0.04, 0.19, "R0 = (contacts per day) x (probability of transmission per contact) x (days infectious).  Example: 10 x 0.05 x 6 = 3.\n"
                         "R0 > 1: outbreak grows.  R0 = 1: endemic (steady).  R0 < 1: dies out.  Measles is about 12-18, so ~95% coverage is needed.\n"
                         "HIT assumes random mixing and a perfect vaccine.  R0 describes a population with NO immunity; Re describes right now.", fontsize=8.8, va="top")
    fig.savefig(os.path.join(OUT, "06_herd_immunity.png"), dpi=250, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig); print("saved 06")


# ---------------------------------------------------------------- 07 SIR
def img07():
    N, beta, gamma = 1000, 0.5, 0.2
    S, I, R = 990.0, 10.0, 0.0
    S1 = S - beta * S * I / N
    new_inf = beta * S * I / N
    rec = gamma * I
    I1 = I + new_inf - rec
    R1 = R + rec
    Ss, Is, Rs = [S], [I], [R]
    for _ in range(100):
        ni = beta * S * I / N
        rc = gamma * I
        S, I, R = S - ni, I + ni - rc, R + rc
        Ss.append(S); Is.append(I); Rs.append(R)
    fig = plt.figure(figsize=(9.6, 5.9), dpi=250)
    fig.text(0.5, 0.955, "SIR model (Euler steps)", ha="center", fontsize=15, fontweight="bold")
    fig.text(0.5, 0.915, f"S = susceptible, I = infected, R = recovered.  N = {N}, beta = {beta} (transmission), gamma = {gamma} (recovery = 1/days infectious).", ha="center", fontsize=9.2, color=GRAY)
    a = fig.add_axes([0.07, 0.40, 0.45, 0.45])
    a.plot(Ss, color=BLUE, lw=2, label="S"); a.plot(Is, color=RED, lw=2, label="I"); a.plot(Rs, color=GREEN, lw=2, label="R")
    a.set_xlabel("day", fontsize=9); a.set_ylabel("people", fontsize=9); a.legend(fontsize=9); a.grid(alpha=0.3)
    pk = int(np.argmax(Is))
    a.annotate(f"peak I = {max(Is):.0f}\non day {pk}", (pk, max(Is)), textcoords="offset points", xytext=(25, -5), fontsize=8.5, arrowprops=dict(arrowstyle="-"))
    fig.text(0.57, 0.84, "The 3 update rules (each day, dt = 1)", fontsize=10.5, fontweight="bold")
    rules = [("new infections = beta x S x I / N", BLUE), ("new recoveries = gamma x I", GREEN),
             ("S(next) = S - new infections", BLUE), ("I(next) = I + new infections - new recoveries", RED), ("R(next) = R + new recoveries", GREEN)]
    for i, (t, c) in enumerate(rules):
        fig.text(0.57, 0.79 - i * 0.045, t, fontsize=9.3, color=c, fontweight="bold")
    fig.text(0.57, 0.545, "Day 0 -> day 1 worked example (S=990, I=10, R=0)", fontsize=10, fontweight="bold")
    wk = [f"new infections = 0.5 x 990 x 10 / 1000 = {new_inf:.2f}", f"new recoveries = 0.2 x 10 = {rec:.2f}",
          f"S1 = 990 - {new_inf:.2f} = {S1:.2f}", f"I1 = 10 + {new_inf:.2f} - {rec:.2f} = {I1:.2f}", f"R1 = 0 + {rec:.2f} = {R1:.2f}",
          f"Check: S + I + R = {S1 + I1 + R1:.0f} = N (people only move S -> I -> R)"]
    for i, t in enumerate(wk):
        fig.text(0.57, 0.50 - i * 0.043, t, fontsize=9)
    fig.text(0.04, 0.26, f"R0 = beta / gamma = {beta}/{gamma} = {beta / gamma:.1f}  (also R0 = beta x average days infectious = 0.5 x 5).\n"
                         "Infection peaks when S/N = 1/R0 (here S = 400), i.e. when Re = R0 x S/N falls to 1.\n"
                         "I rises while beta x S/N > gamma, and falls when beta x S/N < gamma.  Final R is below N: some never get infected.\n"
                         "Average days infectious = 1 / gamma = 5.  Doubling gamma halves the infectious period and halves R0.", fontsize=8.8, va="top")
    fig.savefig(os.path.join(OUT, "07_sir.png"), dpi=250, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig); print("saved 07")


# ---------------------------------------------------------------- 08 stats
def img08():
    from math import erf, sqrt
    fig = plt.figure(figsize=(9.6, 6.2), dpi=250)
    fig.text(0.5, 0.96, "Distributions, z-scores and box plots", ha="center", fontsize=15, fontweight="bold")
    mu, sd = 100, 15
    a = fig.add_axes([0.06, 0.60, 0.4, 0.30])
    x = np.linspace(55, 145, 400)
    y = np.exp(-0.5 * ((x - mu) / sd) ** 2)
    a.plot(x, y, "k", lw=1.5)
    for k, col in [(3, LGRAY), (2, LBLUE), (1, LORANGE)]:
        m = (x >= mu - k * sd) & (x <= mu + k * sd)
        a.fill_between(x[m], 0, y[m], color=col)
    a.plot(x, y, "k", lw=1.5)
    a.set_xticks([mu + k * sd for k in range(-3, 4)])
    a.set_xticklabels([f"{mu + k * sd}\n(z={k})" for k in range(-3, 4)], fontsize=7.5)
    a.set_yticks([])
    a.set_title(f"Normal curve: mean {mu}, SD {sd}", fontsize=10, fontweight="bold")
    a.text(mu, 0.45, "68%\n(85 to 115)", ha="center", fontsize=8.5, fontweight="bold")
    a.text(mu, 0.12, "95% (70 to 130)", ha="center", fontsize=8.5)
    fig.text(0.06, 0.52, "z = (value - mean) / SD.  Value 130: z = (130-100)/15 = 2.0\n(higher than about 97.5% of people).  99.7% lie within 3 SD.\n95% CI of a mean = mean +/- 1.96 x SE,  SE = SD / sqrt(n).\nExample: mean 100, SD 15, n = 36: SE = 15/6 = 2.5;\n95% CI = 100 +/- 1.96 x 2.5 = 100 +/- 4.9 = 95.1 to 104.9.", fontsize=8.3, va="top", linespacing=1.4)
    # skew
    a2 = fig.add_axes([0.55, 0.60, 0.40, 0.30])
    xs = np.linspace(0, 10, 300)
    right = xs ** 2 * np.exp(-xs / 0.9)
    right /= right.max()
    a2.plot(xs, right, color=BLUE, lw=2, label="right (positive) skew")
    left = right[::-1]
    a2.plot(xs, left * 0.8, color=RED, lw=2, label="left (negative) skew", ls="--")
    a2.set_yticks([]); a2.set_xticks([]); a2.legend(fontsize=8, loc="upper center")
    a2.set_title("Skew: tail points the direction of the name", fontsize=10, fontweight="bold")
    fig.text(0.55, 0.52, "Right skew (tail on the right, e.g. income):\n   mode < median < mean.\nLeft skew (tail on the left, e.g. age at death):\n   mean < median < mode.\nOutliers drag the MEAN toward the tail; the MEDIAN barely moves.\nSkewed data: report the median.  Symmetric data: report the mean.", fontsize=8.3, va="top", linespacing=1.4)
    # box plot
    data = [2, 4, 5, 7, 8, 9, 12, 30]
    med = np.median(data)
    q1, q3 = np.median(data[:4]), np.median(data[4:])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    a3 = fig.add_axes([0.06, 0.17, 0.42, 0.20])
    inside = [v for v in data if lo <= v <= hi]
    a3.bxp([dict(med=med, q1=q1, q3=q3, whislo=min(inside), whishi=max(inside), fliers=[v for v in data if v < lo or v > hi])], vert=False, widths=0.5, patch_artist=True, boxprops=dict(facecolor=LORANGE), medianprops=dict(color="black", lw=2))
    a3.set_yticks([]); a3.set_xlabel("value", fontsize=8.5)
    a3.set_title("Box plot of: " + ", ".join(map(str, data)), fontsize=9.5, fontweight="bold")
    fig.text(0.52, 0.34, "How to compute (n = 8 sorted values)", fontsize=10, fontweight="bold")
    tx = [f"Median = average of the middle two (7 and 8) = {med}",
          f"Q1 = median of lower half (2,4,5,7) = {q1}", f"Q3 = median of upper half (8,9,12,30) = {q3}",
          f"IQR = Q3 - Q1 = {q3} - {q1} = {iqr}",
          f"Fences: Q1 - 1.5 x IQR = {lo}   and   Q3 + 1.5 x IQR = {hi}",
          f"30 is above {hi}, so 30 is an OUTLIER (dot on the plot).",
          f"Range = max - min = 30 - 2 = 28.   Mean = {np.mean(data):.2f} (pulled up by 30)  vs median {med}.",
          f"Variance = sum of (x - mean)^2 / (n-1);  SD = square root of variance = {np.std(data, ddof=1):.2f}."]
    for i, t in enumerate(tx):
        fig.text(0.52, 0.30 - i * 0.034, t, fontsize=8.4)
    fig.text(0.06, 0.02, "Whiskers stop at the last value inside the fences.  Median line splits the data 50/50; the box holds the middle 50%.", fontsize=8.5, color=GRAY)
    fig.savefig(os.path.join(OUT, "08_stats.png"), dpi=250, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig); print("saved 08")


# ---------------------------------------------------------------- 09 incidence vs prevalence
def img09():
    pts = [("P1", -6, 12), ("P2", 3, 9), ("P3", 8, 24), ("P4", 14, 20), ("P5", 18, 33), ("P6", 22, 27), ("P7", 26, 31)]
    POP = 100
    pdate = 15
    p0, p1 = 10, 20
    point = [n for n, s, e in pts if s <= pdate <= e]
    period = [n for n, s, e in pts if s <= p1 and e >= p0]
    new = [n for n, s, e in pts if 0 <= s <= 30]
    preexisting = [n for n, s, e in pts if s < 0]
    atrisk = POP - len(preexisting)
    fig = plt.figure(figsize=(9.6, 6.3), dpi=250)
    fig.text(0.5, 0.96, "Incidence vs prevalence (Yale-style diagram)", ha="center", fontsize=15, fontweight="bold")
    fig.text(0.5, 0.925, "Each bar = one patient's illness from onset to recovery/death.  Population = 100 people.  Study month = day 0 to day 30.", ha="center", fontsize=9.2, color=GRAY)
    a = fig.add_axes([0.07, 0.46, 0.88, 0.41])
    a.axvspan(p0, p1, color=LBLUE, alpha=0.8, label=f"period: day {p0} to {p1}")
    a.axvline(pdate, color=RED, lw=2, label=f"point: day {pdate}")
    a.axvline(0, color="black", lw=1); a.axvline(30, color="black", lw=1)
    for i, (n, s, e) in enumerate(pts):
        y = len(pts) - i
        a.plot([max(s, -8), min(e, 36)], [y, y], color=ORANGE if s >= 0 else GRAY, lw=7, solid_capstyle="butt")
        a.plot([s if s >= -8 else -8], [y], "o", color="black", ms=5)
        a.text(-9.2, y, n, ha="right", va="center", fontsize=9, fontweight="bold")
        if s < 0:
            a.text(-7.5, y + 0.38, "onset before month (old case)", fontsize=7, color=GRAY)
    a.set_xlim(-8, 36); a.set_ylim(0.3, 7.8); a.set_yticks([])
    a.set_xlabel("day", fontsize=9); a.legend(fontsize=8.5, loc="upper right", ncol=2)
    fig.text(0.07, 0.355, "How to count (dot = onset; orange = new in month; gray = old case)", fontsize=10.5, fontweight="bold")
    tx = [
        (f"Point prevalence (day {pdate}) = cases ill ON that day / population = {len(point)} / {POP} = {len(point) / POP * 100:.0f}%     ({', '.join(point)} cross the red line)", RED),
        (f"Period prevalence (day {p0}-{p1}) = cases ill at ANY time in the period / population = {len(period)} / {POP} = {len(period) / POP * 100:.0f}%     ({', '.join(period)} touch the blue band)", BLUE),
        (f"Incidence (month) = NEW cases (onset inside the month) / people at risk = {len(new)} / ({POP} - {len(preexisting)} old case) = {len(new)} / {atrisk} = {len(new) / atrisk * 100:.1f}%", ORANGE),
        ("Incidence counts only NEW onsets and uses people who could still get sick as the denominator.  Prevalence counts ALL existing cases, old and new.", "black"),
        ("P = I x D : prevalence is roughly incidence rate x average duration.  Long illness (long bars) raises prevalence without raising incidence.", "black"),
        ("Prevalence goes UP when: new cases rise, cure rate falls, or deaths fall (people live longer with disease).  Prevalence DOWN: faster cure or death.", "black"),
        ("Incidence rate with person-time = new cases / total person-time.  Example: 6 new cases / 1,200 person-months = 5 per 1,000 person-months.", "black"),
    ]
    for i, (t, c) in enumerate(tx):
        fig.text(0.07, 0.315 - i * 0.043, t, fontsize=8.2, color=c)
    fig.savefig(os.path.join(OUT, "09_incidence_prevalence.png"), dpi=250, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig); print("saved 09", point, period, new)


# ---------------------------------------------------------------- 10 standardization
def img10():
    W, H = 9.6, 7.6
    fig, ax = new(W, H, "Age standardization and SMR", "Used to compare death rates of two populations that have different age mixes.")
    ages = ["0-24", "25-49", "50+"]
    cw = [1.4, 1.7, 1.7, 3.0]
    ax.text(0.4, 6.65, "DIRECT: apply the STUDY population's age-specific rates to a STANDARD population", fontsize=10.2, fontweight="bold", color=BLUE)
    rates = [2, 5, 20]
    std = [40000, 35000, 25000]
    hdr = ["Age group", "Study rate\n(per 1,000)", "Standard\npopulation", "Expected deaths\n= rate/1,000 x std pop"]
    x = 0.8
    for h, w in zip(hdr, cw):
        box(ax, x, 5.6, w, 0.55, h, fc=LBLUE, fs=8.8, bold=True)
        x += w
    exps = [r / 1000 * sv for r, sv in zip(rates, std)]
    for i in range(3):
        x = 0.8
        yy = 5.2 - i * 0.4
        for t, w in zip([ages[i], str(rates[i]), f"{std[i]:,}", f"{rates[i]}/1,000 x {std[i]:,} = {exps[i]:.0f}"], cw):
            box(ax, x, yy, w, 0.4, t, fs=9)
            x += w
    x = 0.8
    for t, w in zip(["Total", "", f"{sum(std):,}", f"{sum(exps):.0f}"], cw):
        box(ax, x, 4.0, w, 0.4, t, fc=LGRAY, fs=9, bold=True)
        x += w
    adj = sum(exps) / sum(std) * 1000
    ax.text(0.8, 3.85, f"Age-adjusted rate = total expected / total standard population = {sum(exps):.0f} / {sum(std):,} = {adj:.2f} per 1,000.", fontsize=9.2, fontweight="bold", va="top")
    ax.text(0.8, 3.55, "Compare adjusted rates only when both used the SAME standard population.", fontsize=8.6, va="top")
    ax.text(0.4, 3.0, "INDIRECT (SMR): apply STANDARD (reference) rates to the STUDY population's size", fontsize=10.2, fontweight="bold", color=RED)
    pop = [10000, 20000, 5000]
    srate = [2, 5, 20]
    hdr2 = ["Age group", "Standard rate\n(per 1,000)", "Study\npopulation", "Expected deaths\n= std rate/1,000 x study pop"]
    x = 0.8
    for h, w in zip(hdr2, cw):
        box(ax, x, 2.2, w, 0.55, h, fc=LRED, fs=8.8, bold=True)
        x += w
    ex2 = [r / 1000 * p for r, p in zip(srate, pop)]
    for i in range(3):
        x = 0.8
        yy = 1.8 - i * 0.4
        for t, w in zip([ages[i], str(srate[i]), f"{pop[i]:,}", f"{srate[i]}/1,000 x {pop[i]:,} = {ex2[i]:.0f}"], cw):
            box(ax, x, yy, w, 0.4, t, fs=9)
            x += w
    obs = 264
    ax.text(0.8, 0.8, f"Total expected = {sum(ex2):.0f}.  Observed deaths = {obs}.  SMR = observed / expected = {obs} / {sum(ex2):.0f} = {obs / sum(ex2):.2f}", fontsize=9.2, fontweight="bold", va="top")
    ax.text(0.8, 0.5, "SMR 1.0 = same as reference.  1.20 = 20% more deaths than expected.  0.80 = 20% fewer.\nUse when the study population's age-specific rates are unstable (small numbers).", fontsize=8.4, va="top", linespacing=1.4)
    save(fig, "10_standardization.png")


# ---------------------------------------------------------------- 11 chain + triad
def img11():
    W, H = 9.6, 6.2
    fig, ax = new(W, H, "Chain of infection and the epidemiologic triad")
    cx, cy, R = 2.6, 3.0, 1.75
    names = [("1. Infectious agent", "bacteria, virus, parasite, fungus", "kill/neutralize: disinfect, antibiotics"),
             ("2. Reservoir", "humans, animals, soil, water", "remove source: treat carriers, clean water"),
             ("3. Portal of exit", "cough, stool, blood, bite", "cover coughs, safe sharps disposal"),
             ("4. Mode of transmission", "direct / indirect / vector", "handwashing, masks, bed nets, cook food"),
             ("5. Portal of entry", "mouth, skin, lungs, mucosa", "gloves, masks, protect skin"),
             ("6. Susceptible host", "unvaccinated, young, old, ill", "vaccinate, nutrition, treat illness")]
    cols = [LRED, LORANGE, LGREEN, LBLUE, LPURPLE, LGRAY]
    ang = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, 7)[:-1]
    for i, (th, (n, ex, br)) in enumerate(zip(ang, names)):
        x, y = cx + R * np.cos(th), cy + R * np.sin(th) * 1.0
        ax.add_patch(Circle((x, y), 0.55, fc=cols[i], ec="black", lw=1.2))
        ax.text(x, y, n.split(". ")[0], ha="center", va="center", fontsize=14, fontweight="bold")
        th2 = ang[(i + 1) % 6]
        x2, y2 = cx + R * np.cos(th2), cy + R * np.sin(th2)
        v = np.array([x2 - x, y2 - y]); v /= np.linalg.norm(v)
        ax.add_patch(FancyArrowPatch((x + v[0] * 0.6, y + v[1] * 0.6), (x2 - v[0] * 0.6, y2 - v[1] * 0.6), arrowstyle="-|>", mutation_scale=14, lw=1.6, color="black"))
    ax.text(cx, cy, "Break ANY\nlink and the\nchain stops", ha="center", va="center", fontsize=10, fontweight="bold", color=RED)
    y = H - 0.9
    for i, (n, ex, br) in enumerate(names):
        ax.text(5.15, y, n, fontsize=9.6, fontweight="bold")
        ax.text(5.15, y - 0.2, "e.g. " + ex, fontsize=8.4)
        ax.text(5.15, y - 0.38, "break it: " + br, fontsize=8.4, color=GREEN)
        y -= 0.58
    # triad
    ax.text(5.15, 1.7, "Epidemiologic triad = AGENT + HOST + ENVIRONMENT\n(all three must meet for disease).", fontsize=9.4, fontweight="bold", va="top", linespacing=1.3)
    ax.text(5.15, 1.25, "Agent: the germ or chemical.  Host: age, immunity, behavior, genes.\nEnvironment: weather, crowding, sanitation.\nVector (mosquito/tick) is sometimes added as a 4th corner.", fontsize=8.4, va="top", linespacing=1.4)
    ax.text(0.4, 0.55, "Person-Place-Time = the three parts of DESCRIPTIVE epidemiology (who, where, when).  Triad = the CAUSES.  Chain = HOW it spreads.\n"
                       "Transmission: DIRECT = touching, kissing, sex, droplets under about 1 meter, mother to baby.  INDIRECT = airborne (particles under 5 micrometers, travel far),\n"
                       "vehicle (food, water, blood), fomite (doorknob), vector (mechanical = on the body; biological = the germ grows in the vector).", fontsize=8.3, va="top")
    save(fig, "11_chain_and_triad.png")


# ---------------------------------------------------------------- 12 natural history
def img12():
    W, H = 9.6, 4.8
    fig, ax = new(W, H, "Natural history of disease and the four levels of prevention", "Read left to right: what happens to ONE person over time.")
    stages = [("Susceptibility\n(risk factors,\nno disease yet)", 0.4, 2.1, LGREEN), ("Subclinical\n(disease inside,\nno symptoms)", 2.5, 2.1, LORANGE),
              ("Clinical\n(symptoms)", 4.6, 2.1, LRED), ("Recovery,\ndisability or death", 6.7, 2.4, LGRAY)]
    for t, x, w, c in stages:
        box(ax, x, 2.7, w, 0.9, t, fc=c, fs=9.3, bold=True)
    ax.add_patch(FancyArrowPatch((0.4, 2.55), (9.1, 2.55), arrowstyle="-|>", mutation_scale=14, lw=1.5, color="black"))
    ax.text(2.5, 2.35, "exposure", fontsize=8.5, ha="center", color=GRAY)
    ax.text(4.6, 2.35, "symptom onset", fontsize=8.5, ha="center", color=GRAY)
    ax.annotate("", xy=(4.6, 2.2), xytext=(2.5, 2.2), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.4))
    ax.text(3.55, 1.95, "incubation period (infection)\nlatent period (chronic disease)", fontsize=8.2, ha="center", va="top", color=BLUE)
    prev = [("Primordial", "stop risk factors from ever\nappearing (laws, clean air,\nhealthy food policy)", 0.4, 2.0, LGREEN),
            ("Primary", "prevent disease before it\nstarts: vaccines, seat belts,\nhandwashing", 2.5, 2.0, LBLUE),
            ("Secondary", "catch it early: screening\n(mammogram, blood\npressure check)", 4.6, 2.0, LORANGE),
            ("Tertiary", "limit damage after disease:\nrehab, treatment to prevent\ncomplications", 6.7, 2.4, LPURPLE)]
    for t, d, x, w, c in prev:
        box(ax, x, 0.15, w, 0.5, t, fc=c, fs=10.5, bold=True)
        ax.text(x + w / 2, 0.8, d, ha="center", va="bottom", fontsize=8)
    ax.text(9.15, 0.4, "", fontsize=8)
    ax.text(0.4, 1.3, "Primordial -> Primary -> Secondary -> Tertiary (match each to the stage above it).", fontsize=8.8, fontweight="bold", color=GRAY)
    save(fig, "12_natural_history_prevention.png")


# ---------------------------------------------------------------- 13 study designs
def img13():
    W, H = 10.6, 7.2
    fig, ax = new(W, H, "Study designs at a glance", "Arrow shows the direction you follow people.  The measure you can compute depends on the design.")
    designs = [
        ("COHORT", "Start: exposed vs unexposed (healthy people)\nFollow FORWARD -> who gets disease?", "RR, incidence, attack rate", "good for rare exposures, many outcomes;\nslow and costly; loss to follow-up bias", LORANGE),
        ("CASE-CONTROL", "Start: people WITH disease vs people without\nLook BACKWARD -> who was exposed?", "OR only", "good for rare disease, many exposures;\nquick and cheap; recall bias,\nselection of controls", LBLUE),
        ("CROSS-SECTIONAL", "Start: one group, measured at ONE time\nExposure and disease at the same moment", "prevalence (not incidence)", "quick snapshot; cannot show which\ncame first (no temporality)", LGREEN),
        ("RANDOMIZED TRIAL (RCT)", "Start: volunteers randomly assigned to\ntreatment or placebo.  Follow FORWARD.", "RR, VE = 1-RR, ARR, NNT", "strongest evidence for cause and effect;\nrandom assignment balances confounders;\nblinding removes bias", LPURPLE),
        ("ECOLOGICAL", "Start: groups (countries, towns), not individuals\nCompare group-level rates and exposures", "correlation", "cheap; risk of ecological fallacy\n(group pattern need not be true\nfor each person)", LGRAY),
    ]
    y = H - 1.0
    for nm, how, meas, pro, col in designs:
        box(ax, 0.3, y - 0.95, 1.9, 1.05, nm.replace(" (RCT)", "\n(RCT)").replace("RANDOMIZED ", "RANDOMIZED\n"), fc=col, fs=9.8, bold=True)
        box(ax, 2.2, y - 0.95, 3.4, 1.05, how, fs=8.6)
        box(ax, 5.6, y - 0.95, 2.0, 1.05, "gives:\n" + meas.replace(", ", ",\n", 1) if len(meas) > 20 else "gives:\n" + meas, fs=8.6, fc=LGRAY)
        box(ax, 7.6, y - 0.95, 2.7, 1.05, pro, fs=8.0)
        y -= 1.12
    ax.text(0.3, 0.3, "Strength of evidence (weakest to strongest): case report < case series < cross-sectional / ecological < case-control < cohort < RCT < systematic review / meta-analysis.", fontsize=8.5, va="center")
    save(fig, "13_study_designs.png")


for f in [img01, img02, img03, img04, img05, img06, img07, img08, img09, img10, img11, img12, img13]:
    f()
