#!/usr/bin/env python3
"""
=============================================================================
ANÁLISE ULTRA-ESTRATÉGICA DA QUINA - CONCURSO 6969 (06/03/2026 - SEXTA)
=============================================================================
Base: 59 concursos (6910-6968) + Histórico all-time
14 Modelos: Frequência, Atraso, Momentum, Ciclos, Pares, Trincas,
           Dia da Semana, Pós-5Pares, Mapa de Calor, Fibonacci,
           Bolas Pesadas, Monte Carlo, Score Composto, Otimização Final
=============================================================================
"""

from collections import Counter, defaultdict
from itertools import combinations
import random
import math

# =====================================================================
# BASE DE DADOS EXPANDIDA: 59 CONCURSOS (6910-6968)
# =====================================================================

results = {
    # Dezembro 2025
    6910: [2, 18, 20, 49, 68],
    6911: [3, 51, 56, 59, 72],
    6912: [4, 43, 44, 58, 62],
    6913: [25, 31, 38, 42, 58],
    6914: [25, 41, 48, 49, 66],
    6915: [5, 19, 21, 51, 66],
    6916: [8, 54, 58, 72, 76],
    6917: [11, 15, 29, 48, 57],
    6918: [9, 21, 24, 63, 69],
    6919: [4, 6, 9, 26, 64],
    # Janeiro 2026
    6920: [4, 28, 34, 42, 47],
    6921: [26, 50, 69, 74, 77],
    6922: [16, 26, 36, 51, 56],
    6923: [18, 34, 41, 57, 63],
    6924: [4, 13, 49, 52, 66],
    6925: [9, 25, 44, 46, 62],
    6926: [14, 29, 40, 79, 80],
    6927: [3, 20, 49, 57, 69],
    6928: [33, 44, 56, 66, 72],
    6929: [8, 13, 14, 53, 54],
    6930: [5, 16, 22, 65, 80],
    6931: [48, 69, 73, 77, 79],
    6932: [28, 33, 65, 71, 76],
    6933: [51, 55, 62, 64, 69],
    6934: [5, 15, 25, 40, 67],
    6935: [5, 7, 33, 58, 64],
    6936: [8, 15, 21, 39, 48],
    6937: [16, 17, 46, 56, 70],
    6938: [3, 4, 21, 32, 52],
    6939: [10, 26, 27, 55, 73],
    6940: [24, 53, 66, 73, 77],
    # Fevereiro 2026
    6941: [12, 32, 34, 57, 64],
    6942: [16, 33, 34, 50, 71],
    6943: [22, 23, 35, 40, 44],
    6944: [2, 8, 30, 56, 61],
    6945: [33, 61, 66, 68, 70],
    6946: [1, 48, 53, 75, 80],
    6947: [6, 30, 52, 60, 79],
    6948: [3, 21, 32, 46, 57],
    6949: [21, 51, 60, 67, 73],
    6950: [1, 6, 24, 47, 60],
    6951: [1, 10, 20, 44, 66],
    6952: [1, 2, 57, 62, 79],
    6953: [7, 22, 35, 58, 63],
    6954: [2, 29, 34, 44, 78],
    6955: [6, 8, 18, 23, 74],
    6956: [10, 38, 51, 64, 68],
    6957: [11, 14, 18, 67, 74],
    6958: [9, 14, 24, 55, 68],
    6959: [7, 12, 27, 49, 54],
    # Fevereiro/Março 2026
    6960: [7, 8, 14, 39, 52],
    6961: [15, 45, 55, 62, 65],
    6962: [15, 25, 37, 79, 80],
    6963: [6, 19, 29, 62, 74],
    6964: [3, 9, 30, 56, 58],
    6965: [7, 12, 26, 68, 74],
    6966: [9, 19, 26, 28, 52],
    6967: [26, 47, 68, 74, 77],
    6968: [8, 14, 44, 56, 72],
}

# Dia da semana para cada concurso (0=seg, 1=ter, 2=qua, 3=qui, 4=sex, 5=sáb)
# O concurso 6969 é SEXTA-FEIRA
day_of_week = {
    6910: 1, 6911: 2, 6912: 4, 6913: 5, 6914: 0, 6915: 1, 6916: 3, 6917: 4, 6918: 5, 6919: 0,
    6920: 1, 6921: 2, 6922: 3, 6923: 4, 6924: 5, 6925: 0, 6926: 1, 6927: 2, 6928: 3, 6929: 4,
    6930: 5, 6931: 0, 6932: 1, 6933: 2, 6934: 3, 6935: 4, 6936: 5, 6937: 0, 6938: 1, 6939: 2,
    6940: 3, 6941: 4, 6942: 5, 6943: 0, 6944: 1, 6945: 2, 6946: 3, 6947: 4, 6948: 5, 6949: 0,
    6950: 1, 6951: 2, 6952: 3, 6953: 4, 6954: 5, 6955: 2, 6956: 3, 6957: 4, 6958: 5, 6959: 0,
    6960: 1, 6961: 2, 6962: 3, 6963: 4, 6964: 5, 6965: 0, 6966: 1, 6967: 2, 6968: 3,
}

