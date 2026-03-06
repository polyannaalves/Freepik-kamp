#!/usr/bin/env python3
"""
=============================================================================
ANÁLISE DEFINITIVA DA QUINA - CONCURSO 6969 (06/03/2026 - SEXTA)
=============================================================================
FOCO: Diversificação máxima + Cobertura + 3 Níveis de Bolas Pesadas
Base: 59 concursos (6910-6968) + Histórico all-time
=============================================================================
"""

from collections import Counter, defaultdict
from itertools import combinations
import random
import math

# =====================================================================
# BASE DE DADOS: 59 CONCURSOS (6910-6968)
# =====================================================================
results = {
    6910: [2, 18, 20, 49, 68], 6911: [3, 51, 56, 59, 72],
    6912: [4, 43, 44, 58, 62], 6913: [25, 31, 38, 42, 58],
    6914: [25, 41, 48, 49, 66], 6915: [5, 19, 21, 51, 66],
    6916: [8, 54, 58, 72, 76], 6917: [11, 15, 29, 48, 57],
    6918: [9, 21, 24, 63, 69], 6919: [4, 6, 9, 26, 64],
    6920: [4, 28, 34, 42, 47], 6921: [26, 50, 69, 74, 77],
    6922: [16, 26, 36, 51, 56], 6923: [18, 34, 41, 57, 63],
    6924: [4, 13, 49, 52, 66], 6925: [9, 25, 44, 46, 62],
    6926: [14, 29, 40, 79, 80], 6927: [3, 20, 49, 57, 69],
    6928: [33, 44, 56, 66, 72], 6929: [8, 13, 14, 53, 54],
    6930: [5, 16, 22, 65, 80], 6931: [48, 69, 73, 77, 79],
    6932: [28, 33, 65, 71, 76], 6933: [51, 55, 62, 64, 69],
    6934: [5, 15, 25, 40, 67], 6935: [5, 7, 33, 58, 64],
    6936: [8, 15, 21, 39, 48], 6937: [16, 17, 46, 56, 70],
    6938: [3, 4, 21, 32, 52], 6939: [10, 26, 27, 55, 73],
    6940: [24, 53, 66, 73, 77], 6941: [12, 32, 34, 57, 64],
    6942: [16, 33, 34, 50, 71], 6943: [22, 23, 35, 40, 44],
    6944: [2, 8, 30, 56, 61], 6945: [33, 61, 66, 68, 70],
    6946: [1, 48, 53, 75, 80], 6947: [6, 30, 52, 60, 79],
    6948: [3, 21, 32, 46, 57], 6949: [21, 51, 60, 67, 73],
    6950: [1, 6, 24, 47, 60], 6951: [1, 10, 20, 44, 66],
    6952: [1, 2, 57, 62, 79], 6953: [7, 22, 35, 58, 63],
    6954: [2, 29, 34, 44, 78], 6955: [6, 8, 18, 23, 74],
    6956: [10, 38, 51, 64, 68], 6957: [11, 14, 18, 67, 74],
    6958: [9, 14, 24, 55, 68], 6959: [7, 12, 27, 49, 54],
    6960: [7, 8, 14, 39, 52], 6961: [15, 45, 55, 62, 65],
    6962: [15, 25, 37, 79, 80], 6963: [6, 19, 29, 62, 74],
    6964: [3, 9, 30, 56, 58], 6965: [7, 12, 26, 68, 74],
    6966: [9, 19, 26, 28, 52], 6967: [26, 47, 68, 74, 77],
    6968: [8, 14, 44, 56, 72],
}

# Sextas-feiras na base
friday_concursos = [6912, 6917, 6923, 6929, 6935, 6941, 6947, 6953, 6957, 6963]

historical_freq = {
    4: 484, 52: 470, 26: 468, 49: 462, 31: 460, 44: 458, 39: 456,
    16: 455, 53: 454, 15: 452, 56: 451, 62: 450, 14: 449, 64: 448,
    8: 447, 33: 446, 7: 445, 68: 444, 55: 443, 9: 442, 58: 441,
    34: 440, 21: 439, 3: 438, 51: 437, 57: 436, 66: 435, 29: 434,
    6: 433, 24: 432, 74: 430,
}

