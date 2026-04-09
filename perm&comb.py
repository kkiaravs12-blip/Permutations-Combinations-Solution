import math
import itertools
import string
import random
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

# ------------------ Pigeonhole Principle ------------------
def pigeonhole_principle(pigeons, holes):
    if holes <= 0:
        return "Error: Number of holes must be greater than 0."
    min_required = math.ceil(pigeons / holes)
    return f"By the Pigeonhole Principle, at least one hole must contain at least {min_required} pigeon(s)."

def pigeonhole_distribution(pigeons, holes):
    min_per_hole = pigeons // holes
    remainder = pigeons % holes
    distribution = [min_per_hole + 1 if i < remainder else min_per_hole for i in range(holes)]
    return distribution

def show_distribution_bar(distribution):
    labels = [f"Hole {i+1}" for i in range(len(distribution))]
    plt.bar(labels, distribution)
    plt.title("Pigeon Distribution Across Holes")
    plt.xlabel("Holes")
    plt.ylabel("Number of Pigeons")
    plt.tight_layout()
    plt.show()

# ------------------ Distinct Permutations & Combinations ------------------
def permutations_distinct(n, r):
    if r > n:
        return 0
    return math.factorial(n) // math.factorial(n - r)

def combinations_distinct(n, r):
    if r > n:
        return 0
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

def show_permutation_bars(n, r):
    terms = list(range(n, n - r, -1))
    plt.bar(range(1, r + 1), terms)
    plt.title(f"Permutation Terms for P({n},{r})")
    plt.xlabel("Term Number")
    plt.ylabel("Value")
    plt.show()

def show_pascal_triangle(rows):
    triangle = []
    for _ in range(rows):
        row = [1]
        if triangle:
            last = triangle[-1]
            row.extend([sum(pair) for pair in zip(last, last[1:])])
            row.append(1)
        triangle.append(row)

    plt.figure(figsize=(10, rows/2))
    plt.axis('off')
    for i, row in enumerate(triangle):
        for j, val in enumerate(row):
            x = j - len(row) / 2
            y = -i
            plt.text(x, y, str(val), fontsize=12, ha='center')
    plt.title(f"Pascal's Triangle ({rows} rows)")
    plt.ylim(-rows - 1, 1)
    plt.xlim(-rows / 2 - 1, rows / 2 + 1)
    plt.show()

# ------------------ Tree Diagrams ------------------
def buildPaths(options, r, permutations=True, repetition=False):
    if permutations:
        if repetition:
            return list(itertools.product(options, repeat=r))
        else:
            return list(itertools.permutations(options, r))
    else:
        if repetition:
            return list(itertools.combinations_with_replacement(options, r))
        else:
            return list(itertools.combinations(options, r))

def plotTree(ax, paths, title):
    ax.set_title(title, fontsize=11, fontweight="bold")
    levelNodes = {}
    for path in paths:
        for level in range(len(path) + 1):
            prefix = path[:level]
            levelNodes.setdefault(level, set()).add(prefix)

    pos = {}
    yGap = -1.5
    for level, nodes in levelNodes.items():
        for i, node in enumerate(sorted(nodes)):
            pos[node] = (i, level * yGap)

    for path in paths:
        for level in range(len(path)):
            parent = path[:level]
            child = path[:level+1]
            ax.plot([pos[parent][0], pos[child][0]],
                    [pos[parent][1], pos[child][1]], 'k-', lw=1)

    for node, (x, y) in pos.items():
        label = ''.join(node) if node else "Start"
        ax.scatter(x, y, s=500, edgecolors="black", zorder=3)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight="bold")

    ax.axis('off')

# ------------------ Binomial Expansion ------------------
def binomial_coefficient(n, k):
    return math.comb(n, k)

def binomial_expansion(a, b, n):
    terms = []
    for k in range(n + 1):
        coeff = binomial_coefficient(n, k)
        term = f"{coeff}*{a}^{n-k}*{b}^{k}"
        terms.append(term)
    return " + ".join(terms)

def plot_binomial_expansion(a, b, n):
    coeffs = [binomial_coefficient(n, k) for k in range(n + 1)]
    plt.bar(range(n + 1), coeffs)
    plt.title(f"Binomial Expansion Coefficients for (a + b)^{n}")
    plt.xlabel("Term index k")
    plt.ylabel("Coefficient")
    plt.xticks(range(n + 1))
    plt.show()