# Histórico all-time (top 30 + bottom 10)
historical_freq = {
    4: 484, 52: 470, 26: 468, 49: 462, 31: 460, 44: 458, 39: 456,
    16: 455, 53: 454, 15: 452, 56: 451, 62: 450, 14: 449, 64: 448,
    8: 447, 33: 446, 7: 445, 68: 444, 55: 443, 9: 442, 58: 441,
    34: 440, 21: 439, 3: 438, 51: 437, 57: 436, 66: 435, 29: 434,
    6: 433, 24: 432,
    # Menos sorteados
    47: 376, 76: 380, 73: 385, 75: 388, 42: 390, 36: 392, 41: 394,
    17: 396, 50: 398, 13: 400,
}

all_numbers = list(range(1, 81))
sorted_concursos = sorted(results.keys())
total_concursos = len(results)
NEXT_CONCURSO = 6969
NEXT_DOW = 4  # Sexta-feira

print("=" * 75)
print("  ╔═══════════════════════════════════════════════════════════════════╗")
print("  ║   ANÁLISE ULTRA-ESTRATÉGICA DA QUINA - CONCURSO 6969            ║")
print("  ║   06/03/2026 (SEXTA-FEIRA) | Prêmio: ~R$ 13.500.000            ║")
print(f"  ║   Base: {total_concursos} concursos (6910-6968) + histórico all-time        ║")
print("  ╚═══════════════════════════════════════════════════════════════════╝")

# =====================================================================
# COLETA BASE
# =====================================================================
all_drawn = []
for nums in results.values():
    all_drawn.extend(nums)

freq = Counter(all_drawn)
total_draws = len(all_drawn)
expected_freq = total_draws / 80

# Delays
delays = {}
for num in all_numbers:
    last_seen = None
    for c in reversed(sorted_concursos):
        if num in results[c]:
            last_seen = c
            break
    delays[num] = (NEXT_CONCURSO - last_seen) if last_seen else 999

# =====================================================================
# MODELO 1: FREQUÊNCIA POR DIA DA SEMANA (SEXTA-FEIRA)
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 1: PADRÃO DE SEXTA-FEIRA")
print("  (Hoje é sexta → filtrando apenas sorteios de sexta)")
print("=" * 75)

friday_concursos = [c for c in sorted_concursos if day_of_week.get(c) == NEXT_DOW]
friday_nums = []
for c in friday_concursos:
    friday_nums.extend(results[c])

friday_freq = Counter(friday_nums)
total_friday = len(friday_concursos)

print(f"\n  Sorteios de sexta-feira na base: {total_friday}")
print(f"  Concursos: {friday_concursos}")

print(f"\n  >> TOP 20 NÚMEROS QUE MAIS SAEM ÀS SEXTAS:")
for i, (num, cnt) in enumerate(friday_freq.most_common(20)):
    pct = cnt / total_friday * 100
    bar = "█" * (cnt * 3)
    print(f"  {i+1:2d}. {num:02d} → {cnt}x em {total_friday} sextas ({pct:.0f}%) {bar}")

# Par/Ímpar nas sextas
print(f"\n  >> PAR/ÍMPAR nas sextas:")
friday_pi = Counter()
for c in friday_concursos:
    p = sum(1 for n in results[c] if n % 2 == 0)
    friday_pi[f"{p}P/{5-p}I"] += 1
for dist in sorted(friday_pi.keys()):
    cnt = friday_pi[dist]
    print(f"    {dist}: {cnt}x ({cnt/total_friday*100:.0f}%)")

# Soma nas sextas
friday_somas = [sum(results[c]) for c in friday_concursos]
friday_soma_avg = sum(friday_somas) / len(friday_somas)
friday_soma_std = math.sqrt(sum((s - friday_soma_avg)**2 for s in friday_somas) / len(friday_somas))
print(f"\n  >> SOMA nas sextas: Média={friday_soma_avg:.0f} ± {friday_soma_std:.0f}")
print(f"     Faixa ideal: {friday_soma_avg-friday_soma_std:.0f} a {friday_soma_avg+friday_soma_std:.0f}")

# =====================================================================
# MODELO 2: O QUE ACONTECE DEPOIS DE SORTEIO 5P/0I (TODOS PARES)
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 2: PÓS-SORTEIO 5 PARES / 0 ÍMPARES")
print("  (O último sorteio 6968 teve 5P/0I → o que vem depois?)")
print("=" * 75)

