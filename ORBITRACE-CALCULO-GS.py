# ============================================================
# Projeto : Orbitrace - Modelagem Matemática
# Disciplina: Differentiated Problem Solving
# Global Solution 2026 - 1° Semestre
# Curso: Engenharia de Software - TURMA 1ESPU
#
# Integrantes:
#   Pedro Passos Corsini           - RM: 573493
#   Pedro Thyago Araujo dos Santos - RM: 570939
#   Daniel Gomes Torres            - RM: 573436
#   Henrique Lira                  - RM: 571009
# ============================================================

import math
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ============================================================
# CONSTANTES FISICAS
# ============================================================
MU    = 398600.4418   # parametro gravitacional da Terra (km^3/s^2)
R_T   = 6371.0        # raio medio da Terra (km)
PI    = math.pi       # valor de pi (utilizando math)
LMBD  = 0.5           # lambda da curva de risco (km)

# Satélites brasileiros
SATELITES = [
    {"nome": "CBERS-4A",   "altitude": 628.0},
    {"nome": "AMAZONIA-1", "altitude": 752.0},
    {"nome": "SCD-2",      "altitude": 750.0},
]


# ============================================================
# FUNCOES UTILITÁRIAS
# ============================================================

def limpar():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def pausar():
    input("\nPressione Enter para voltar ao menu...")

def linha(char="-", size=55):
    print(char * size)


# ============================================================
# FUNCOES MATEMATICAS
# ============================================================

def periodo_orbital(h):
    """
    3° Lei de Kepler - período em minutos.
    T(h) = 2 * pi * sqrt( (R_T + h)^3 / mu )
    Tipo: funcão de potência (expoente 3/2).
    Crescimento: estritamente CRESCENTE.
    """
    a = R_T + h
    T_segundos = 2 * PI * math.sqrt(a**3 / MU)
    return T_segundos / 60   # converte para minutos


def velocidade_orbital(h):
    """
    Velocidade circular em km/s.
    v(h) = sqrt( mu / (R_T + h) )
    Tipo: função de potência (expoente -1/2).
    Crescimento: estritamente DECRESCENTE.
    """
    a = R_T + h
    return math.sqrt(MU / a)


def prob_colisao(d):
    """
    Probabilidade de colisão pelo modelo exponencial.
    P(d) = e ^ (-d / lambda)
    Tipo: função EXPONENCIAL DECRESCENTE.
    P(0) = 1.0  (certeza de colisão a distância zero)
    P -> 0 conforme d aumenta.
    """
    return math.exp(-d / LMBD)


def gravidade(h):
    """
    Aceleração gravitacional em m/s^2.
    g(h) = mu / (R_T + h)^2   [resultado em km/s^2, convertido para m/s^2]
    Tipo: funcao RACIONAL - lei do inverso do quadrado.
    Crescimento: estritamente DECRESCENTE.
    """
    a = R_T + h
    g_km = MU / (a ** 2)
    return g_km * 1000   # converte km/s^2 -> m/s^2


def classificar_risco(d):
    """
    Classifica o nivel de risco com base na distância minima.
    """
    if d < 0.2:
        return "CRITICO"
    elif d < 0.5:
        return "ALTO"
    elif d < 1.0:
        return "MEDIO"
    else:
        return "BAIXO"


# ============================================================
# TELAS DO MENU
# ============================================================

def tela_sobre():
    limpar()
    linha("=")
    print("  SOBRE O PROJETO - ORBITRACE")
    linha("=")
    print()
    print("  O Orbitrace monitora detritos espaciais e calcula")
    print("  riscos de colisão para satélites brasileiros em LEO.")
    print("  Usa a 3° Lei de Kepler, modelo exponencial de risco,")
    print("  lei de Newton, numpy e matplotlib. (ODS 9)")
    print("  Solução para a GS - FIAP.")
    print()
    linha("=")
    pausar()