# ------------------ Multinomial Expansion ------------------
def multinomial_coefficient(n, ks):
    coeff = math.factorial(n)
    for k in ks:
        coeff //= math.factorial(k)
    return coeff

def multinomial_expansion(variables, powers):
    n = sum(powers)
    coeff = multinomial_coefficient(n, powers)
    parts = [f"{var}^{p}" if p > 0 else "" for var, p in zip(variables, powers)]
    term_str = "*".join([p for p in parts if p])
    return f"{coeff} * {term_str}"

def plot_multinomial_expansion(variables, powers):
    coeff = multinomial_coefficient(sum(powers), powers)
    plt.bar([0], [coeff])
    plt.title(f"Multinomial Coefficient for powers {powers}")
    plt.xlabel("Term")
    plt.ylabel("Coefficient")
    plt.xticks([0], [f"{variables}^{powers}"])
    plt.show()

# ------------------ (NEW) Combinations with Repetition ------------------
def combinations_with_repetition(n, r):
    return math.comb(n + r - 1, r)

def _draw_bins(ax, counts, r, labels):
    n = len(counts)
    ax.set_xlim(0, n)
    ax.set_ylim(0, max(r, 1) + 1)
    for i, c in enumerate(counts):
        # draw bin
        ax.add_patch(Rectangle((i + 0.1, 0.6), 0.8, max(r, 1), fill=False, linewidth=1.5))
        # draw balls as small circles stacked
        if c > 0:
            spacing = max(0.9 / max(c, 1), 0.18)  # keep balls separated
            start_y = 0.8
            for k in range(c):
                y = start_y + k * spacing
                ax.add_patch(Circle((i + 0.5, y), 0.08))
        # label
        ax.text(i + 0.5, 0.35, labels[i], ha='center', va='center', fontsize=9)
        ax.text(i + 0.5, max(r, 1) + 0.8, str(c), ha='center', va='center', fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(" | ".join(map(str, counts)), fontsize=10)

def show_combination_bins(n, r, show_all=True, max_examples=20):
    from itertools import combinations_with_replacement
    labels = [f"Type {i+1}" for i in range(n)]

    # Build all distributions (as count vectors)
    combos = list(combinations_with_replacement(range(n), r))
    counts_list = []
    for combo in combos:
        counts = [0] * n
        for idx in combo:
            counts[idx] += 1
        counts_list.append(tuple(counts))

    # Decide how many to show
    if not show_all or len(counts_list) > max_examples:
        # sample a subset (deterministic: pick first k)
        counts_list = counts_list[:max_examples]
        title_extra = f" (showing {len(counts_list)} of many)"
    else:
        title_extra = ""

    cols = min(4, len(counts_list))
    rows = math.ceil(len(counts_list) / cols) if counts_list else 1
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3.2, rows * 3.2))
    if isinstance(axes, plt.Axes):
        axes = [axes]
    else:
        axes = axes.flatten()

    for ax, counts in zip(axes, counts_list):
        _draw_bins(ax, counts, r, labels)

    # hide any unused axes
    for ax in axes[len(counts_list):]:
        ax.axis('off')

    plt.suptitle(f"Combinations with Repetition (n={n}, r={r}){title_extra}", fontsize=12)
    plt.tight_layout()
    plt.show()

# ------------------ (NEW) Indistinct Permutations ------------------
def permutations_indistinct(word):
    counts = Counter(word)
    n = sum(counts.values())
    denom = 1
    for c in counts.values():
        denom *= math.factorial(c)
    return math.factorial(n) // denom

def show_indistinct_visuals(word):
    counts = Counter(word)

    # 1) Frequency bar chart
    plt.bar(counts.keys(), counts.values())
    plt.title(f"Letter Frequencies in '{word}'")
    plt.xlabel("Letters")
    plt.ylabel("Frequency")
    plt.show()

    # 2) Factorial breakdown (log10 for big numbers)
    n = sum(counts.values())
    num = math.factorial(n)
    den_parts = [math.factorial(c) for c in counts.values()]

    values = [num] + den_parts
    labels = ["n!"] + [f"{ch}! (×{counts[ch]})" for ch in counts.keys()]

    use_log = any(v > 1e9 for v in values)
    to_plot = [math.log10(v) if use_log else v for v in values]

    plt.bar(range(len(labels)), to_plot)
    plt.xticks(range(len(labels)), labels, rotation=20, ha='right')
    plt.ylabel("log10(value)" if use_log else "value")
    plt.title("Factorial Breakdown for n! / (k1! k2! ...)")
    plt.tight_layout()
    plt.show()

    # 3) Sample distinct arrangements (only for small n to avoid slowdown)
    if n <= 8:
        # safe: generate unique permutations and show first 10
        unique = set(itertools.permutations(word))
        examples = ["".join(p) for p in list(unique)[:10]]
        print("\nSample distinct arrangements (up to 10):")
        for s in examples:
            print(s)
    else:
        print("\nToo many letters to list sample arrangements safely (n > 8).")