# Encontrar todos os sorteios 5P/0I e ver o que veio depois
all_5p = []
for i, c in enumerate(sorted_concursos):
    pares = sum(1 for n in results[c] if n % 2 == 0)
    if pares == 5 and i + 1 < len(sorted_concursos):
        next_c = sorted_concursos[i + 1]
        all_5p.append((c, results[c], next_c, results[next_c]))

print(f"\n  Sorteios com 5P/0I encontrados: {len(all_5p) + 1}")
print(f"  (O 6968 é o mais recente: {results[6968]})")

if all_5p:
    print(f"\n  >> O QUE SAIU DEPOIS DE 5P/0I:")
    post_5p_nums = []
    for prev_c, prev_nums, next_c, next_nums in all_5p:
        pares_next = sum(1 for n in next_nums if n % 2 == 0)
        print(f"    {prev_c} {prev_nums} → {next_c} {next_nums} ({pares_next}P/{5-pares_next}I)")
        post_5p_nums.extend(next_nums)

    if post_5p_nums:
        post_freq = Counter(post_5p_nums)
        print(f"\n  >> Números mais frequentes pós-5P/0I:")
        for num, cnt in post_freq.most_common(10):
            print(f"    {num:02d} → {cnt}x")

        post_pi = Counter()
        for _, _, _, next_nums in all_5p:
            p = sum(1 for n in next_nums if n % 2 == 0)
            post_pi[f"{p}P/{5-p}I"] += 1
        print(f"\n  >> Distribuição Par/Ímpar pós-5P/0I:")
        for dist, cnt in sorted(post_pi.items()):
            print(f"    {dist}: {cnt}x")
else:
    print("  Nenhum caso anterior de 5P/0I encontrado na base.")
    print("  → Tendência: FORTE correção para mais ímpares (regressão à média)")

# =====================================================================
# MODELO 3: MAPA DE CALOR DO TABULEIRO 8x10
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 3: MAPA DE CALOR DO TABULEIRO (últimos 15 concursos)")
print("=" * 75)

# Últimos 15 concursos
recent_15 = sorted_concursos[-15:]
recent_freq = Counter()
for c in recent_15:
    for n in results[c]:
        recent_freq[n] += 1

print("\n  Tabuleiro 1-80 (calor = freq nos últimos 15 concursos):")
print("  " + "-" * 52)
for row in range(8):
    line = f"  {row*10+1:02d}-{row*10+10:02d} │"
    for col in range(10):
        num = row * 10 + col + 1
        f = recent_freq.get(num, 0)
        if f >= 3:
            line += f" [{num:02d}]"  # muito quente
        elif f >= 2:
            line += f"  {num:02d} "
        elif f == 1:
            line += f"  {num:02d}."
        else:
            line += "   · "
    print(line)
print("  " + "-" * 52)
print("  [XX] = 3+ vezes | XX = 2 vezes | XX. = 1 vez | · = 0")

# Zonas quentes
print("\n  >> ZONAS QUENTES (≥3 aparições em 15 concursos):")
hot_zones = sorted([n for n in all_numbers if recent_freq.get(n, 0) >= 3])
print(f"  {hot_zones}")

# =====================================================================
# MODELO 4: SEQUÊNCIAS DE FIBONACCI E PRIMO
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 4: NÚMEROS PRIMOS E FIBONACCI NO TABULEIRO")
print("=" * 75)

primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79]
fib = [1,2,3,5,8,13,21,34,55]

prime_drawn = [n for n in all_drawn if n in primes]
non_prime_drawn = [n for n in all_drawn if n not in primes]
pct_prime = len(prime_drawn) / total_draws * 100

print(f"\n  Primos no tabuleiro (1-80): {len(primes)} de 80 ({len(primes)/80*100:.0f}%)")
print(f"  Primos nos sorteios: {len(prime_drawn)} de {total_draws} ({pct_prime:.1f}%)")
print(f"  → {'Primos estão SOBREREPRESENTADOS' if pct_prime > len(primes)/80*100 else 'Primos estão sub-representados'}")

fib_drawn = [n for n in all_drawn if n in fib]
pct_fib = len(fib_drawn) / total_draws * 100
print(f"\n  Fibonacci no tabuleiro: {len(fib)} de 80 ({len(fib)/80*100:.0f}%)")
print(f"  Fibonacci nos sorteios: {len(fib_drawn)} de {total_draws} ({pct_fib:.1f}%)")

# Quantos primos por sorteio
print(f"\n  >> PRIMOS POR SORTEIO:")
prime_per_draw = Counter()
for nums in results.values():
    p = sum(1 for n in nums if n in primes)
    prime_per_draw[p] += 1
for cnt in sorted(prime_per_draw.keys()):
    total = prime_per_draw[cnt]
    pct = total / total_concursos * 100
    print(f"    {cnt} primos: {total}x ({pct:.0f}%)")

# =====================================================================
# MODELO 5: ANÁLISE DE TERMINAÇÕES (último dígito)
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 5: ANÁLISE DE TERMINAÇÕES (último dígito)")
print("=" * 75)