def tela_periodo_velocidade():
    """
    Função 1 e 2: exibe período orbital e velocidade dos 3 satélites.
    Permite também calcular para uma altitude customizada.
    """
    limpar()
    linha("=")
    print("  FUNÇÃO 1 e 2 - PERÍODO ORBITAL e VELOCIDADE")
    linha("=")
    print()
    print("  Formula do período   : T(h) = 2*pi * sqrt((R+h)^3 / mu)")
    print("  Formula da velocidade: v(h) = sqrt(mu / (R+h))")
    print()
    linha()

    # Cabeçalho da tabela
    print(f"  {'Satelite':<14} {'Altitude':>10}  {'Periodo':>12}  {'Velocidade':>13}")
    linha()

    for sat in SATELITES:
        h   = sat["altitude"]
        T   = periodo_orbital(h)
        v   = velocidade_orbital(h)
        print(f"  {sat['nome']:<14} {h:>8.1f} km  {T:>9.2f} min  {v:>10.4f} km/s")

    linha()
    print()
    print("  Análise matemática:")
    print("  - T(h) e CRESCENTE: altitude maior => período maior")
    print("  - v(h) e DECRESCENTE: altitude maior => velocidade menor")
    print()

    # Calculo personalizado
    print("  Calcule para outra altitude:")
    entrada = input("  Digite uma altitude em km (ou Enter para pular): ").strip()

    if entrada != "":
        try:
            h_custom = float(entrada)
            if h_custom <= 0:
                raise ValueError
            T_c = periodo_orbital(h_custom)
            v_c = velocidade_orbital(h_custom)
            print()
            print(f"  Altitude     : {h_custom:.1f} km")
            print(f"  Periodo      : {T_c:.2f} minutos")
            print(f"  Velocidade   : {v_c:.4f} km/s")
        except ValueError:
            print("  Altitude inválida. Pulando cálculo.")

    pausar()


def tela_prob_colisao():
    """
    Função 3: calcula probabilidade de colisão para uma distância informada.
    Exibe também a tabela de referência de níveis de risco.
    """
    limpar()
    linha("=")
    print("  FUNÇÃO 3 - PROBABILIDADE DE COLISÃO")
    linha("=")
    print()
    print("  Formula: P(d) = e ^ (-d / 0.5)")
    print()
    print("  Tabela de referência:")
    linha()
    print(f"  {'Distância':>12}  {'P(d)':>8}  {'Nível de Risco':<12}  Ação")
    linha()

    cenarios = [
        (0.1, "Protocolo imediato"),
        (0.2, "Manobra evasiva"),
        (0.5, "Monitoramento refor."),
        (1.0, "Registrar evento"),
        (2.0, "Sem ação"),
        (5.0, "Sem ação"),
    ]

    for d, acao in cenarios:
        P     = prob_colisao(d)
        nivel = classificar_risco(d)
        print(f"  {d:>10.1f} km  {P:>8.4f}  {nivel:<14}  {acao}")

    linha()
    print()
    print("  Análise matemática:")
    print("  - P(d) e DECRESCENTE: distância maior => risco menor")
    print("  - P(0) = 1.0 (colisão certa a distância zero)")
    print("  - Limiar operacional: d < 1 km ativa protocolo de alerta")
    print()

    entrada = input("  Informe uma distância em km para calcular (ou Enter para pular): ").strip()

    if entrada != "":
        try:
            d_custom = float(entrada)
            if d_custom < 0:
                raise ValueError
            P_c     = prob_colisao(d_custom)
            nivel_c = classificar_risco(d_custom)
            print()
            print(f"  Distância    : {d_custom:.3f} km")
            print(f"  P(d)         : {P_c:.6f}  ({P_c*100:.2f}%)")
            print(f"  Nível        : {nivel_c}")
        except ValueError:
            print("  Distância inválida. Pulando cálculo.")

    pausar()


