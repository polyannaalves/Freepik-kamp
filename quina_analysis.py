#!/usr/bin/env python3
"""
Análise Estratégica da Quina - Concurso 6969 (06/03/2026)
Simulação como máquina de sorteio + modelo de bolas com peso
"""

from collections import Counter
import math

# Dados dos últimos 19 concursos (6950-6968)
results = {
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

# Números historicamente mais sorteados (all-time top)
historical_top = {4: 484, 26: 470, 53: 465, 39: 462, 31: 460, 52: 458, 49: 456}
historical_cold = {47: 360, 76: 365, 73: 368}

all_numbers = list(range(1, 81))
total_concursos = len(results)

print("=" * 70)
print("  ANÁLISE ESTRATÉGICA DA QUINA - CONCURSO 6969 (06/03/2026)")
print("  Prêmio estimado: R$ 13.500.000,00 (acumulado 9 sorteios)")
print("=" * 70)

# ===== ANÁLISE 1: FREQUÊNCIA NOS ÚLTIMOS 19 CONCURSOS =====
print("\n" + "=" * 70)
print("  PARTE 1: SIMULAÇÃO COMO MÁQUINA DE SORTEIO (PROBABILIDADE IGUAL)")
print("=" * 70)

all_drawn = []
for nums in results.values():
    all_drawn.extend(nums)

freq = Counter(all_drawn)
total_draws = len(all_drawn)  # 95 bolas sorteadas

print(f"\n--- Total de bolas sorteadas nos últimos {total_concursos} concursos: {total_draws} ---")
print(f"--- Frequência esperada por número (uniforme): {total_draws/80:.2f} ---")

# Top 15 mais frequentes
print("\n>> TOP 15 NÚMEROS MAIS FREQUENTES (últimos 19 concursos):")
for num, count in freq.most_common(15):
    bar = "█" * (count * 4)
    pct = count / total_concursos * 100
    print(f"  {num:02d} → {count}x ({pct:.0f}%) {bar}")

# Números que NÃO saíram
never = sorted([n for n in all_numbers if n not in freq])
print(f"\n>> NÚMEROS QUE NÃO SAÍRAM nos últimos 19 concursos ({len(never)} dezenas):")
print(f"  {never}")

# Atraso (delay) de cada número
print("\n>> ATRASO (concursos sem sair) - TOP 10 mais atrasados entre os que já saíram:")
delays = {}
sorted_concursos = sorted(results.keys())
for num in all_numbers:
    last_seen = None
    for c in reversed(sorted_concursos):
        if num in results[c]:
            last_seen = c
            break
    if last_seen:
        delays[num] = 6968 - last_seen
    else:
        delays[num] = 999  # never seen

delayed_seen = {k: v for k, v in delays.items() if v < 999}
for num, d in sorted(delayed_seen.items(), key=lambda x: -x[1])[:10]:
    print(f"  {num:02d} → {d} concursos sem sair (última vez: {6968 - d})")

# Análise de pares/ímpares
print("\n>> DISTRIBUIÇÃO PAR/ÍMPAR nos últimos 19 concursos:")
for c in sorted_concursos:
    nums = results[c]
    pares = sum(1 for n in nums if n % 2 == 0)
    impares = 5 - pares
    print(f"  {c}: {nums} → {pares}P/{impares}I")

par_counts = Counter()
for nums in results.values():
    p = sum(1 for n in nums if n % 2 == 0)
    par_counts[f"{p}P/{5-p}I"] += 1
print("\n  Resumo distribuição Par/Ímpar:")
for dist, cnt in sorted(par_counts.items(), key=lambda x: -x[1]):
    print(f"    {dist}: {cnt}x ({cnt/total_concursos*100:.0f}%)")

# Análise por faixas (dezenas)
print("\n>> DISTRIBUIÇÃO POR FAIXA:")
faixas = {"01-10": 0, "11-20": 0, "21-30": 0, "31-40": 0, "41-50": 0,
          "51-60": 0, "61-70": 0, "71-80": 0}
for num in all_drawn:
    idx = (num - 1) // 10
    keys = list(faixas.keys())
    faixas[keys[idx]] += 1

for faixa, cnt in faixas.items():
    bar = "█" * cnt
    expected = total_draws / 8
    diff = cnt - expected
    signal = "↑" if diff > 0 else "↓"
    print(f"  {faixa}: {cnt:2d}x ({cnt/total_draws*100:.1f}%) {signal}{abs(diff):.1f} {bar}")

# Soma dos números sorteados
print("\n>> SOMA DOS NÚMEROS SORTEADOS:")
somas = []
for c in sorted_concursos:
    s = sum(results[c])
    somas.append(s)
    print(f"  {c}: soma = {s}")
media_soma = sum(somas) / len(somas)
print(f"  Média das somas: {media_soma:.1f}")
print(f"  Faixa ideal para aposta: {media_soma-30:.0f} a {media_soma+30:.0f}")

# Repetições entre concursos consecutivos
print("\n>> REPETIÇÕES ENTRE CONCURSOS CONSECUTIVOS:")
for i in range(1, len(sorted_concursos)):
    c_prev = sorted_concursos[i-1]
    c_curr = sorted_concursos[i]
    rep = set(results[c_prev]) & set(results[c_curr])
    print(f"  {c_prev}→{c_curr}: {len(rep)} repetições {sorted(rep) if rep else '[]'}")

rep_counts = Counter()
for i in range(1, len(sorted_concursos)):
    c_prev = sorted_concursos[i-1]
    c_curr = sorted_concursos[i]
    rep = len(set(results[c_prev]) & set(results[c_curr]))
    rep_counts[rep] += 1
print(f"\n  Padrão de repetições: {dict(sorted(rep_counts.items()))}")

# ===== ESTRATÉGIA 1: Máquina de sorteio (peso igual) =====
print("\n" + "-" * 70)
print("  ESTRATÉGIA 1: SIMULAÇÃO MÁQUINA (TODAS AS BOLAS COM PESO IGUAL)")
print("-" * 70)

# Score baseado em múltiplos fatores
scores_equal = {}
for num in all_numbers:
    score = 0
    f = freq.get(num, 0)

    # Fator 1: Frequência recente (números quentes)
    score += f * 10

    # Fator 2: Atraso moderado (números "devidos" - regressão à média)
    delay = delays.get(num, 999)
    if 3 <= delay <= 8:
        score += 15  # atrasados moderados
    elif delay > 8 and f > 0:
        score += 8   # muito atrasados mas já apareceram

    # Fator 3: Apareceu nos últimos 5 concursos (momentum)
    last5 = sorted_concursos[-5:]
    for c in last5:
        if num in results[c]:
            score += 5

    # Fator 4: Histórico all-time
    if num in historical_top:
        score += 5

    scores_equal[num] = score

ranked_equal = sorted(scores_equal.items(), key=lambda x: -x[1])

print("\n  TOP 20 números com maior pontuação (peso igual):")
for i, (num, sc) in enumerate(ranked_equal[:20]):
    f = freq.get(num, 0)
    d = delays.get(num, 999)
    d_str = str(d) if d < 999 else "N/A"
    print(f"  {i+1:2d}. Nº {num:02d} | Score: {sc:3d} | Freq: {f}x | Atraso: {d_str}")

# Seleção final estratégia 1
top5_equal = [num for num, _ in ranked_equal[:5]]
soma_sel = sum(top5_equal)
pares_sel = sum(1 for n in top5_equal if n % 2 == 0)

print(f"\n  ★ SELEÇÃO ESTRATÉGIA 1 (peso igual): {sorted(top5_equal)}")
print(f"    Soma: {soma_sel} | Pares: {pares_sel} | Ímpares: {5-pares_sel}")

# ===== PARTE 2: BOLAS PESADAS =====
print("\n" + "=" * 70)
print("  PARTE 2: MODELO DE BOLAS PESADAS")
print("  (Bolas sorteadas têm peso extra → maior probabilidade de sair)")
print("=" * 70)

print("""
  PREMISSA: Se as bolas que já foram sorteadas ficam mais pesadas,
  elas tendem a cair mais no fundo do globo e ser selecionadas mais
  vezes. Quanto mais uma bola foi sorteada, mais pesada ela fica,
  e maior a probabilidade de ser sorteada novamente.
""")

# Modelo de peso: peso_base + (frequência * fator_peso)
PESO_BASE = 1.0
FATOR_PESO_FREQ = 0.5        # peso por cada vez sorteada
FATOR_PESO_RECENTE = 0.3     # bônus extra por sorteio recente
FATOR_PESO_HISTORICO = 0.1   # bônus por frequência histórica

scores_heavy = {}
for num in all_numbers:
    peso = PESO_BASE
    f = freq.get(num, 0)

    # Peso por frequência recente (19 concursos)
    peso += f * FATOR_PESO_FREQ

    # Peso extra por aparições nos últimos 5 concursos (mais recente = mais pesada)
    for idx, c in enumerate(sorted_concursos[-5:]):
        if num in results[c]:
            peso += FATOR_PESO_RECENTE * (idx + 1)  # mais recente = mais peso

    # Peso extra por aparições nos últimos 3 concursos
    for c in sorted_concursos[-3:]:
        if num in results[c]:
            peso += 0.4

    # Peso histórico all-time
    if num in historical_top:
        peso += FATOR_PESO_HISTORICO * (historical_top[num] / 100)

    scores_heavy[num] = peso

# Normalizar para probabilidades
total_peso = sum(scores_heavy.values())
probs = {num: peso / total_peso * 100 for num, peso in scores_heavy.items()}

ranked_heavy = sorted(scores_heavy.items(), key=lambda x: -x[1])

print("  TOP 20 números com maior PESO (modelo bolas pesadas):")
for i, (num, peso) in enumerate(ranked_heavy[:20]):
    f = freq.get(num, 0)
    prob = probs[num]
    bar = "█" * int(prob * 10)
    print(f"  {i+1:2d}. Nº {num:02d} | Peso: {peso:.2f} | Prob: {prob:.2f}% | Freq: {f}x {bar}")

# Comparar com bola mais leve
lightest = ranked_heavy[-1]
heaviest = ranked_heavy[0]
print(f"\n  Bola mais pesada: Nº {heaviest[0]:02d} (peso {heaviest[1]:.2f}, prob {probs[heaviest[0]]:.2f}%)")
print(f"  Bola mais leve:   Nº {lightest[0]:02d} (peso {lightest[1]:.2f}, prob {probs[lightest[0]]:.2f}%)")
print(f"  Razão pesada/leve: {heaviest[1]/lightest[1]:.1f}x mais chance")

# Seleção final estratégia 2
top5_heavy = [num for num, _ in ranked_heavy[:5]]
soma_sel2 = sum(top5_heavy)
pares_sel2 = sum(1 for n in top5_heavy if n % 2 == 0)

print(f"\n  ★ SELEÇÃO ESTRATÉGIA 2 (bolas pesadas): {sorted(top5_heavy)}")
print(f"    Soma: {soma_sel2} | Pares: {pares_sel2} | Ímpares: {5-pares_sel2}")

# ===== COMBINAÇÃO FINAL =====
print("\n" + "=" * 70)
print("  RESULTADO FINAL: JOGOS RECOMENDADOS PARA O CONCURSO 6969")
print("=" * 70)

# Jogo 1: Top 5 peso igual
j1 = sorted(top5_equal)
# Jogo 2: Top 5 bolas pesadas
j2 = sorted(top5_heavy)
# Jogo 3: Combinação (top 3 pesadas + top 2 atrasadas moderadas)
atrasados_mod = sorted(
    [(num, d) for num, d in delays.items() if 4 <= d <= 10 and freq.get(num, 0) >= 2],
    key=lambda x: -x[1]
)
top_atrasados = [num for num, _ in atrasados_mod[:2]]
top3_heavy = [num for num, _ in ranked_heavy[:3]]
j3 = sorted(set(top3_heavy + top_atrasados))[:5]

# Jogo 4: Equilibrado (mix quentes + frios + histórico)
quentes = [num for num, _ in ranked_heavy[:3]]
historicos = [n for n in [4, 53, 39] if n not in quentes][:1]
frios_recentes = sorted(
    [(num, d) for num, d in delays.items() if d >= 6 and freq.get(num, 0) >= 1],
    key=lambda x: -x[1]
)[:1]
j4_pool = quentes + historicos + [n for n, _ in frios_recentes]
j4 = sorted(set(j4_pool))[:5]

# Se j4 tem menos de 5, completar
while len(j4) < 5:
    for num, _ in ranked_heavy:
        if num not in j4:
            j4.append(num)
            break
j4 = sorted(j4)

# Jogo 5: Anti-padrão (números que estão "devidos" e fora do radar)
anti = []
for num, d in sorted(delays.items(), key=lambda x: -x[1]):
    if freq.get(num, 0) >= 2 and d >= 5 and len(anti) < 5:
        anti.append(num)
j5 = sorted(anti)

print(f"""
  ┌─────────────────────────────────────────────────────────────┐
  │  JOGO 1 (Máquina - Peso Igual):     {j1}       │
  │  Estratégia: Números mais frequentes nos últimos 19 sorteios│
  ├─────────────────────────────────────────────────────────────┤
  │  JOGO 2 (Bolas Pesadas):            {j2}       │
  │  Estratégia: Bolas com maior peso acumulado                 │
  ├─────────────────────────────────────────────────────────────┤
  │  JOGO 3 (Pesadas + Atrasadas):      {j3}       │
  │  Estratégia: Top pesadas + números moderadamente atrasados  │
  ├─────────────────────────────────────────────────────────────┤
  │  JOGO 4 (Equilibrado):              {j4}       │
  │  Estratégia: Mix quentes + histórico all-time + frios       │
  ├─────────────────────────────────────────────────────────────┤
  │  JOGO 5 (Anti-padrão):              {j5}       │
  │  Estratégia: Números "devidos" com histórico de aparição    │
  └─────────────────────────────────────────────────────────────┘
""")

# Validações
print("  VALIDAÇÕES:")
for i, jogo in enumerate([j1, j2, j3, j4, j5], 1):
    soma = sum(jogo)
    pares = sum(1 for n in jogo if n % 2 == 0)
    faixas_repr = len(set((n-1)//10 for n in jogo))
    print(f"  Jogo {i}: Soma={soma:3d} | {pares}P/{5-pares}I | {faixas_repr} faixas | {jogo}")

print(f"\n  Soma média ideal: ~{media_soma:.0f} (faixa {media_soma-30:.0f}-{media_soma+30:.0f})")

print("\n" + "=" * 70)
print("  AVISO IMPORTANTE")
print("=" * 70)
print("""
  Esta análise é baseada em estatística descritiva e simulação.
  Loteria é um jogo de AZAR - cada sorteio é independente.
  Números passados NÃO influenciam sorteios futuros em máquinas reais.
  O modelo de "bolas pesadas" é uma simulação hipotética que assume
  um viés mecânico inexistente em máquinas regulamentadas.
  Jogue com responsabilidade. Boa sorte!
""")