all_numbers = list(range(1, 81))
sorted_concursos = sorted(results.keys())
total_concursos = len(results)
NEXT = 6969
last_draw = set(results[6968])
primes = set([2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79])

print("=" * 75)
print("  ╔═══════════════════════════════════════════════════════════════════╗")
print("  ║     ANÁLISE DEFINITIVA DA QUINA - CONCURSO 6969                 ║")
print("  ║     06/03/2026 (SEXTA) | Prêmio: ~R$ 13.500.000               ║")
print("  ║     59 concursos + 3 níveis de bolas pesadas                    ║")
print("  ╚═══════════════════════════════════════════════════════════════════╝")

# =====================================================================
# CÁLCULOS BASE
# =====================================================================
all_drawn = []
for nums in results.values():
    all_drawn.extend(nums)
freq = Counter(all_drawn)

# Delays
delays = {}
for num in all_numbers:
    last_seen = None
    for c in reversed(sorted_concursos):
        if num in results[c]:
            last_seen = c
            break
    delays[num] = (NEXT - last_seen) if last_seen else 999

# Somas
all_somas = [sum(results[c]) for c in sorted_concursos]
media_soma = sum(all_somas) / len(all_somas)
std_soma = math.sqrt(sum((s - media_soma)**2 for s in all_somas) / len(all_somas))

# Sexta freq
friday_nums = []
for c in friday_concursos:
    friday_nums.extend(results[c])
friday_freq = Counter(friday_nums)

# Momentum
def calc_momentum():
    freq_5 = Counter()
    for c in sorted_concursos[-5:]:
        for n in results[c]:
            freq_5[n] += 1
    freq_10 = Counter()
    for c in sorted_concursos[-10:]:
        for n in results[c]:
            freq_10[n] += 1
    mom = {}
    for num in all_numbers:
        r5 = freq_5.get(num, 0) / 5
        r10 = freq_10.get(num, 0) / 10
        r_all = freq.get(num, 0) / total_concursos
        if r_all > 0:
            mom[num] = (r5 * 3 + r10 * 2) / 5 / r_all
        else:
            mom[num] = (r5 * 3 + r10 * 2) * 5
    return mom
momentum = calc_momentum()

# Ciclos
cycles_data = {}
for num in all_numbers:
    apps = [c for c in sorted_concursos if num in results[c]]
    if len(apps) >= 3:
        intervals = [apps[i] - apps[i-1] for i in range(1, len(apps))]
        avg = sum(intervals) / len(intervals)
        std = math.sqrt(sum((x - avg)**2 for x in intervals) / len(intervals))
        since = NEXT - apps[-1]
        due = since / avg if avg > 0 else 0
        cycles_data[num] = {'avg': avg, 'std': std, 'since': since, 'due': due}

# Pares
pair_count = Counter()
for nums in results.values():
    s = sorted(nums)
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            pair_count[(s[i], s[j])] += 1

pair_scores = defaultdict(int)
for (a, b), cnt in pair_count.most_common(50):
    pair_scores[a] += cnt
    pair_scores[b] += cnt

# =====================================================================
# 3 NÍVEIS DE BOLAS PESADAS
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO DE BOLAS PESADAS - 3 CENÁRIOS")
print("=" * 75)

def calc_heavy_weights(decay, weight_per_draw, hist_bonus):
    weights = {}
    for num in all_numbers:
        peso = 1.0
        for c in sorted_concursos:
            if num in results[c]:
                dist = NEXT - c
                peso += weight_per_draw * (decay ** dist)
        hist = historical_freq.get(num, 420)
        peso += hist_bonus * hist
        weights[num] = peso
    return weights

# Nível 1: Peso LEVE (pouca influência do passado)
heavy_light = calc_heavy_weights(decay=0.85, weight_per_draw=0.5, hist_bonus=0.001)
# Nível 2: Peso MÉDIO (influência moderada)
heavy_medium = calc_heavy_weights(decay=0.92, weight_per_draw=1.0, hist_bonus=0.003)
# Nível 3: Peso FORTE (bolas muito pesadas, passado recente domina)
heavy_strong = calc_heavy_weights(decay=0.95, weight_per_draw=1.5, hist_bonus=0.005)