term_freq = Counter()
for n in all_drawn:
    term_freq[n % 10] += 1

print("\n  Frequência por terminação:")
for t in range(10):
    cnt = term_freq.get(t, 0)
    expected = total_draws / 10
    diff = cnt - expected
    bar = "█" * int(cnt / 2)
    signal = "↑" if diff > 3 else "↓" if diff < -3 else "="
    print(f"  Terminal {t}: {cnt:3d}x ({cnt/total_draws*100:4.1f}%) {signal} {bar}")

# Terminações do último sorteio: 8, 14→4, 44→4, 56→6, 72→2
last_terms = [n % 10 for n in results[6968]]
print(f"\n  Terminações do último sorteio (6968): {last_terms}")
print(f"  Terminações ausentes no último: {sorted(set(range(10)) - set(last_terms))}")

# =====================================================================
# MODELO 6: PARES, TRINCAS E QUADRAS FREQUENTES
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 6: COMBINAÇÕES FREQUENTES (Pares + Trincas)")
print("=" * 75)

pair_count = Counter()
triple_count = Counter()
for nums in results.values():
    s = sorted(nums)
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            pair_count[(s[i], s[j])] += 1
            for k in range(j+1, len(s)):
                triple_count[(s[i], s[j], s[k])] += 1

print("\n  >> TOP 20 DUPLAS:")
for i, (pair, cnt) in enumerate(pair_count.most_common(20)):
    print(f"  {i+1:2d}. ({pair[0]:02d}, {pair[1]:02d}) → {cnt}x")

print("\n  >> TOP 10 TRINCAS:")
for i, (triple, cnt) in enumerate(triple_count.most_common(10)):
    print(f"  {i+1:2d}. ({triple[0]:02d}, {triple[1]:02d}, {triple[2]:02d}) → {cnt}x")

# Pares que saíram nos últimos 5 concursos
print("\n  >> DUPLAS ATIVAS (saíram nos últimos 5 concursos):")
recent_5 = sorted_concursos[-5:]
recent_pairs = Counter()
for c in recent_5:
    s = sorted(results[c])
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            recent_pairs[(s[i], s[j])] += 1

for pair, cnt in recent_pairs.most_common(10):
    total = pair_count[pair]
    print(f"    ({pair[0]:02d}, {pair[1]:02d}) → {cnt}x recente, {total}x total")

# =====================================================================
# MODELO 7: MOMENTUM AVANÇADO (3 janelas + tendência)
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 7: MOMENTUM AVANÇADO")
print("=" * 75)

def freq_window(window_size):
    recent = sorted_concursos[-window_size:]
    nums = []
    for c in recent:
        nums.extend(results[c])
    return Counter(nums)

freq_5 = freq_window(5)
freq_10 = freq_window(10)
freq_20 = freq_window(20)

momentum = {}
for num in all_numbers:
    r5 = freq_5.get(num, 0) / 5
    r10 = freq_10.get(num, 0) / 10
    r20 = freq_20.get(num, 0) / 20
    r_all = freq.get(num, 0) / total_concursos

    # Momentum ponderado: recente vale mais
    if r_all > 0:
        mom = (r5 * 4 + r10 * 2 + r20) / 7 / r_all
    else:
        mom = (r5 * 4 + r10 * 2 + r20) * 10

    # Tendência (aceleração): comparar janela 5 vs janela 10
    accel = r5 - r10 if r10 > 0 else r5

    momentum[num] = {'score': mom, 'accel': accel, 'r5': r5, 'r10': r10, 'r20': r20}

print("\n  >> TOP 15 MOMENTUM (ponderado):")
mom_ranked = sorted(momentum.items(), key=lambda x: -x[1]['score'])
for i, (num, m) in enumerate(mom_ranked[:15]):
    trend = "⬆⬆" if m['accel'] > 0.05 else "⬆ " if m['accel'] > 0 else "⬇ "
    f = freq.get(num, 0)
    print(f"  {i+1:2d}. {num:02d} → Mom: {m['score']:.2f} {trend} | r5={m['r5']:.2f} r10={m['r10']:.2f} r20={m['r20']:.2f} | Total: {f}x")

# =====================================================================
# MODELO 8: CICLOS DE APARIÇÃO
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 8: CICLOS - NÚMEROS 'DEVIDOS'")
print("=" * 75)

cycles = defaultdict(list)
for num in all_numbers:
    appearances = [c for c in sorted_concursos if num in results[c]]
    for i in range(1, len(appearances)):
        cycles[num].append(appearances[i] - appearances[i-1])

cycle_stats = []
for num in all_numbers:
    if len(cycles[num]) >= 3:
        avg = sum(cycles[num]) / len(cycles[num])
        std = math.sqrt(sum((c - avg)**2 for c in cycles[num]) / len(cycles[num]))
        cv = std / avg if avg > 0 else 999
        last_app = max(c for c in sorted_concursos if num in results[c])
        since = NEXT_CONCURSO - last_app
        due = since / avg if avg > 0 else 0
        cycle_stats.append((num, avg, std, cv, since, due))

