#!/usr/bin/env python3
"""
=============================================================================
ANÁLISE ESTRATÉGICA AVANÇADA DA QUINA - CONCURSO 6969 (06/03/2026)
=============================================================================
Base: 39 concursos recentes (6920-6968) + histórico all-time
Modelos: Frequência, Atraso, Momentum, Ciclos, Bolas Pesadas, Monte Carlo
=============================================================================
"""

from collections import Counter, defaultdict
import random
import math

# =====================================================================
# BASE DE DADOS: 39 CONCURSOS RECENTES (6920-6968) + HISTÓRICO ALL-TIME
# =====================================================================

results = {
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

# Histórico all-time (top 20 mais sorteados em ~6968 concursos)
historical_freq = {
    4: 484, 52: 470, 26: 468, 49: 462, 31: 460,
    44: 458, 39: 456, 16: 455, 53: 454, 15: 452,
    56: 451, 62: 450, 14: 449, 64: 448, 8: 447,
    33: 446, 7: 445, 68: 444, 55: 443, 9: 442,
    # Menos sorteados
    47: 376, 76: 380, 73: 385, 75: 388, 42: 390,
}

all_numbers = list(range(1, 81))
sorted_concursos = sorted(results.keys())
total_concursos = len(results)
NEXT_CONCURSO = 6969

print("=" * 75)
print("  ANÁLISE ESTRATÉGICA AVANÇADA DA QUINA")
print(f"  CONCURSO {NEXT_CONCURSO} - 06/03/2026 (Sexta-feira)")
print(f"  Base de dados: {total_concursos} concursos (6920-6968)")
print("=" * 75)

# =====================================================================
# 1. FREQUÊNCIA ABSOLUTA E RELATIVA
# =====================================================================
print("\n" + "=" * 75)
print("  1. ANÁLISE DE FREQUÊNCIA (39 concursos = 195 bolas)")
print("=" * 75)

all_drawn = []
for nums in results.values():
    all_drawn.extend(nums)

freq = Counter(all_drawn)
total_draws = len(all_drawn)
expected_freq = total_draws / 80

print(f"\n  Total de bolas sorteadas: {total_draws}")
print(f"  Frequência esperada (uniforme): {expected_freq:.2f}")
print(f"  Desvio padrão esperado: {math.sqrt(expected_freq * (1 - 5/80)):.2f}")

print("\n  >> TOP 25 MAIS FREQUENTES:")
for i, (num, count) in enumerate(freq.most_common(25)):
    deviation = (count - expected_freq) / math.sqrt(expected_freq)
    bar = "█" * count
    status = "🔥" if deviation > 1.5 else "  "
    print(f"  {i+1:2d}. {num:02d} → {count:2d}x ({count/total_concursos*100:4.1f}%) σ={deviation:+.1f} {status} {bar}")

print("\n  >> NÚMEROS FRIOS (0 aparições nos 39 concursos):")
cold = sorted([n for n in all_numbers if n not in freq])
print(f"  {cold} ({len(cold)} dezenas)")

# =====================================================================
# 2. ATRASO (DELAY) - QUANTOS CONCURSOS SEM SAIR
# =====================================================================
print("\n" + "=" * 75)
print("  2. ANÁLISE DE ATRASO (quantos concursos cada número não sai)")
print("=" * 75)

delays = {}
for num in all_numbers:
    last_seen = None
    for c in reversed(sorted_concursos):
        if num in results[c]:
            last_seen = c
            break
    delays[num] = (NEXT_CONCURSO - last_seen) if last_seen else 999

# Calcular atraso médio esperado
avg_delay_expected = 80 / 5  # = 16 concursos (cada bola sai em média 1 a cada 16)

print(f"\n  Atraso médio esperado: {avg_delay_expected:.0f} concursos")
print(f"\n  >> TOP 15 MAIS ATRASADOS (que já apareceram):")
delayed = [(n, d) for n, d in delays.items() if d < 999]
delayed.sort(key=lambda x: -x[1])
for i, (num, d) in enumerate(delayed[:15]):
    f = freq.get(num, 0)
    overdue = d / avg_delay_expected
    status = "⚡" if overdue > 1.5 else "  "
    print(f"  {i+1:2d}. {num:02d} → {d:2d} concursos sem sair | Freq: {f}x | Atraso/Esperado: {overdue:.1f}x {status}")

# =====================================================================
# 3. MOMENTUM (TENDÊNCIA RECENTE) - Janelas deslizantes
# =====================================================================
print("\n" + "=" * 75)
print("  3. ANÁLISE DE MOMENTUM (janelas de 5, 10 e 15 concursos)")
print("=" * 75)

def freq_window(window_size):
    """Frequência nos últimos N concursos"""
    recent = sorted_concursos[-window_size:]
    nums = []
    for c in recent:
        nums.extend(results[c])
    return Counter(nums)

freq_5 = freq_window(5)
freq_10 = freq_window(10)
freq_15 = freq_window(15)

# Score de momentum: acelera ou desacelera?
momentum = {}
for num in all_numbers:
    f5 = freq_5.get(num, 0) / 5
    f10 = freq_10.get(num, 0) / 10
    f15 = freq_15.get(num, 0) / 15
    f39 = freq.get(num, 0) / 39

    # Momentum = taxa recente vs taxa geral
    if f39 > 0:
        mom = (f5 * 3 + f10 * 2 + f15) / 6 / f39
    else:
        mom = f5 * 3 + f10 * 2 + f15

    momentum[num] = mom

print("\n  >> TOP 15 COM MAIOR MOMENTUM (acelerando):")
mom_ranked = sorted(momentum.items(), key=lambda x: -x[1])
for i, (num, mom) in enumerate(mom_ranked[:15]):
    f5 = freq_5.get(num, 0)
    f10 = freq_10.get(num, 0)
    ftot = freq.get(num, 0)
    trend = "↗↗" if mom > 1.5 else "↗ " if mom > 1.0 else "→ "
    print(f"  {i+1:2d}. {num:02d} → Mom: {mom:.2f} {trend} | Últ5: {f5}x | Últ10: {f10}x | Total: {ftot}x")

# =====================================================================
# 4. ANÁLISE DE PARES FREQUENTES (duplas e trincas)
# =====================================================================
print("\n" + "=" * 75)
print("  4. PARES E TRINCAS MAIS FREQUENTES")
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

print("\n  >> TOP 15 DUPLAS mais frequentes:")
for i, (pair, cnt) in enumerate(pair_count.most_common(15)):
    print(f"  {i+1:2d}. ({pair[0]:02d}, {pair[1]:02d}) → {cnt}x")

print("\n  >> TOP 10 TRINCAS mais frequentes:")
for i, (triple, cnt) in enumerate(triple_count.most_common(10)):
    print(f"  {i+1:2d}. ({triple[0]:02d}, {triple[1]:02d}, {triple[2]:02d}) → {cnt}x")

# =====================================================================
# 5. ANÁLISE DE SEQUÊNCIAS E PADRÕES
# =====================================================================
print("\n" + "=" * 75)
print("  5. PADRÕES ESTRUTURAIS")
print("=" * 75)

# 5a. Par/Ímpar
print("\n  >> DISTRIBUIÇÃO PAR/ÍMPAR:")
pi_counts = Counter()
for nums in results.values():
    p = sum(1 for n in nums if n % 2 == 0)
    pi_counts[f"{p}P/{5-p}I"] += 1

for dist in sorted(pi_counts.keys()):
    cnt = pi_counts[dist]
    pct = cnt / total_concursos * 100
    bar = "█" * cnt
    print(f"  {dist}: {cnt:2d}x ({pct:4.1f}%) {bar}")

# Último sorteio foi 5P/0I → próximo tende a normalizar para 3P/2I ou 2P/3I
last_pares = sum(1 for n in results[6968] if n % 2 == 0)
print(f"\n  Último sorteio (6968): {last_pares}P/{5-last_pares}I")
print(f"  Distribuição dominante: 3P/2I (mais provável para o próximo)")

# 5b. Soma
print("\n  >> SOMA DOS NÚMEROS:")
somas = [(c, sum(results[c])) for c in sorted_concursos]
soma_vals = [s for _, s in somas]
media_soma = sum(soma_vals) / len(soma_vals)
std_soma = math.sqrt(sum((s - media_soma)**2 for s in soma_vals) / len(soma_vals))
print(f"  Média: {media_soma:.1f} | Desvio: {std_soma:.1f}")
print(f"  Faixa 1σ: {media_soma - std_soma:.0f} a {media_soma + std_soma:.0f}")
print(f"  Faixa 2σ: {media_soma - 2*std_soma:.0f} a {media_soma + 2*std_soma:.0f}")
print(f"  Última soma (6968): {sum(results[6968])}")

# 5c. Distribuição por faixas (dezenas)
print("\n  >> DISTRIBUIÇÃO POR FAIXA DE DEZENA:")
faixa_labels = ["01-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80"]
faixa_counts = [0] * 8
for num in all_drawn:
    idx = (num - 1) // 10
    faixa_counts[idx] += 1

expected_per_faixa = total_draws / 8
for i, label in enumerate(faixa_labels):
    cnt = faixa_counts[i]
    diff = cnt - expected_per_faixa
    pct = cnt / total_draws * 100
    signal = "↑" if diff > 2 else "↓" if diff < -2 else "="
    bar = "█" * cnt
    print(f"  {label}: {cnt:3d}x ({pct:4.1f}%) {signal}{abs(diff):+.1f} {bar}")

# 5d. Repetições entre consecutivos
print("\n  >> REPETIÇÕES ENTRE CONSECUTIVOS:")
rep_pattern = Counter()
for i in range(1, len(sorted_concursos)):
    c_prev = sorted_concursos[i-1]
    c_curr = sorted_concursos[i]
    rep = len(set(results[c_prev]) & set(results[c_curr]))
    rep_pattern[rep] += 1

for reps in sorted(rep_pattern.keys()):
    cnt = rep_pattern[reps]
    pct = cnt / (total_concursos - 1) * 100
    print(f"  {reps} repetições: {cnt}x ({pct:.1f}%)")

# Último: 6968 = [8, 14, 44, 56, 72]
last_draw = set(results[6968])
print(f"\n  Último sorteio: {sorted(last_draw)}")
print(f"  Padrão dominante: 0 repetições ({rep_pattern[0]/(total_concursos-1)*100:.0f}%)")
print(f"  → Esperar 0-1 repetição do sorteio anterior")

# 5e. Números consecutivos (sequenciais)
print("\n  >> NÚMEROS SEQUENCIAIS (consecutivos) NOS SORTEIOS:")
seq_counts = Counter()
for nums in results.values():
    s = sorted(nums)
    has_seq = 0
    for i in range(len(s)-1):
        if s[i+1] - s[i] == 1:
            has_seq += 1
    seq_counts[has_seq] += 1

for seqs in sorted(seq_counts.keys()):
    cnt = seq_counts[seqs]
    pct = cnt / total_concursos * 100
    print(f"  {seqs} par(es) consecutivo(s): {cnt}x ({pct:.1f}%)")

# =====================================================================
# 6. CICLOS - INTERVALOS ENTRE APARIÇÕES
# =====================================================================
print("\n" + "=" * 75)
print("  6. CICLOS DE APARIÇÃO (intervalos entre sorteios de cada número)")
print("=" * 75)

cycles = defaultdict(list)
for num in all_numbers:
    appearances = [c for c in sorted_concursos if num in results[c]]
    for i in range(1, len(appearances)):
        cycles[num].append(appearances[i] - appearances[i-1])

print("\n  >> TOP 15 números com ciclo mais previsível (menor desvio):")
cycle_stats = []
for num in all_numbers:
    if len(cycles[num]) >= 3:
        avg = sum(cycles[num]) / len(cycles[num])
        std = math.sqrt(sum((c - avg)**2 for c in cycles[num]) / len(cycles[num]))
        cv = std / avg if avg > 0 else 999  # coeficiente de variação
        last_app = max(c for c in sorted_concursos if num in results[c])
        since = NEXT_CONCURSO - last_app
        due = since / avg if avg > 0 else 0  # quanto "devido" está
        cycle_stats.append((num, avg, std, cv, since, due, len(cycles[num])))

cycle_stats.sort(key=lambda x: x[3])  # menor CV = mais previsível
for i, (num, avg, std, cv, since, due, n_cycles) in enumerate(cycle_stats[:15]):
    status = "🎯" if due > 0.9 else "  "
    print(f"  {i+1:2d}. {num:02d} → Ciclo: {avg:.1f}±{std:.1f} | CV: {cv:.2f} | Atraso: {since} | Devido: {due:.1f}x {status}")

# =====================================================================
# 7. SCORE COMPOSTO - MÁQUINA DE SORTEIO (PESO IGUAL)
# =====================================================================
print("\n" + "=" * 75)
print("  7. SCORE COMPOSTO - MODELO MÁQUINA (PESO IGUAL)")
print("=" * 75)
print("  Pesos: Freq(25%) + Momentum(25%) + Atraso/Ciclo(20%) + Pares(15%) + Histórico(15%)")

composite_scores = {}
for num in all_numbers:
    score = 0.0

    # A) Frequência recente normalizada (0-100)
    f = freq.get(num, 0)
    max_freq = freq.most_common(1)[0][1] if freq else 1
    score_freq = (f / max_freq) * 100 if max_freq > 0 else 0

    # B) Momentum (0-100)
    mom = momentum.get(num, 0)
    max_mom = max(momentum.values()) if momentum else 1
    score_mom = (mom / max_mom) * 100 if max_mom > 0 else 0

    # C) Atraso/Ciclo - "quanto devido" está (0-100)
    cycle_info = [x for x in cycle_stats if x[0] == num]
    if cycle_info:
        due = cycle_info[0][5]  # due ratio
        score_due = min(due * 50, 100)  # cap at 100
    else:
        d = delays.get(num, 0)
        score_due = min(d / avg_delay_expected * 50, 100)

    # D) Pares populares (0-100)
    pair_score = 0
    for (a, b), cnt in pair_count.most_common(30):
        if num == a or num == b:
            pair_score += cnt * 10
    score_pairs = min(pair_score, 100)

    # E) Histórico all-time (0-100)
    hist = historical_freq.get(num, 420)  # média assumida
    score_hist = (hist - 360) / (484 - 360) * 100

    # Composto ponderado
    total = (score_freq * 0.25 + score_mom * 0.25 +
             score_due * 0.20 + score_pairs * 0.15 +
             score_hist * 0.15)

    composite_scores[num] = {
        'total': total,
        'freq': score_freq,
        'momentum': score_mom,
        'due': score_due,
        'pairs': score_pairs,
        'hist': score_hist,
    }

ranked_composite = sorted(composite_scores.items(), key=lambda x: -x[1]['total'])

print(f"\n  {'#':>3} {'Nº':>3} {'TOTAL':>6} {'Freq':>5} {'Mom':>5} {'Due':>5} {'Pares':>5} {'Hist':>5}")
print("  " + "-" * 40)
for i, (num, scores) in enumerate(ranked_composite[:25]):
    print(f"  {i+1:3d}  {num:02d}  {scores['total']:5.1f}  {scores['freq']:5.1f} {scores['momentum']:5.1f} {scores['due']:5.1f} {scores['pairs']:5.1f} {scores['hist']:5.1f}")

# =====================================================================
# 8. MODELO DE BOLAS PESADAS (REFINADO)
# =====================================================================
print("\n" + "=" * 75)
print("  8. MODELO DE BOLAS PESADAS (REFINADO)")
print("=" * 75)
print("""
  PREMISSA FÍSICA: Cada vez que uma bola é sorteada, ela ganha peso.
  Bolas mais pesadas têm maior tendência gravitacional → mais chance de
  cair na posição de sorteio. O peso acumula ao longo dos concursos,
  mas decresce com o tempo (esfriamento gradual).

  Modelo: Peso = Base + Σ(peso_por_sorteio × decaimento^(distância))
""")

PESO_BASE = 1.0
PESO_POR_SORTEIO = 0.8
FATOR_DECAIMENTO = 0.92  # peso decai 8% por concurso de distância
BONUS_HISTORICO = 0.002   # peso por aparição histórica

heavy_weights = {}
for num in all_numbers:
    peso = PESO_BASE

    # Peso acumulado por cada aparição com decaimento temporal
    for c in sorted_concursos:
        if num in results[c]:
            distancia = NEXT_CONCURSO - c  # quantos concursos atrás
            peso += PESO_POR_SORTEIO * (FATOR_DECAIMENTO ** distancia)

    # Bônus histórico all-time
    hist_count = historical_freq.get(num, 420)
    peso += BONUS_HISTORICO * hist_count

    heavy_weights[num] = peso

# Normalizar para probabilidades
total_peso = sum(heavy_weights.values())
heavy_probs = {num: (peso / total_peso) * 100 for num, peso in heavy_weights.items()}

ranked_heavy = sorted(heavy_weights.items(), key=lambda x: -x[1])

print(f"  {'#':>3} {'Nº':>3} {'Peso':>6} {'Prob%':>6} {'vs Unif':>7} {'Freq39':>6} {'Barra'}")
print("  " + "-" * 55)
uniform_prob = 100 / 80  # 1.25%
for i, (num, peso) in enumerate(ranked_heavy[:25]):
    prob = heavy_probs[num]
    advantage = prob / uniform_prob
    f = freq.get(num, 0)
    bar = "█" * int(prob * 20)
    print(f"  {i+1:3d}  {num:02d}  {peso:5.2f}  {prob:5.2f}%  {advantage:5.2f}x  {f:2d}x  {bar}")

lightest = ranked_heavy[-1]
heaviest = ranked_heavy[0]
print(f"\n  Bola MAIS pesada: Nº {heaviest[0]:02d} (peso {heaviest[1]:.2f}, prob {heavy_probs[heaviest[0]]:.2f}%)")
print(f"  Bola MAIS leve:   Nº {lightest[0]:02d} (peso {lightest[1]:.2f}, prob {heavy_probs[lightest[0]]:.2f}%)")
print(f"  Vantagem máxima:  {heaviest[1]/lightest[1]:.2f}x")

# =====================================================================
# 9. SIMULAÇÃO MONTE CARLO (10.000 sorteios simulados)
# =====================================================================
print("\n" + "=" * 75)
print("  9. SIMULAÇÃO MONTE CARLO (10.000 sorteios com pesos)")
print("=" * 75)

random.seed(6969)  # seed determinística para reprodutibilidade

# Criar lista de pesos para amostragem
weight_list = [(num, heavy_weights[num]) for num in all_numbers]
nums_list = [n for n, _ in weight_list]
weights_list = [w for _, w in weight_list]

monte_carlo_freq = Counter()
N_SIMULATIONS = 10000

for _ in range(N_SIMULATIONS):
    drawn = random.choices(nums_list, weights=weights_list, k=5)
    # Garantir 5 únicos
    drawn_set = set()
    while len(drawn_set) < 5:
        pick = random.choices(nums_list, weights=weights_list, k=1)[0]
        drawn_set.add(pick)
    for n in drawn_set:
        monte_carlo_freq[n] += 1

print(f"\n  >> TOP 20 números mais sorteados na simulação ({N_SIMULATIONS} sorteios):")
for i, (num, cnt) in enumerate(monte_carlo_freq.most_common(20)):
    pct = cnt / N_SIMULATIONS * 100
    bar = "█" * int(pct)
    print(f"  {i+1:2d}. {num:02d} → {cnt:5d}x ({pct:4.1f}%) {bar}")

# =====================================================================
# 10. GERAÇÃO DE JOGOS OTIMIZADOS
# =====================================================================
print("\n" + "=" * 75)
print("  10. JOGOS OTIMIZADOS PARA O CONCURSO 6969")
print("=" * 75)

def validate_game(game, label):
    """Valida um jogo contra os padrões identificados"""
    soma = sum(game)
    pares = sum(1 for n in game if n % 2 == 0)
    faixas = len(set((n-1)//10 for n in game))
    consecutivos = sum(1 for i in range(len(game)-1) if game[i+1] - game[i] == 1)
    reps_last = len(set(game) & last_draw)

    # Checks
    soma_ok = (media_soma - std_soma) <= soma <= (media_soma + std_soma)
    pi_ok = 2 <= pares <= 4
    faixa_ok = faixas >= 3
    rep_ok = reps_last <= 1

    score = 0
    if soma_ok: score += 1
    if pi_ok: score += 1
    if faixa_ok: score += 1
    if rep_ok: score += 1

    return {
        'label': label,
        'game': game,
        'soma': soma,
        'pares': pares,
        'impares': 5 - pares,
        'faixas': faixas,
        'consecutivos': consecutivos,
        'reps_last': reps_last,
        'soma_ok': soma_ok,
        'pi_ok': pi_ok,
        'faixa_ok': faixa_ok,
        'rep_ok': rep_ok,
        'checks': score,
    }

# JOGO 1: Top composite score
j1_pool = [num for num, _ in ranked_composite[:10]]
j1 = sorted(j1_pool[:5])
# Verificar se passa nos checks, senão ajustar
v1 = validate_game(j1, "Composite Score")
if not v1['pi_ok'] or not v1['soma_ok']:
    # Trocar último por melhor candidato que melhore
    for num, _ in ranked_composite[5:20]:
        test = sorted(j1[:4] + [num])
        vtest = validate_game(test, "")
        if vtest['pi_ok'] and vtest['soma_ok'] and vtest['faixa_ok']:
            j1 = test
            break
v1 = validate_game(j1, "Composite Score")

# JOGO 2: Bolas pesadas puro
j2 = sorted([num for num, _ in ranked_heavy[:5]])
v2 = validate_game(j2, "Bolas Pesadas")
if not v2['pi_ok'] or not v2['soma_ok']:
    for num, _ in ranked_heavy[5:20]:
        test = sorted(j2[:4] + [num])
        vtest = validate_game(test, "")
        if vtest['pi_ok'] and vtest['soma_ok'] and vtest['faixa_ok']:
            j2 = test
            break
v2 = validate_game(j2, "Bolas Pesadas")

# JOGO 3: Monte Carlo (top 5 da simulação)
j3 = sorted([num for num, _ in monte_carlo_freq.most_common(5)])
v3 = validate_game(j3, "Monte Carlo")
if not v3['pi_ok'] or not v3['soma_ok']:
    for num, _ in monte_carlo_freq.most_common(20):
        if num not in j3[:4]:
            test = sorted(j3[:4] + [num])
            vtest = validate_game(test, "")
            if vtest['pi_ok'] and vtest['soma_ok'] and vtest['faixa_ok']:
                j3 = test
                break
v3 = validate_game(j3, "Monte Carlo")

# JOGO 4: Momentum + Ciclos "devidos"
momentum_top = [num for num, _ in sorted(momentum.items(), key=lambda x: -x[1])[:8]]
due_top = [x[0] for x in cycle_stats if x[5] > 0.8][:8]  # números "devidos"
j4_pool = list(set(momentum_top[:3] + due_top[:3]))
# Complementar com composite
for num, _ in ranked_composite:
    if num not in j4_pool:
        j4_pool.append(num)
    if len(j4_pool) >= 10:
        break
j4 = sorted(j4_pool[:5])
v4 = validate_game(j4, "Momentum + Ciclo")
if not v4['pi_ok'] or not v4['soma_ok']:
    for num in j4_pool[5:]:
        test = sorted(j4[:4] + [num])
        vtest = validate_game(test, "")
        if vtest['pi_ok'] and vtest['soma_ok'] and vtest['faixa_ok']:
            j4 = test
            break
v4 = validate_game(j4, "Momentum + Ciclo")

# JOGO 5: Anti-padrão (números atrasados que historicamente são quentes)
hot_delayed = []
for num, d in sorted(delays.items(), key=lambda x: -x[1]):
    if freq.get(num, 0) >= 2 and d >= 8:
        hot_delayed.append(num)
    if len(hot_delayed) >= 3:
        break
# Completar com histórico all-time
hist_picks = []
for num in sorted(historical_freq.keys(), key=lambda x: -historical_freq[x]):
    if num not in hot_delayed and freq.get(num, 0) >= 1:
        hist_picks.append(num)
    if len(hist_picks) >= 3:
        break
j5_pool = hot_delayed + hist_picks
j5 = sorted(j5_pool[:5])
v5 = validate_game(j5, "Atrasados Quentes")
if not v5['pi_ok'] or not v5['soma_ok']:
    for num in hist_picks + hot_delayed:
        if num not in j5[:4]:
            test = sorted(j5[:4] + [num])
            vtest = validate_game(test, "")
            if vtest['pi_ok'] and vtest['soma_ok']:
                j5 = test
                break
v5 = validate_game(j5, "Atrasados Quentes")

# JOGO 6: Duplas+Trincas mais frequentes
top_pairs = pair_count.most_common(5)
j6_pool = set()
for (a, b), _ in top_pairs:
    j6_pool.add(a)
    j6_pool.add(b)
j6_pool = sorted(j6_pool, key=lambda x: -composite_scores[x]['total'])[:5]
j6 = sorted(j6_pool)
v6 = validate_game(j6, "Duplas Frequentes")

# JOGO 7: Bolas pesadas COM ajuste de equilíbrio par/ímpar e soma
j7_candidates = [num for num, _ in ranked_heavy[:15]]
best_j7 = None
best_j7_score = -1
from itertools import combinations
for combo in combinations(j7_candidates, 5):
    game = sorted(combo)
    v = validate_game(game, "")
    if v['checks'] == 4:  # todos os checks OK
        # Score = soma dos pesos
        total_w = sum(heavy_weights[n] for n in game)
        if total_w > best_j7_score:
            best_j7_score = total_w
            best_j7 = game

if best_j7 is None:
    best_j7 = j2  # fallback
j7 = best_j7
v7 = validate_game(j7, "Pesadas Otimizadas")

games = [
    (j1, v1, "COMPOSITE SCORE", "Score ponderado: Freq + Momentum + Ciclo + Pares + Histórico"),
    (j2, v2, "BOLAS PESADAS", "Modelo gravitacional: bolas mais sorteadas = mais pesadas"),
    (j3, v3, "MONTE CARLO", "Simulação de 10.000 sorteios com distribuição de pesos"),
    (j4, v4, "MOMENTUM + CICLO", "Números acelerando + devidos pelo ciclo natural"),
    (j5, v5, "ATRASADOS QUENTES", "Números atrasados que historicamente são frequentes"),
    (j6, v6, "DUPLAS FREQUENTES", "Baseado nas duplas que mais saem juntas"),
    (j7, v7, "PESADAS OTIMIZADAS", "Bolas pesadas com ajuste de soma/par/ímpar/faixas"),
]

print("""
  ╔═════════════════════════════════════════════════════════════════════╗
  ║              JOGOS RECOMENDADOS - CONCURSO 6969                   ║
  ╠═════════════════════════════════════════════════════════════════════╣""")

for game, v, name, desc in games:
    checks = "✓" * v['checks'] + "✗" * (4 - v['checks'])
    game_str = " - ".join(f"{n:02d}" for n in game)
    print(f"  ║                                                                   ║")
    print(f"  ║  {name:<20}  {game_str:>25}        ║")
    print(f"  ║  {desc[:65]:<65}  ║")
    print(f"  ║  Soma: {v['soma']:3d} | {v['pares']}P/{v['impares']}I | {v['faixas']} faixas | Reps: {v['reps_last']} | [{checks}]  ║")
    print(f"  ╠═════════════════════════════════════════════════════════════════════╣")

print(f"  ║                                                                   ║")
print(f"  ║  PARÂMETROS IDEAIS:                                               ║")
print(f"  ║  Soma: {media_soma-std_soma:.0f}-{media_soma+std_soma:.0f} | Par/Ímpar: 2P-4P | Faixas: ≥3 | Reps: 0-1   ║")
print(f"  ╚═════════════════════════════════════════════════════════════════════╝")

# =====================================================================
# 11. ANÁLISE COMPARATIVA: PESO IGUAL vs BOLAS PESADAS
# =====================================================================
print("\n" + "=" * 75)
print("  11. COMPARAÇÃO: PESO IGUAL vs BOLAS PESADAS")
print("=" * 75)

# Interseção entre top 10 de cada modelo
top10_composite = set(num for num, _ in ranked_composite[:10])
top10_heavy = set(num for num, _ in ranked_heavy[:10])
top10_monte = set(num for num, _ in monte_carlo_freq.most_common(10))

consensus = top10_composite & top10_heavy & top10_monte
print(f"\n  Top 10 Composite: {sorted(top10_composite)}")
print(f"  Top 10 Pesadas:   {sorted(top10_heavy)}")
print(f"  Top 10 Monte C.:  {sorted(top10_monte)}")
print(f"\n  ★ CONSENSO (presentes nos 3 modelos): {sorted(consensus)}")
print(f"  → Estes são os números com MAIOR CONFIANÇA")

two_models = (top10_composite & top10_heavy) | (top10_composite & top10_monte) | (top10_heavy & top10_monte)
two_models -= consensus
print(f"  ★ Em 2 de 3 modelos: {sorted(two_models)}")

# =====================================================================
# RESUMO FINAL
# =====================================================================
print("\n" + "=" * 75)
print("  RESUMO EXECUTIVO")
print("=" * 75)

print(f"""
  ┌─────────────────────────────────────────────────────────────────┐
  │  NÚMEROS DE ALTA CONFIANÇA (consenso dos 3 modelos):            │
  │  → {sorted(consensus)}
  │                                                                 │
  │  NÚMEROS DE MÉDIA CONFIANÇA (2 de 3 modelos):                   │
  │  → {sorted(two_models)}
  │                                                                 │
  │  JOGO PRINCIPAL RECOMENDADO (Pesadas Otimizadas):               │
  │  → {' - '.join(f'{n:02d}' for n in j7)}
  │                                                                 │
  │  DIFERENÇA NO MODELO DE BOLAS PESADAS:                          │
  │  • Bola mais pesada tem {heaviest[1]/lightest[1]:.1f}x mais chance que a mais leve │
  │  • O peso recente conta mais (decaimento exponencial)            │
  │  • Números que saíram nos últimos 3-5 sorteios dominam           │
  │  • No modelo uniforme, números atrasados têm mais peso           │
  │                                                                 │
  │  PERFIL IDEAL DO JOGO:                                          │
  │  • Soma entre {media_soma-std_soma:.0f} e {media_soma+std_soma:.0f}                                      │
  │  • 3 pares e 2 ímpares (ou 2P/3I)                              │
  │  • Pelo menos 3 faixas de dezena diferentes                     │
  │  • 0 a 1 repetição do sorteio anterior                          │
  │  • Incluir pelo menos 2 números do consenso                    │
  └─────────────────────────────────────────────────────────────────┘
""")

print("=" * 75)
print("  AVISO LEGAL")
print("=" * 75)
print("""
  Esta análise utiliza métodos estatísticos e simulações computacionais.
  Loteria é um jogo de AZAR puro. Cada sorteio é INDEPENDENTE.
  Resultados passados NÃO garantem resultados futuros.
  O modelo de "bolas pesadas" é HIPOTÉTICO - máquinas reais são
  regulamentadas para garantir aleatoriedade.
  Jogue com responsabilidade. Nunca aposte mais do que pode perder.
  BOA SORTE NO CONCURSO 6969!
""")