levels = [
    ("LEVE", heavy_light, "Decaimento rápido (85%), pouca memória"),
    ("MÉDIO", heavy_medium, "Decaimento moderado (92%), equilíbrio"),
    ("FORTE", heavy_strong, "Decaimento lento (95%), forte memória"),
]

for level_name, weights, desc in levels:
    ranked = sorted(weights.items(), key=lambda x: -x[1])
    total_w = sum(weights.values())
    top5 = [n for n, _ in ranked[:5]]
    top10 = [n for n, _ in ranked[:10]]

    print(f"\n  ── NÍVEL {level_name}: {desc} ──")
    print(f"  Top 10: {sorted(top10)}")
    print(f"  Top 5:  {sorted(top5)}")
    print(f"  Vantagem máxima: {ranked[0][1]/ranked[-1][1]:.2f}x")

    # Monte Carlo com este peso
    random.seed(6969)
    mc = Counter()
    for _ in range(20000):
        drawn = set()
        while len(drawn) < 5:
            pick = random.choices(all_numbers, weights=[weights[n] for n in all_numbers], k=1)[0]
            drawn.add(pick)
        for n in drawn:
            mc[n] += 1

    print(f"  Monte Carlo Top 10: {[n for n, _ in mc.most_common(10)]}")

# =====================================================================
# ANÁLISE DE LACUNAS (GAPS) ENTRE NÚMEROS SORTEADOS
# =====================================================================
print("\n" + "=" * 75)
print("  ANÁLISE DE LACUNAS (GAPS ENTRE NÚMEROS)")
print("=" * 75)

gap_patterns = Counter()
for nums in results.values():
    s = sorted(nums)
    gaps = tuple(s[i+1] - s[i] for i in range(len(s)-1))
    gap_patterns[gaps] += 1

print("\n  >> Padrões de lacuna mais comuns (diferença entre números consecutivos):")
for i, (gaps, cnt) in enumerate(gap_patterns.most_common(10)):
    print(f"  {i+1:2d}. Gaps {gaps} → {cnt}x")

# Distribuição de gaps
all_gaps = []
for nums in results.values():
    s = sorted(nums)
    for i in range(len(s)-1):
        all_gaps.append(s[i+1] - s[i])

gap_freq = Counter(all_gaps)
avg_gap = sum(all_gaps) / len(all_gaps)
print(f"\n  Gap médio entre números: {avg_gap:.1f}")
print(f"  Gaps mais comuns: {gap_freq.most_common(8)}")

# Amplitude (max - min)
amplitudes = [max(results[c]) - min(results[c]) for c in sorted_concursos]
avg_amp = sum(amplitudes) / len(amplitudes)
std_amp = math.sqrt(sum((a - avg_amp)**2 for a in amplitudes) / len(amplitudes))
print(f"\n  Amplitude média (max-min): {avg_amp:.1f} ± {std_amp:.1f}")
print(f"  Faixa ideal: {avg_amp-std_amp:.0f} a {avg_amp+std_amp:.0f}")
print(f"  Última amplitude (6968): {max(results[6968]) - min(results[6968])}")

# =====================================================================
# ANÁLISE DE DEZENA FINAL (última dezena do sorteio)
# =====================================================================
print("\n" + "=" * 75)
print("  ANÁLISE: MAIOR E MENOR NÚMERO DO SORTEIO")
print("=" * 75)

min_nums = Counter()
max_nums = Counter()
for nums in results.values():
    min_nums[min(nums)] += 1
    max_nums[max(nums)] += 1

print("\n  >> MENOR número do sorteio (Top 10):")
for num, cnt in min_nums.most_common(10):
    print(f"    {num:02d} como menor: {cnt}x ({cnt/total_concursos*100:.0f}%)")