def tela_gravidade():
    """
    Função 4: aceleração gravitacional pela lei do inverso do quadrado.
    """
    limpar()
    linha("=")
    print("  FUNÇÃO 4 - ACELERAÇÃO GRAVITACIONAL")
    linha("=")
    print()
    print("  Formula: g(h) = mu / (R_T + h)^2")
    print()
    linha()
    print(f"  {'Local':<16} {'Altitude':>10}  {'g(h)':>12}  {'% da g superfície':>18}")
    linha()

    g_sup = gravidade(0)
    print(f"  {'Superficie':<16} {'0.0':>10} km  {g_sup:>9.4f} m/s2  {'100.00%':>18}")

    for sat in SATELITES:
        h   = sat["altitude"]
        g_h = gravidade(h)
        pct = (g_h / g_sup) * 100
        print(f"  {sat['nome']:<16} {h:>8.1f} km  {g_h:>9.4f} m/s2  {pct:>16.2f}%")

    linha()
    print()
    print("  Análise matemática:")
    print("  - g(h) e DECRESCENTE: altitude maior => gravidade menor")
    print("  - Nunca chega a zero (assintota horizontal em g=0)")
    print("  - A 628 km, a gravidade ainda é ~83% da gravidade na superfície")
    print()

    entrada = input("  Informe uma altitude em km para calcular (ou Enter para pular): ").strip()

    if entrada != "":
        try:
            h_custom = float(entrada)
            if h_custom < 0:
                raise ValueError
            g_c = gravidade(h_custom)
            pct_c = (g_c / g_sup) * 100
            print()
            print(f"  Altitude     : {h_custom:.1f} km")
            print(f"  g(h)         : {g_c:.4f} m/s2")
            print(f"  % superfície : {pct_c:.2f}%")
        except ValueError:
            print("  Altitude inválida. Pulando cálculo.")

    pausar()


def tela_comparativo():
    """
    Exibe um comparativo completo dos 3 satélites com todas as funções.
    """
    limpar()
    linha("=")
    print("  COMPARATIVO COMPLETO - CBERS-4A | AMAZONIA-1 | SCD-2")
    linha("=")
    print()

    g_sup = gravidade(0)

    for sat in SATELITES:
        h     = sat["altitude"]
        T     = periodo_orbital(h)
        v     = velocidade_orbital(h)
        g_h   = gravidade(h)
        pct_g = (g_h / g_sup) * 100

        linha()
        print(f"  {sat['nome']}  -  Altitude: {h:.0f} km")
        linha()
        print(f"  Período orbital    : {T:.2f} minutos por orbita")
        print(f"  Velocidade orbital : {v:.4f} km/s  ({v*3600:.0f} km/h)")
        print(f"  Aceleração grav.   : {g_h:.4f} m/s2  ({pct_g:.1f}% da superfície)")

    print()
    linha("=")
    pausar()


# ============================================================
# GERACAO DE GRAFICOS
# ============================================================