# ------------------ Main Menu ------------------
def main():
    while True:
        print("\nPermutations and Combinations Calculator with Visual Aids")
        print("1) Distinct permutations P(n,r)")
        print("2) Distinct combinations C(n,r) + Pascal's Triangle")
        print("3) Binomial Expansion")
        print("4) Multinomial Expansion")
        print("5) Tree diagrams for counting problems")
        print("6) Pigeonhole Principle demonstration")
        print("7) Combinations with Repetition (Bins Visual)")
        print("8) Indistinct permutations (e.g. BANANA)")
        print("0) Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            n = int(input("Enter n (total items): "))
            r = int(input("Enter r (items to choose): "))
            val = permutations_distinct(n, r)
            print(f"P({n},{r}) = {val}")
            show_permutation_bars(n, r)

        elif choice == "2":
            n = int(input("Enter n (rows for Pascal's Triangle): "))
            r = int(input("Enter r (choose r for combinations): "))
            val = combinations_distinct(n, r)
            print(f"C({n},{r}) = {val}")
            show_pascal_triangle(n)

        elif choice == "3":
            a = input("Enter variable a: ").strip()
            b = input("Enter variable b: ").strip()
            n = int(input("Enter power n: "))
            expansion = binomial_expansion(a, b, n)
            print(f"Binomial expansion of ({a} + {b})^{n}:")
            print(expansion)
            plot_binomial_expansion(a, b, n)

        elif choice == "4":
            variables = input("Enter variables separated by space (e.g. x y z): ").split()
            powers = list(map(int, input("Enter powers for each variable separated by space: ").split()))
            expansion = multinomial_expansion(variables, powers)
            print("Multinomial expansion term:")
            print(expansion)
            plot_multinomial_expansion(variables, powers)

        elif choice == "5":
            n = int(input("Enter total number of items (n): "))
            r = int(input("Enter number to choose (r): "))
            repetition = input("Allow repetition? (yes/no): ").strip().lower() == "yes"
            items = list(string.ascii_uppercase[:n])
            permPaths = buildPaths(items, r, permutations=True, repetition=repetition)
            combPaths = buildPaths(items, r, permutations=False, repetition=repetition)
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            plotTree(axes[0], permPaths, f"Permutations Tree ({'With' if repetition else 'No'} Repetition)")
            plotTree(axes[1], combPaths, f"Combinations Tree ({'With' if repetition else 'No'} Repetition)")
            plt.tight_layout()
            plt.show()

        elif choice == "6":
            pigeons = int(input("Enter number of pigeons (items): "))
            holes = int(input("Enter number of holes (containers): "))
            result = pigeonhole_principle(pigeons, holes)
            print("\n" + result)
            distribution = pigeonhole_distribution(pigeons, holes)
            print("\nDistribution of pigeons across holes:")
            for i, count in enumerate(distribution, start=1):
                print(f"Hole {i}: {'🐦' * count} ({count})")
            show_distribution_bar(distribution)

        elif choice == "7":
            n = int(input("Enter number of types (n): "))
            r = int(input("Enter number to choose (r): "))
            val = combinations_with_repetition(n, r)
            print(f"Number of combinations with repetition C({n}+{r}-1,{r}) = {val}")
            # show all if small; else sample a grid so it never becomes a super-wide figure
            show_combination_bins(n, r, show_all=True, max_examples=20)

        elif choice == "8":
            word = input("Enter a word (e.g. BANANA): ").strip().upper()
            val = permutations_indistinct(word)
            print(f"Number of distinct permutations of '{word}' = {val}")
            show_indistinct_visuals(word)

        elif choice == "0":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