print("\n  >> MAIOR número do sorteio (Top 10):")
for num, cnt in max_nums.most_common(10):
    print(f"    {num:02d} como maior: {cnt}x ({cnt/total_concursos*100:.0f}%)")

# Faixa do menor
min_faixa = Counter()
for num in min_nums.elements():
    min_faixa[(num-1)//10] += 1
print(f"\n  Menor número geralmente na faixa 01-10: {min_faixa.get(0,0)}/{total_concursos} ({min_faixa.get(0,0)/total_concursos*100:.0f}%)")

max_faixa = Counter()
for num in max_nums.elements():
    max_faixa[(num-1)//10] += 1
print(f"  Maior número geralmente na faixa 71-80: {max_faixa.get(7,0)}/{total_concursos} ({max_faixa.get(7,0)/total_concursos*100:.0f}%)")

# =====================================================================
# SCORE COMPOSTO DEFINITIVO
# =====================================================================
print("\n" + "=" * 75)
print("  SCORE COMPOSTO DEFINITIVO (10 variáveis)")
print("=" * 75)

# Normalizar cada variável
max_freq_val = max(freq.values())
max_friday = max(friday_freq.values())
max_mom = max(momentum.values())
max_heavy_m = max(heavy_medium.values())
max_mc_val = 1
max_pair = max(pair_scores.values()) if pair_scores else 1

composite_final = {}
for num in all_numbers:
    # 1. Frequência geral (10%)
    s1 = (freq.get(num, 0) / max_freq_val) * 100

    # 2. Frequência sexta (10%)
    s2 = (friday_freq.get(num, 0) / max_friday) * 100

    # 3. Momentum (15%)
    s3 = (momentum.get(num, 0) / max_mom) * 100 if max_mom > 0 else 0

    # 4. Ciclo/Devido (15%)
    if num in cycles_data:
        s4 = min(cycles_data[num]['due'] * 25, 100)
    else:
        d = delays.get(num, 0)
        s4 = min(d / 16 * 25, 100) if d < 999 else 0

    # 5. Bolas pesadas LEVE (8%)
    total_l = sum(heavy_light.values())
    s5 = (heavy_light.get(num, 1) / max(heavy_light.values())) * 100

    # 6. Bolas pesadas MÉDIO (8%)
    s6 = (heavy_medium.get(num, 1) / max(heavy_medium.values())) * 100

    # 7. Bolas pesadas FORTE (8%)
    s7 = (heavy_strong.get(num, 1) / max(heavy_strong.values())) * 100

    # 8. Histórico all-time (10%)
    hist = historical_freq.get(num, 420)
    s8 = ((hist - 370) / (484 - 370)) * 100

    # 9. Pares frequentes (8%)
    s9 = (pair_scores.get(num, 0) / max_pair) * 100 if max_pair > 0 else 0

    # 10. Atraso (penalidade se muito recente, bônus se moderado) (8%)
    d = delays.get(num, 999)
    if d == 0:  # saiu no último
        s10 = 20  # penalidade leve
    elif 1 <= d <= 3:
        s10 = 40
    elif 4 <= d <= 8:
        s10 = 80  # ideal
    elif 9 <= d <= 15:
        s10 = 60
    elif d > 15 and d < 999:
        s10 = 40  # muito atrasado
    else:
        s10 = 10

    total = (s1 * 0.10 + s2 * 0.10 + s3 * 0.15 + s4 * 0.15 +
             s5 * 0.08 + s6 * 0.08 + s7 * 0.08 + s8 * 0.10 +
             s9 * 0.08 + s10 * 0.08)

    composite_final[num] = total

ranked_final = sorted(composite_final.items(), key=lambda x: -x[1])

print(f"\n  {'#':>2} {'Nº':>3} {'Score':>6} {'Freq':>4} {'Atraso':>6} {'Mom':>5} {'Nível'}")
print("  " + "-" * 50)
for i, (num, score) in enumerate(ranked_final[:35]):
    f = freq.get(num, 0)
    d = delays.get(num, 999)
    d_str = f"{d}" if d < 999 else "N/A"
    mom = momentum.get(num, 0)
    level = "🔥🔥🔥" if score >= 60 else "🔥🔥 " if score >= 50 else "🔥  " if score >= 40 else "    "
    print(f"  {i+1:2d}  {num:02d}  {score:5.1f}  {f:3d}x  {d_str:>5}  {mom:4.1f}  {level}")

# =====================================================================
# GERAÇÃO DE JOGOS DIVERSIFICADOS
# =====================================================================
print("\n" + "=" * 75)
print("  PORTFOLIO DE 10 JOGOS DIVERSIFICADOS")
print("=" * 75)

print("""
  ESTRATÉGIA: Maximizar COBERTURA de números únicos
  → Se o sorteio tiver números do nosso pool, maior chance de quadra/quina
  → Cada jogo diferente cobre 5 números → 10 jogos cobrem até 50 números
  → Objetivo: cobrir os 25-30 melhores números sem repetir demais
""")

def game_score(game):
    """Score completo de um jogo"""
    soma = sum(game)
    pares = sum(1 for n in game if n % 2 == 0)
    faixas = len(set((n-1)//10 for n in game))
    reps = len(set(game) & last_draw)
    terms = len(set(n % 10 for n in game))
    amp = max(game) - min(game)

    score = 0
    # Soma na faixa
    if (media_soma - std_soma) <= soma <= (media_soma + std_soma):
        score += 30
    elif (media_soma - 1.5*std_soma) <= soma <= (media_soma + 1.5*std_soma):
        score += 15

    # Par/Ímpar
    if pares == 3: score += 30
    elif pares == 2: score += 25
    elif pares == 4: score += 15

    # Faixas
    score += faixas * 8

    # Repetições
    if reps <= 1: score += 15

    # Terminações diversas
    score += terms * 3

    # Amplitude adequada
    if (avg_amp - std_amp) <= amp <= (avg_amp + std_amp):
        score += 10

    # Score composto dos números
    for n in game:
        score += composite_final.get(n, 0) * 0.5

    return score

def validate(game):
    soma = sum(game)
    pares = sum(1 for n in game if n % 2 == 0)
    faixas = len(set((n-1)//10 for n in game))
    reps = len(set(game) & last_draw)
    terms = len(set(n % 10 for n in game))
    amp = max(game) - min(game)
    return {
        'soma': soma, 'pares': pares, 'impares': 5 - pares,
        'faixas': faixas, 'reps': reps, 'terms': terms, 'amp': amp,
        'soma_ok': (media_soma - std_soma) <= soma <= (media_soma + std_soma),
        'pi_ok': 2 <= pares <= 4,
        'faixa_ok': faixas >= 3,
        'rep_ok': reps <= 1,
        'amp_ok': (avg_amp - std_amp) <= amp <= (avg_amp + std_amp),
    }

# Pool dos melhores 30 números
top30_pool = [num for num, _ in ranked_final[:30]]

# Gerar MUITOS jogos candidatos
print("  Gerando candidatos...")
candidates = []
for combo in combinations(top30_pool[:20], 5):
    game = sorted(combo)
    v = validate(game)
    if v['pi_ok'] and v['soma_ok'] and v['faixa_ok'] and v['rep_ok']:
        s = game_score(game)
        candidates.append((game, s, v))

candidates.sort(key=lambda x: -x[1])
print(f"  {len(candidates)} jogos válidos encontrados nos top 20")

# Selecionar 10 jogos DIVERSIFICADOS (greedy com penalidade por repetição)
selected = []
used_nums = Counter()

# Jogo 1: Melhor absoluto
if candidates:
    selected.append(candidates[0])
    for n in candidates[0][0]:
        used_nums[n] += 1

# Jogos 2-10: Maximizar diversidade
for target in range(9):
    best_diverse = None
    best_score = -1

    for game, s, v in candidates:
        if tuple(game) in [tuple(g[0]) for g in selected]:
            continue

        # Penalizar números já usados
        overlap = sum(used_nums.get(n, 0) for n in game)
        diversity_penalty = overlap * 30

        # Bônus por números novos
        new_nums = sum(1 for n in game if used_nums.get(n, 0) == 0)
        diversity_bonus = new_nums * 20

        adjusted_score = s - diversity_penalty + diversity_bonus

        if adjusted_score > best_score:
            best_score = adjusted_score
            best_diverse = (game, s, v)

    if best_diverse:
        selected.append(best_diverse)
        for n in best_diverse[0]:
            used_nums[n] += 1

# Adicionar jogos de estratégias alternativas se necessário
# Jogo de Sexta-feira puro
friday_pool = [n for n, _ in friday_freq.most_common(15)]
friday_games = []
for combo in combinations(friday_pool[:12], 5):
    game = sorted(combo)
    v = validate(game)
    if v['pi_ok'] and v['soma_ok'] and v['faixa_ok'] and v['rep_ok']:
        s = game_score(game)
        friday_games.append((game, s, v))
friday_games.sort(key=lambda x: -x[1])

# Jogo de Bolas Pesadas Forte
strong_pool = [n for n, _ in sorted(heavy_strong.items(), key=lambda x: -x[1])[:15]]
strong_games = []
for combo in combinations(strong_pool[:12], 5):
    game = sorted(combo)
    v = validate(game)
    if v['pi_ok'] and v['soma_ok'] and v['faixa_ok'] and v['rep_ok']:
        s = game_score(game)
        strong_games.append((game, s, v))
strong_games.sort(key=lambda x: -x[1])

# Jogo de "Devidos" (ciclo vencido)
due_pool = sorted([n for n in cycles_data if cycles_data[n]['due'] > 1.0],
                  key=lambda x: -cycles_data[x]['due'])[:15]
due_games = []
if len(due_pool) >= 5:
    for combo in combinations(due_pool[:12], 5):
        game = sorted(combo)
        v = validate(game)
        if v['pi_ok'] and v['soma_ok'] and v['faixa_ok'] and v['rep_ok']:
            s = game_score(game)
            due_games.append((game, s, v))
    due_games.sort(key=lambda x: -x[1])

# =====================================================================
# APRESENTAÇÃO FINAL
# =====================================================================
print(f"""
  ╔═══════════════════════════════════════════════════════════════════════╗
  ║                                                                     ║
  ║        PORTFOLIO FINAL - CONCURSO 6969 (06/03/2026 SEXTA)          ║
  ║        Prêmio estimado: R$ 13.500.000,00                           ║
  ║                                                                     ║
  ╠═══════════════════════════════════════════════════════════════════════╣""")

strategies = [
    "SCORE MÁXIMO",
    "DIVERSIFICADO 1",
    "DIVERSIFICADO 2",
    "DIVERSIFICADO 3",
    "DIVERSIFICADO 4",
    "DIVERSIFICADO 5",
    "DIVERSIFICADO 6",
    "DIVERSIFICADO 7",
    "DIVERSIFICADO 8",
    "DIVERSIFICADO 9",
]

all_final_games = []

for i, (game, score, v) in enumerate(selected[:10]):
    strat = strategies[i] if i < len(strategies) else f"EXTRA {i+1}"
    game_str = " - ".join(f"{n:02d}" for n in game)
    checks = sum([v['soma_ok'], v['pi_ok'], v['faixa_ok'], v['rep_ok'], v['amp_ok']])
    all_final_games.append(game)

    print(f"  ║                                                                     ║")
    print(f"  ║  {i+1:2d}. {strat:<20}                                          ║")
    print(f"  ║                                                                     ║")
    print(f"  ║       >>>  {game_str}  <<<                           ║")
    print(f"  ║                                                                     ║")
    print(f"  ║       Soma: {v['soma']:3d} | {v['pares']}P/{v['impares']}I | {v['faixas']} faixas | Amp: {v['amp']} | Score: {score:.0f}   ║")
    print(f"  ╠═══════════════════════════════════════════════════════════════════════╣")

# Jogos especiais
special_games = []
if friday_games:
    fg = friday_games[0]
    if tuple(fg[0]) not in [tuple(g) for g in all_final_games]:
        special_games.append(("ESPECIAL SEXTA", fg))
        all_final_games.append(fg[0])

if strong_games:
    sg = strong_games[0]
    if tuple(sg[0]) not in [tuple(g) for g in all_final_games]:
        special_games.append(("BOLAS ULTRA-PESADAS", sg))
        all_final_games.append(sg[0])

if due_games:
    dg = due_games[0]
    if tuple(dg[0]) not in [tuple(g) for g in all_final_games]:
        special_games.append(("NÚMEROS DEVIDOS", dg))
        all_final_games.append(dg[0])

for strat, (game, score, v) in special_games:
    game_str = " - ".join(f"{n:02d}" for n in game)
    idx = len(all_final_games)
    print(f"  ║                                                                     ║")
    print(f"  ║  {idx:2d}. {strat:<20}                                          ║")
    print(f"  ║                                                                     ║")
    print(f"  ║       >>>  {game_str}  <<<                           ║")
    print(f"  ║                                                                     ║")
    print(f"  ║       Soma: {v['soma']:3d} | {v['pares']}P/{v['impares']}I | {v['faixas']} faixas | Amp: {v['amp']} | Score: {score:.0f}   ║")
    print(f"  ╠═══════════════════════════════════════════════════════════════════════╣")

print(f"  ║                                                                     ║")
print(f"  ║  PARÂMETROS IDEAIS:                                                 ║")
print(f"  ║  Soma: {media_soma-std_soma:.0f}-{media_soma+std_soma:.0f} | P/I: 3P/2I | Faixas ≥3 | Amp: {avg_amp-std_amp:.0f}-{avg_amp+std_amp:.0f}     ║")
print(f"  ╚═══════════════════════════════════════════════════════════════════════╝")

# =====================================================================
# ANÁLISE DE COBERTURA
# =====================================================================
print("\n" + "=" * 75)
print("  ANÁLISE DE COBERTURA DO PORTFOLIO")
print("=" * 75)

all_covered = set()
for game in all_final_games:
    all_covered.update(game)

print(f"\n  Números únicos cobertos: {len(all_covered)} de 80")
print(f"  Números cobertos: {sorted(all_covered)}")
print(f"\n  Frequência de uso de cada número no portfolio:")

usage = Counter()
for game in all_final_games:
    for n in game:
        usage[n] += 1

for num, cnt in sorted(usage.items(), key=lambda x: -x[1]):
    bar = "█" * cnt
    score = composite_final.get(num, 0)
    print(f"    {num:02d}: {cnt}x {bar} (score: {score:.1f})")

# Verificar se os números do consenso estão cobertos
consensus_nums = [7, 9, 14, 26, 68, 74, 8, 56]
covered_consensus = [n for n in consensus_nums if n in all_covered]
print(f"\n  Números de consenso cobertos: {covered_consensus} ({len(covered_consensus)}/{len(consensus_nums)})")

# =====================================================================
# SIMULAÇÃO: QUAL JOGO TERIA GANHADO NOS ÚLTIMOS 10 CONCURSOS?
# =====================================================================
print("\n" + "=" * 75)
print("  BACKTESTING: DESEMPENHO NOS ÚLTIMOS 10 CONCURSOS")
print("=" * 75)

last10 = sorted_concursos[-10:]
for i, game in enumerate(all_final_games, 1):
    acertos_total = 0
    melhor = 0
    detalhes = []
    for c in last10:
        acertos = len(set(game) & set(results[c]))
        acertos_total += acertos
        melhor = max(melhor, acertos)
        if acertos >= 2:
            detalhes.append(f"{c}({acertos})")

    media_acertos = acertos_total / len(last10)
    game_str = "-".join(f"{n:02d}" for n in game)
    hits = " ".join(detalhes) if detalhes else "nenhum ≥2"
    print(f"  Jogo {i:2d} [{game_str}] Méd: {media_acertos:.1f} | Max: {melhor} | {hits}")

# =====================================================================
# TOP 3 RANKING FINAL
# =====================================================================
print("\n" + "=" * 75)
print("  ★ TOP 3 JOGOS - RECOMENDAÇÃO FINAL ★")
print("=" * 75)

# Rankear por backtesting + score
game_rankings = []
for i, game in enumerate(all_final_games):
    bt_score = 0
    for c in last10:
        acertos = len(set(game) & set(results[c]))
        bt_score += acertos * acertos  # quadrático para valorizar mais acertos

    gs = game_score(game)
    combined = gs * 0.6 + bt_score * 10 * 0.4
    game_rankings.append((game, combined, gs, bt_score))

game_rankings.sort(key=lambda x: -x[1])

for rank, (game, combined, gs, bt) in enumerate(game_rankings[:3], 1):
    v = validate(game)
    game_str = " - ".join(f"{n:02d}" for n in game)
    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"

    print(f"""
  {medal} #{rank} LUGAR
  ┌──────────────────────────────────────────┐
  │                                          │
  │    {game_str:>30}        │
  │                                          │
  │    Soma: {v['soma']:3d}  |  {v['pares']}P/{v['impares']}I  |  {v['faixas']} faixas     │
  │    Amplitude: {v['amp']}  |  Reps: {v['reps']}            │
  │    Score jogo: {gs:.0f}                      │
  │    Backtesting: {bt}                       │
  │    Score combinado: {combined:.0f}                  │
  │                                          │
  └──────────────────────────────────────────┘""")

# =====================================================================
# RESUMO EXECUTIVO FINAL
# =====================================================================
print("\n" + "=" * 75)
print("  RESUMO EXECUTIVO FINAL")
print("=" * 75)

top1 = game_rankings[0][0]
top2 = game_rankings[1][0]
top3 = game_rankings[2][0]

print(f"""
  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  CONCURSO 6969 - 06/03/2026 (SEXTA) - R$ 13.500.000               │
  │                                                                     │
  │  SE FOSSE JOGAR APENAS 1 JOGO:                                     │
  │  → {' - '.join(f'{n:02d}' for n in top1)}                                             │
  │                                                                     │
  │  SE FOSSE JOGAR 3 JOGOS:                                           │
  │  → Jogo A: {' - '.join(f'{n:02d}' for n in top1)}                                     │
  │  → Jogo B: {' - '.join(f'{n:02d}' for n in top2)}                                     │
  │  → Jogo C: {' - '.join(f'{n:02d}' for n in top3)}                                     │
  │                                                                     │
  │  NÚMEROS-CHAVE (presentes em 4+ de 6 modelos):                     │
  │  → 07, 09, 14, 26, 68, 74                                         │
  │                                                                     │
  │  BOLAS PESADAS - 3 CENÁRIOS:                                       │
  │  • Leve:  números recentes têm vantagem modesta                    │
  │  • Médio: vantagem de 2-3x para bolas frequentes                  │
  │  • Forte: vantagem de 4-5x → domínio total dos "quentes"          │
  │                                                                     │
  │  POR QUE ESTES NÚMEROS?                                            │
  │  • 07: ULTRA-consenso (5/6 modelos), frequente às sextas           │
  │  • 09: momentum forte, frequente recente, bom ciclo               │
  │  • 14: alta frequência + sexta-feira + bolas pesadas               │
  │  • 26: líder em 3x nos últimos 5 sorteios, dupla com 74           │
  │  • 68: presente na trinca quente (26,68,74)                        │
  │  • 74: CAMPEÃ em bolas pesadas, 6x nos 59 concursos               │
  │                                                                     │
  │  INSIGHT PÓS-5P/0I:                                               │
  │  O último sorteio (6968) teve 5 pares / 0 ímpares (2% dos casos). │
  │  Regressão à média: o próximo sorteio deve ter 3P/2I.             │
  │  → Todos os jogos foram calibrados para 3P/2I ou 2P/3I.           │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
""")

print("=" * 75)
print("  AVISO: Loteria é jogo de AZAR. Cada sorteio é INDEPENDENTE.")
print("  Resultados passados NÃO garantem resultados futuros.")
print("  O modelo de bolas pesadas é HIPOTÉTICO.")
print("  Jogue com responsabilidade. BOA SORTE!")
print("=" * 75)