print("\n  >> TOP 15 NÚMEROS MAIS 'DEVIDOS' (atraso/ciclo > 1.0):")
due_ranked = sorted(cycle_stats, key=lambda x: -x[5])
for i, (num, avg, std, cv, since, due) in enumerate(due_ranked[:15]):
    f = freq.get(num, 0)
    status = "🎯" if due > 2.0 else "⚡" if due > 1.0 else "  "
    print(f"  {i+1:2d}. {num:02d} → Due: {due:.1f}x | Ciclo: {avg:.1f}±{std:.1f} | Atraso: {since} | Freq: {f}x {status}")

# =====================================================================
# MODELO 9: BOLAS PESADAS (REFINADO COM DECAIMENTO)
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 9: BOLAS PESADAS (decaimento exponencial)")
print("=" * 75)

PESO_BASE = 1.0
PESO_POR_SORTEIO = 1.0
FATOR_DECAIMENTO = 0.90  # perde 10% por concurso
BONUS_HISTORICO = 0.003

heavy_weights = {}
for num in all_numbers:
    peso = PESO_BASE
    for c in sorted_concursos:
        if num in results[c]:
            distancia = NEXT_CONCURSO - c
            peso += PESO_POR_SORTEIO * (FATOR_DECAIMENTO ** distancia)
    hist_count = historical_freq.get(num, 420)
    peso += BONUS_HISTORICO * hist_count
    heavy_weights[num] = peso

total_peso = sum(heavy_weights.values())
heavy_probs = {num: (peso / total_peso) * 100 for num, peso in heavy_weights.items()}
ranked_heavy = sorted(heavy_weights.items(), key=lambda x: -x[1])

print(f"\n  {'#':>3} {'Nº':>3} {'Peso':>7} {'Prob%':>6} {'Vantagem':>8} {'Freq':>4}")
print("  " + "-" * 40)
uniform_prob = 100 / 80
for i, (num, peso) in enumerate(ranked_heavy[:20]):
    prob = heavy_probs[num]
    adv = prob / uniform_prob
    f = freq.get(num, 0)
    bar = "█" * int(prob * 15)
    print(f"  {i+1:3d}  {num:02d}   {peso:5.2f}  {prob:5.2f}%  {adv:5.2f}x   {f:2d}x {bar}")

# =====================================================================
# MODELO 10: MONTE CARLO (50.000 simulações)
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 10: MONTE CARLO (50.000 sorteios simulados)")
print("=" * 75)

random.seed(6969)
nums_list = list(range(1, 81))
weights_list = [heavy_weights[n] for n in nums_list]

monte_carlo_freq = Counter()
N_SIM = 50000

for _ in range(N_SIM):
    drawn_set = set()
    while len(drawn_set) < 5:
        pick = random.choices(nums_list, weights=weights_list, k=1)[0]
        drawn_set.add(pick)
    for n in drawn_set:
        monte_carlo_freq[n] += 1

print(f"\n  >> TOP 20 na simulação Monte Carlo ({N_SIM} sorteios):")
for i, (num, cnt) in enumerate(monte_carlo_freq.most_common(20)):
    pct = cnt / N_SIM * 100
    bar = "█" * int(pct)
    print(f"  {i+1:2d}. {num:02d} → {cnt:6d}x ({pct:4.1f}%) {bar}")

# =====================================================================
# MODELO 11: SCORE COMPOSTO MULTI-FATOR
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 11: SCORE COMPOSTO MULTI-FATOR")
print("=" * 75)

print("""
  Ponderação:
  • Frequência recente (59 jogos): 15%
  • Frequência sexta-feira:        10%
  • Momentum (tendência):          20%
  • Ciclo/Devido:                  15%
  • Bolas Pesadas:                 15%
  • Monte Carlo:                   10%
  • Histórico all-time:            10%
  • Pares frequentes:               5%
""")

composite = {}
max_freq_val = max(freq.values()) if freq else 1
max_friday = max(friday_freq.values()) if friday_freq else 1
max_mom = max(m['score'] for m in momentum.values())
max_heavy = max(heavy_weights.values())
max_mc = max(monte_carlo_freq.values()) if monte_carlo_freq else 1

# Pair score
pair_scores = defaultdict(int)
for (a, b), cnt in pair_count.most_common(40):
    pair_scores[a] += cnt
    pair_scores[b] += cnt
max_pair = max(pair_scores.values()) if pair_scores else 1