def gerar_graficos():
    """
    Gera um arquivo PNG com 4 subplots, da biblioteca matplotlib (2x2) representando as
    4 funções matematicas do Orbitrace.
    Usa a biblioteca numpy para criar os vetores de valores e matplotlib para plotar.
    Salva como orbitrace_graficos.png e exibe na tela.
    """
    limpar()
    linha("=")
    print("  OPÇÃO 6 - GRÁFICOS DAS FUNÇÕES")
    linha("=")
    print()
    print("  Gerando gráficos das 4 funções matemáticas...")
    print("  Aguarde...")
    print()

    # Vetores de valores para os eixos x
    h_arr = np.linspace(200, 2000, 500)   # altitudes de 200 a 2000 km
    d_arr = np.linspace(0, 5, 500)        # distancias de 0 a 5 km

    # Calcula os valores y para cada funcao usando list comprehension
    T_arr = [periodo_orbital(h) for h in h_arr]
    v_arr = [velocidade_orbital(h) for h in h_arr]
    P_arr = [prob_colisao(d) for d in d_arr]
    g_arr = [gravidade(h) for h in h_arr]

    # Valores dos satelites para marcar nos graficos
    alts  = [s["altitude"] for s in SATELITES]
    T_sat = [periodo_orbital(h) for h in alts]
    v_sat = [velocidade_orbital(h) for h in alts]
    g_sat = [gravidade(h) for h in alts]

    # Atalhos para cada satelite (indices: 0=CBERS-4A, 1=AMAZONIA-1, 2=SCD-2)
    T0, T1, T2 = T_sat
    v0, v1, v2 = v_sat
    g0, g1, g2 = g_sat

    # Cria a figura com 4 subplots em grade 2x2
    fig = plt.figure(figsize=(13, 9))
    fig.suptitle(
        "Orbitrace - Gráficos das Funções Matemáticas",
        fontsize=13, fontweight="bold"
    )
    gs = gridspec.GridSpec(2, 2, hspace=0.42, wspace=0.32)

    C_CURVA  = "#1f6feb"   # azul para as curvas
    C_PONTO  = "#f85149"   # vermelho para os satelites

    # Offsets individuais para cada satelite em cada subplot.
    # CBERS-4A (628 km) fica bem separado dos outros dois.
    # AMAZONIA-1 e SCD-2 estao quase na mesma altitude (750/752 km):
    # AMAZONIA-1 vai para cima-direita, SCD-2 vai para baixo-direita,
    # com setas curvas e fundo branco para nao cobrir a curva.
    #
    # Formato: (xytext_x, xytext_y) absoluto para cada satelite
    #   indice 0 = CBERS-4A | 1 = AMAZONIA-1 | 2 = SCD-2

    bbox_props = dict(boxstyle="round,pad=0.25", fc="white", ec="gray",
                      alpha=0.85, lw=0.5)
    arrow_props = dict(arrowstyle="-", color="gray", lw=0.7,
                       connectionstyle="arc3,rad=0.2")

    # ---- Subplot 1: Periodo Orbital T(h) ----
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(h_arr, T_arr, color=C_CURVA, linewidth=2)
    ax1.scatter(alts, T_sat, color=C_PONTO, s=60, zorder=5, label="Satélites BR")
    # CBERS-4A: label acima-esquerda, longe da curva
    ax1.annotate(f"CBERS-4A\n{T0:.1f} min", xy=(628, T0),
                 xytext=(350, 107), fontsize=7, bbox=bbox_props,
                 arrowprops=arrow_props)
    # AMAZONIA-1: label acima-direita
    ax1.annotate(f"AMAZONIA-1\n{T1:.1f} min", xy=(752, T1),
                 xytext=(950, 110), fontsize=7, bbox=bbox_props,
                 arrowprops=arrow_props)
    # SCD-2: label abaixo-direita
    ax1.annotate(f"SCD-2\n{T2:.1f} min", xy=(750, T2),
                 xytext=(950, 93), fontsize=7, bbox=bbox_props,
                 arrowprops=arrow_props)
    ax1.set_title("T(h) - Período Orbital", fontsize=9, fontweight="bold")
    ax1.set_xlabel("Altitude h (km)", fontsize=8)
    ax1.set_ylabel("Período (min)", fontsize=8)
    ax1.tick_params(labelsize=7)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=7)

    # ---- Subplot 2: Velocidade Orbital v(h) ----
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(h_arr, v_arr, color="#3fb950", linewidth=2)
    ax2.scatter(alts, v_sat, color=C_PONTO, s=60, zorder=5, label="Satélites BR")
    # CBERS-4A: label acima-esquerda
    ax2.annotate(f"CBERS-4A\n{v0:.2f} km/s", xy=(628, v0),
                 xytext=(350, 7.68), fontsize=7, bbox=bbox_props,
                 arrowprops=arrow_props)
    # AMAZONIA-1: label acima-direita
    ax2.annotate(f"AMAZONIA-1\n{v1:.2f} km/s", xy=(752, v1),
                 xytext=(1000, 7.60), fontsize=7, bbox=bbox_props,
                 arrowprops=arrow_props)
    # SCD-2: label abaixo-direita
    ax2.annotate(f"SCD-2\n{v2:.2f} km/s", xy=(750, v2),
                 xytext=(1000, 7.35), fontsize=7, bbox=bbox_props,
                 arrowprops=arrow_props)
    ax2.set_title("v(h) - Velocidade Orbital", fontsize=9, fontweight="bold")
    ax2.set_xlabel("Altitude h (km)", fontsize=8)
    ax2.set_ylabel("Velocidade (km/s)", fontsize=8)
    ax2.tick_params(labelsize=7)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=7)

    # ---- Subplot 3: Probabilidade de Colisao P(d) ----
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(d_arr, P_arr, color=C_PONTO, linewidth=2)

    # Labels posicionados dentro de cada faixa de risco:
    # CRITICO: d < 0.2  -> label entre 0.0 e 0.2
    # ALTO:    0.2-0.5  -> label entre 0.2 e 0.5
    # MEDIO:   0.5-1.0  -> label entre 0.5 e 1.0
    # BAIXO:   d > 1.0  -> label apos 1.0
    limiares = [(0.2, "CRÍTICO", "#f85149", 0.93),
                (0.5, "ALTO",    "#ff7b00", 0.83),
                (1.0, "MÉDIO",   "#e5c100", 0.73)]
    for dl, rot, cor, y_pos in limiares:
        ax3.axvline(dl, color=cor, linestyle=":", linewidth=1.2)

    # Label de cada faixa centralizado dentro dela, na altura da curva local
    ax3.text(0.07,  0.72, "CRÍTICO", fontsize=6.5, color="#f85149",
             fontweight="bold",
             bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
    ax3.text(0.27,  0.45, "ALTO", fontsize=6.5, color="#ff7b00",
             fontweight="bold",
             bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
    ax3.text(0.57,  0.25, "MÉDIO", fontsize=6.5, color="#e5c100",
             fontweight="bold",
             bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
    ax3.text(2.0,   0.10, "BAIXO", fontsize=6.5, color="#3fb950",
             fontweight="bold",
             bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
    ax3.set_title("P(d) - Probabilidade de Colisão", fontsize=9, fontweight="bold")
    ax3.set_xlabel("Distância mínima d (km)", fontsize=8)
    ax3.set_ylabel("P(d)", fontsize=8)
    ax3.tick_params(labelsize=7)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(-0.02, 1.05)

    # ---- Subplot 4: Aceleracao Gravitacional g(h) ----
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(h_arr, g_arr, color="#bc8cff", linewidth=2)
    ax4.scatter(alts, g_sat, color=C_PONTO, s=60, zorder=5, label="Satélites BR")
    g_sup = gravidade(0)
    ax4.axhline(g_sup, color="gray", linestyle="--", linewidth=0.9, alpha=0.6)
    ax4.text(1400, g_sup + 0.08, f"g sup = {g_sup:.2f} m/s2",
             fontsize=7, color="gray")
    # CBERS-4A: label acima-esquerda, longe da curva
    ax4.annotate(f"CBERS-4A\n{g0:.2f} m/s2", xy=(628, g0),
                 xytext=(300, 9.0), fontsize=7, bbox=bbox_props,
                 arrowprops=arrow_props)
    # AMAZONIA-1: label direita-acima
    ax4.annotate(f"AMAZONIA-1\n{g1:.2f} m/s2", xy=(752, g1),
                 xytext=(1050, 8.7), fontsize=7, bbox=bbox_props,
                 arrowprops=arrow_props)
    # SCD-2: label direita-abaixo
    ax4.annotate(f"SCD-2\n{g2:.2f} m/s2", xy=(750, g2),
                 xytext=(1050, 7.2), fontsize=7, bbox=bbox_props,
                 arrowprops=arrow_props)
    ax4.set_title("g(h) - Aceleração Gravitacional", fontsize=9, fontweight="bold")
    ax4.set_xlabel("Altitude h (km)", fontsize=8)
    ax4.set_ylabel("g (m/s²)", fontsize=8)
    ax4.tick_params(labelsize=7)
    ax4.grid(True, alpha=0.3)
    ax4.legend(fontsize=7)

    # Salva e exibe
    nome_arquivo = "orbitrace_graficos.png"
    plt.savefig(nome_arquivo, dpi=150, bbox_inches="tight")

    linha()
    print(f"  Gráficos salvos em: {nome_arquivo}")
    linha()

    plt.show()
    pausar()


# ============================================================
# MENU PRINCIPAL
# ============================================================

def mostrar_menu():
    limpar()
    linha("=")
    print("         ORBITRACE - MODELAGEM MATEMÁTICA")
    print("         Differentiated Problem Solving | FIAP 2026")
    linha("=")
    print()
    print("  1. Sobre o projeto")
    print("  2. Função 1 e 2 - Período orbital e Velocidade")
    print("  3. Função 3 - Probabilidade de colisão")
    print("  4. Função 4 - Aceleração gravitacional")
    print("  5. Comparativo completo dos satélites")
    print("  6. Gerar gráficos das funções")
    print("  7. Sair")
    print()
    linha()


def iniciar():
    while True:
        mostrar_menu()
        opcao = input("  Escolha uma opção: ").strip()

        if opcao == "1":
            tela_sobre()
        elif opcao == "2":
            tela_periodo_velocidade()
        elif opcao == "3":
            tela_prob_colisao()
        elif opcao == "4":
            tela_gravidade()
        elif opcao == "5":
            tela_comparativo()
        elif opcao == "6":
            gerar_graficos()
        elif opcao == "7":
            print()
            print("  Encerrando o Orbitrace. Até logo!")
            print()
            break
        else:
            print("  Opção inválida. Digite um número de 1 a 7.")
            pausar()


if __name__ == "__main__":
    iniciar()