for num in all_numbers:
    # Normalizar cada componente para 0-100
    s_freq = (freq.get(num, 0) / max_freq_val) * 100
    s_friday = (friday_freq.get(num, 0) / max_friday) * 100
    s_mom = (momentum[num]['score'] / max_mom) * 100 if max_mom > 0 else 0

    # Due score
    cycle_info = [x for x in cycle_stats if x[0] == num]
    if cycle_info:
        s_due = min(cycle_info[0][5] * 30, 100)
    else:
        d = delays.get(num, 0)
        s_due = min(d / 16 * 30, 100) if d < 999 else 0

    s_heavy = (heavy_weights.get(num, 1) / max_heavy) * 100
    s_mc = (monte_carlo_freq.get(num, 0) / max_mc) * 100
    s_hist = ((historical_freq.get(num, 420) - 370) / (484 - 370)) * 100
    s_pairs = (pair_scores.get(num, 0) / max_pair) * 100

    total = (s_freq * 0.15 + s_friday * 0.10 + s_mom * 0.20 +
             s_due * 0.15 + s_heavy * 0.15 + s_mc * 0.10 +
             s_hist * 0.10 + s_pairs * 0.05)

    composite[num] = {
        'total': total,
        'freq': s_freq, 'friday': s_friday, 'mom': s_mom,
        'due': s_due, 'heavy': s_heavy, 'mc': s_mc,
        'hist': s_hist, 'pairs': s_pairs
    }

ranked_composite = sorted(composite.items(), key=lambda x: -x[1]['total'])

print(f"  {'#':>2} {'Nº':>3} {'TOTAL':>6} │{'Freq':>5}│{'Sex':>4}│{'Mom':>5}│{'Due':>5}│{'Peso':>5}│{'MC':>5}│{'Hist':>5}│{'Par':>4}")
print("  " + "-" * 65)
for i, (num, s) in enumerate(ranked_composite[:30]):
    print(f"  {i+1:2d}  {num:02d}  {s['total']:5.1f} │{s['freq']:4.0f} │{s['friday']:3.0f} │{s['mom']:4.0f} │{s['due']:4.0f} │{s['heavy']:4.0f} │{s['mc']:4.0f} │{s['hist']:4.0f} │{s['pairs']:3.0f}")

# =====================================================================
# MODELO 12: CONSENSO ENTRE TODOS OS MODELOS
# =====================================================================
print("\n" + "=" * 75)
print("  MODELO 12: CONSENSO ENTRE MODELOS")
print("=" * 75)

# Top 10 de cada modelo
top10_composite = set(num for num, _ in ranked_composite[:10])
top10_heavy = set(num for num, _ in ranked_heavy[:10])
top10_mc = set(num for num, _ in monte_carlo_freq.most_common(10))
top10_friday = set(num for num, _ in friday_freq.most_common(10))
top10_momentum = set(num for num, _ in sorted(momentum.items(), key=lambda x: -x[1]['score'])[:10])
top10_due = set(x[0] for x in sorted(cycle_stats, key=lambda x: -x[5])[:10])

models = {
    'Composite': top10_composite,
    'Pesadas': top10_heavy,
    'Monte Carlo': top10_mc,
    'Sexta-feira': top10_friday,
    'Momentum': top10_momentum,
    'Devidos': top10_due,
}

print(f"\n  Top 10 de cada modelo:")
for name, nums in models.items():
    print(f"    {name:12s}: {sorted(nums)}")

# Contar em quantos modelos cada número aparece
model_count = Counter()
for nums in models.values():
    for n in nums:
        model_count[n] += 1

print(f"\n  >> CONSENSO (número de modelos onde aparece no Top 10):")
for count in range(6, 0, -1):
    nums = sorted([n for n, c in model_count.items() if c == count])
    if nums:
        label = "ULTRA" if count >= 5 else "ALTO" if count >= 4 else "MÉDIO" if count >= 3 else "BAIXO"
        stars = "★" * count
        print(f"    {count}/6 modelos ({label}): {nums} {stars}")

# =====================================================================
# GERAÇÃO FINAL DE JOGOS OTIMIZADOS
# =====================================================================
print("\n" + "=" * 75)
print("  JOGOS FINAIS OTIMIZADOS - CONCURSO 6969")
print("=" * 75)

# Parâmetros globais
all_somas = [sum(results[c]) for c in sorted_concursos]
media_soma = sum(all_somas) / len(all_somas)
std_soma = math.sqrt(sum((s - media_soma)**2 for s in all_somas) / len(all_somas))
last_draw = set(results[6968])

def score_game(game):
    """Pontua um jogo com base em todos os critérios"""
    soma = sum(game)
    pares = sum(1 for n in game if n % 2 == 0)
    faixas = len(set((n-1)//10 for n in game))
    reps = len(set(game) & last_draw)
    primos_count = sum(1 for n in game if n in primes)
    terms = len(set(n % 10 for n in game))

    score = 0
    # Soma na faixa ideal
    if (media_soma - std_soma) <= soma <= (media_soma + std_soma):
        score += 25
    elif (media_soma - 1.5*std_soma) <= soma <= (media_soma + 1.5*std_soma):
        score += 10

    # Par/Ímpar equilibrado (3P/2I ou 2P/3I é melhor)
    if pares == 3:
        score += 25
    elif pares == 2:
        score += 20
    elif pares == 4:
        score += 10

    # Diversidade de faixas
    score += faixas * 5

    # Repetições do anterior (0-1 é bom)
    if reps <= 1:
        score += 15

    # Terminações diversas
    score += terms * 2

    # Score composto dos números
    for n in game:
        score += composite[n]['total'] * 0.3

    # Bônus por consenso de modelos
    for n in game:
        mc = model_count.get(n, 0)
        score += mc * 8

    # Bônus por ser número de sexta
    for n in game:
        if n in friday_freq:
            score += friday_freq[n] * 3

    return score

def validate_game(game):
    soma = sum(game)
    pares = sum(1 for n in game if n % 2 == 0)
    faixas = len(set((n-1)//10 for n in game))
    reps = len(set(game) & last_draw)
    terms = len(set(n % 10 for n in game))
    primos_count = sum(1 for n in game if n in primes)
    return {
        'soma': soma, 'pares': pares, 'impares': 5 - pares,
        'faixas': faixas, 'reps': reps, 'terms': terms,
        'primos': primos_count,
        'soma_ok': (media_soma - std_soma) <= soma <= (media_soma + std_soma),
        'pi_ok': 2 <= pares <= 4,
        'faixa_ok': faixas >= 3,
        'rep_ok': reps <= 1,
    }

# JOGO 1: Ultra-otimizado (busca exaustiva nos top 20 composite)
print("\n  Gerando jogos otimizados (busca combinatória)...")
top20_pool = [num for num, _ in ranked_composite[:20]]

best_games = []
for combo in combinations(top20_pool, 5):
    game = sorted(combo)
    v = validate_game(game)
    if v['pi_ok'] and v['soma_ok'] and v['faixa_ok'] and v['rep_ok']:
        s = score_game(game)
        best_games.append((game, s, v))

best_games.sort(key=lambda x: -x[1])

# JOGO EXTRA: Busca nos top 15 pesadas
top15_heavy_pool = [num for num, _ in ranked_heavy[:15]]
heavy_games = []
for combo in combinations(top15_heavy_pool, 5):
    game = sorted(combo)
    v = validate_game(game)
    if v['pi_ok'] and v['soma_ok'] and v['faixa_ok'] and v['rep_ok']:
        s = score_game(game)
        heavy_games.append((game, s, v))
heavy_games.sort(key=lambda x: -x[1])

# JOGO de sexta: números que mais saem às sextas
friday_pool = [num for num, _ in friday_freq.most_common(15)]
friday_games = []
for combo in combinations(friday_pool, 5):
    game = sorted(combo)
    v = validate_game(game)
    if v['pi_ok'] and v['soma_ok'] and v['faixa_ok'] and v['rep_ok']:
        s = score_game(game)
        friday_games.append((game, s, v))
friday_games.sort(key=lambda x: -x[1])

# JOGO consenso alto
high_consensus = sorted([n for n, c in model_count.items() if c >= 3],
                        key=lambda x: -composite[x]['total'])
consensus_games = []
if len(high_consensus) >= 5:
    for combo in combinations(high_consensus[:15], 5):
        game = sorted(combo)
        v = validate_game(game)
        if v['pi_ok'] and v['soma_ok'] and v['faixa_ok'] and v['rep_ok']:
            s = score_game(game)
            consensus_games.append((game, s, v))
    consensus_games.sort(key=lambda x: -x[1])

# JOGO devidos + quentes
due_nums = [x[0] for x in due_ranked if x[5] > 1.5][:8]
hot_nums = [num for num, _ in ranked_composite[:8]]
mixed_pool = list(set(due_nums + hot_nums))
mixed_games = []
for combo in combinations(mixed_pool[:15], 5):
    game = sorted(combo)
    v = validate_game(game)
    if v['pi_ok'] and v['soma_ok'] and v['faixa_ok'] and v['rep_ok']:
        s = score_game(game)
        mixed_games.append((game, s, v))
mixed_games.sort(key=lambda x: -x[1])

# Montar lista final
final_games = []

if best_games:
    final_games.append(("COMPOSITE OTIMIZADO", best_games[0]))
    # Pegar um segundo jogo diferente
    for g in best_games[1:]:
        overlap = len(set(g[0]) & set(best_games[0][0]))
        if overlap <= 2:
            final_games.append(("COMPOSITE ALTERNATIVO", g))
            break

if heavy_games:
    final_games.append(("BOLAS PESADAS", heavy_games[0]))

if friday_games:
    final_games.append(("ESPECIAL SEXTA", friday_games[0]))

if consensus_games:
    final_games.append(("CONSENSO MULTI-MODELO", consensus_games[0]))

if mixed_games:
    final_games.append(("DEVIDOS + QUENTES", mixed_games[0]))

# Garantir pelo menos 7 jogos únicos
all_used = set()
for name, (game, score, v) in final_games:
    all_used.add(tuple(game))

# Adicionar mais dos melhores
for g in best_games:
    if tuple(g[0]) not in all_used:
        final_games.append(("EXTRA OTIMIZADO", g))
        all_used.add(tuple(g[0]))
    if len(final_games) >= 10:
        break

print(f"""
  ╔═══════════════════════════════════════════════════════════════════════╗
  ║          JOGOS FINAIS - CONCURSO 6969 (06/03/2026 SEXTA)            ║
  ║          Prêmio estimado: R$ 13.500.000,00                          ║
  ╠═══════════════════════════════════════════════════════════════════════╣""")

for i, (name, (game, score, v)) in enumerate(final_games, 1):
    game_str = " - ".join(f"{n:02d}" for n in game)
    checks = sum([v['soma_ok'], v['pi_ok'], v['faixa_ok'], v['rep_ok']])
    check_str = "✓" * checks + "✗" * (4 - checks)

    # Contar consenso dos números
    consensus_total = sum(model_count.get(n, 0) for n in game)

    print(f"  ║                                                                     ║")
    print(f"  ║  {i:2d}. {name:<25}                                    ║")
    print(f"  ║      ┌──────────────────────────────────┐                            ║")
    print(f"  ║      │  {game_str:>34}  │                            ║")
    print(f"  ║      └──────────────────────────────────┘                            ║")
    print(f"  ║      Soma: {v['soma']:3d} | {v['pares']}P/{v['impares']}I | {v['faixas']} faixas | {v['terms']} terminações | Reps: {v['reps']}     ║")
    print(f"  ║      Score: {score:.0f} | Checks: [{check_str}] | Consenso: {consensus_total}/30      ║")
    print(f"  ╠═══════════════════════════════════════════════════════════════════════╣")

print(f"  ║                                                                     ║")
print(f"  ║  PARÂMETROS IDEAIS:                                                 ║")
print(f"  ║  • Soma: {media_soma-std_soma:.0f}-{media_soma+std_soma:.0f}  • Par/Ímpar: 3P/2I  • Faixas: ≥4           ║")
print(f"  ║  • Repetições anterior: 0-1  • Terminações: ≥4 diferentes          ║")
print(f"  ╚═══════════════════════════════════════════════════════════════════════╝")

# =====================================================================
# CONSENSO FINAL E RECOMENDAÇÃO
# =====================================================================
print("\n" + "=" * 75)
print("  RECOMENDAÇÃO FINAL")
print("=" * 75)

ultra_consensus = sorted([n for n, c in model_count.items() if c >= 4])
high_consensus_nums = sorted([n for n, c in model_count.items() if c == 3])

print(f"""
  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  NÚMEROS ULTRA-CONFIANÇA (4+ de 6 modelos):                        │
  │  → {ultra_consensus}
  │                                                                     │
  │  NÚMEROS ALTA CONFIANÇA (3 de 6 modelos):                          │
  │  → {high_consensus_nums}
  │                                                                     │""")

if final_games:
    top_game = final_games[0][1][0]
    print(f"  │  ★ JOGO PRINCIPAL RECOMENDADO:                                     │")
    print(f"  │  → {' - '.join(f'{n:02d}' for n in top_game):>40}               │")

print(f"""  │                                                                     │
  │  INSIGHTS EXCLUSIVOS DESTA ANÁLISE:                                │
  │  • O último sorteio teve 5P/0I (raro: 2%) → forte correção         │
  │    esperada para mais ÍMPARES no próximo                           │
  │  • Padrão de sexta-feira favorece números específicos              │
  │  • O número 26 está em sequência quente (3x nos últimos 5)        │
  │  • A trinca (26, 68, 74) saiu 2x juntas nos 59 concursos          │
  │  • Faixa 01-10 está superaquecida (16% vs 12.5% esperado)         │
  │  • 71% dos sorteios têm 0 repetição do anterior                    │
  │  • 80% dos sorteios NÃO têm números consecutivos                  │
  │                                                                     │
  │  DIFERENÇA PESO IGUAL vs BOLAS PESADAS:                            │
  │  • Peso igual: números ATRASADOS ganham importância                │
  │    (regressão à média → "devidos")                                  │
  │  • Bolas pesadas: números RECENTES dominam                         │
  │    (momentum → quem sai continua saindo)                           │
  │  • A verdade provavelmente está NO MEIO → score composto          │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
""")

print("=" * 75)
print("  AVISO: Loteria é jogo de AZAR. Cada sorteio é INDEPENDENTE.")
print("  Esta análise é estatística/simulação. Jogue com responsabilidade.")
print("  BOA SORTE NO CONCURSO 6969!")
print("=" * 75)
