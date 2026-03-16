#!/usr/bin/env python3
"""
python hirota_solitons_mixtes.py

SOLITONS MIXTES - VERSION PLOTLY 3D PLEIN ÉCRAN
Basé EXACTEMENT sur le PDF: Two_Components_NLSE - Section IV
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

try:
    plt.rcParams.update({
    "text.usetex": False, # Désactive le vrai LaTeX
    "font.family": "STIXGeneral", # Utilise la police STIX (ressemble à Times/LaTeX)
    "mathtext.fontset": "stix", # Les maths en style LaTeX
    "font.size": 20,
    "axes.labelsize": 20,
    "legend.fontsize": 20,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
    })
except Exception as e:
    print(f"Attention: Impossible de configurer LaTeX ({e}). Passage en mode standard.")

# ============================================================================
# PARAMÈTRES DU FORMALISME DE HIROTA
# ============================================================================

gamma = 1.0       # γ
# cas 1
# kappa = 1.0       # κ
# cas 2
kappa = -1.0       # κ
epsilon = 1.0     # ε
N = 2             # Dimension du système vectoriel

# Paramètres des solitons mixtes
# cas 1.1
# Theta1 = 0.25 - 2.0j   # Θ₁
# Theta2 = 0.25 + 1.0j   # Θ₂
# cas 1.2
# Theta1 = 1.0 - 2.0j   # Θ₁
# Theta2 = 2.0 + 1.0j   # Θ₂
# cas 2
Theta1 = - 0.25 - 2.0j   # Θ₁
Theta2 = 0.25 + 2.0j   # Θ₂

Phi1 = 0.0           # Φ₁ (position)
Phi2 = 0.0            # Φ₂ (position)

# Vecteurs de polarisation
v1 = np.array([0.0, 1.0])
v2 = np.array([0.0, 1.0])
 
def compute_Omega(Theta_j):
    """Équation (20)"""
    return -kappa * Theta_j + 0.5j * Theta_j**2
 
Omega1 = compute_Omega(Theta1)
Omega2 = compute_Omega(Theta2)
 
def compute_alpha_pq(Theta_p, Theta_q, v_p, v_q):
    """Équation (21)"""
    v_hermitian = np.dot(np.conj(v_q), v_p)
    numerator = gamma * np.conj(Theta_q) * Theta_p * v_hermitian
    denominator = N * (np.conj(Theta_q) * Theta_p + gamma) * (Theta_p + np.conj(Theta_q))**2
    return numerator / denominator
 
alpha11 = compute_alpha_pq(Theta1, Theta1, v1, v1)
alpha12 = compute_alpha_pq(Theta1, Theta2, v1, v2)
alpha21 = compute_alpha_pq(Theta2, Theta1, v2, v1)
alpha22 = compute_alpha_pq(Theta2, Theta2, v2, v2)
 
def compute_alpha_1212():
    term1 = (alpha11 * alpha22) / ((Theta1 + np.conj(Theta2)) * (Theta2 + np.conj(Theta1)))
    term2 = (alpha12 * alpha21) / ((Theta1 + np.conj(Theta1)) * (Theta2 + np.conj(Theta2)))
    return np.abs(Theta1 - Theta2)**2 * (term1 - term2)
 
alpha_1212 = compute_alpha_1212()
 
def compute_G(x, t):
    Xi1 = Theta1 * x + Omega1 * t + Phi1
    Xi2 = Theta2 * x + Omega2 * t + Phi2
    Xi1_conj = np.conj(Theta1) * x + np.conj(Omega1) * t + np.conj(Phi1)
    Xi2_conj = np.conj(Theta2) * x + np.conj(Omega2) * t + np.conj(Phi2)
    
    G2 = (alpha11 * np.exp(Xi1 + Xi1_conj) + 
          alpha12 * np.exp(Xi1 + Xi2_conj) + 
          alpha21 * np.exp(Xi2 + Xi1_conj) + 
          alpha22 * np.exp(Xi2 + Xi2_conj))
    
    G4 = alpha_1212 * np.exp(Xi1 + Xi2 + Xi1_conj + Xi2_conj)
    return 1.0 + epsilon**2 * G2 + epsilon**4 * G4
 
def compute_density(x, t):
    """Équation (1) : |Ψ|² = (1/γ) ∂²ₓ ln(G) - β/γ avec β = -γ"""
    beta = -gamma
    dx = x[1] - x[0] if len(x) > 1 else 0.1
    G = compute_G(x, t)
    ln_G = np.log(np.abs(G) + 1e-30)
    d2_ln_G = np.gradient(np.gradient(ln_G, dx), dx)
    return np.real((1.0 / gamma) * d2_ln_G - beta / gamma)
 
# ============================================================================
# GÉNÉRATION DU GRAPHIQUE PLOTLY (3D UNIQUEMENT)
# ============================================================================
 
def generate_plotly_plots(xmax=15.0, tmax=10.0, Nx=1024, Nt=1024, tmin=-10.0):  # ← LIGNE 104: Ajout tmin=-10.0
    """Génère le graphique 3D uniquement en plein écran
    
    Args:
        xmax: Position maximale
        tmax: Temps maximal
        Nx: Nombre de points en x
        Nt: Nombre de points en t
        tmin: Temps minimal (NOUVEAU - peut être négatif!)
    """
    
    print("Calcul de la densité des solitons mixtes...")
    print(f"  Plage temporelle: t = {tmin} à {tmax}")
    
    x = np.linspace(-xmax, xmax, Nx)
    tvec = np.linspace(tmin, tmax, Nt)  # ← LIGNE 119: MODIFIÉ - Commence à tmin au lieu de 0
    density_data = np.zeros((Nt, Nx))
    
    for i, t in enumerate(tvec):
        density_data[i, :] = compute_density(x, t)
    
    # Création de la figure 3D sans subplots
    fig = go.Figure(data=[go.Surface(
        x=x, y=tvec, z=density_data,
        colorscale='Jet',
        colorbar=dict(title="|Ψ|²", thickness=20)
    )])
 
    # Mise à jour du layout pour utiliser toute la page
    fig.update_layout(
        scene=dict(
            xaxis_title='x',
            yaxis_title='t',
            zaxis_title='|Ψ|²',
            aspectmode='manual',
            aspectratio=dict(x=2, y=1.5, z=1),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1.3)),
            # ===== POLICE ET FOND =====
            xaxis=dict(
                title_font=dict(size=28),
                tickfont=dict(size=18),
                showbackground=False,
                showgrid=True,
                gridcolor='rgba(200,200,200,0.2)',
                showline=True,
                linewidth=2,
                linecolor='black',
                ticks='inside',
                dtick=5,
                ticklen=5,
                tickwidth=2,
                tickcolor='black'
            ),
            yaxis=dict(
                title_font=dict(size=28),
                tickfont=dict(size=18),
                showbackground=False,
                showgrid=True,
                gridcolor='rgba(200,200,200,0.2)',
                showline=True,
                linewidth=2,
                linecolor='black',
                ticks='inside',
                dtick=5,  # ← Graduations tous les 5 (fonctionne avec temps négatif)
                ticklen=5,
                tickwidth=2,
                tickcolor='black'
            ),
            zaxis=dict(
                title_font=dict(size=28),
                tickfont=dict(size=18),
                showbackground=False,
                showgrid=True,
                gridcolor='rgba(200,200,200,0.2)',
                showline=True,
                linewidth=2,
                linecolor='black',
                ticks='inside',
                dtick=0.1,
                ticklen=5,
                tickwidth=2,
                tickcolor='black'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=50),
        height=850,
        font=dict(size=20)
    )
 
    # Sauvegarde
    output_path = 'C:\\Users\\myxim\\Ecole\\Ecole\\M1 Inge4\\R&D\\Code devoir bonus\\bpm-master\\bpm-master\\Simu resultats\\solitons_brillants_mixtes_plotly.html'
    fig.write_html(output_path)
    
    print(f"✓ Fichier sauvegardé : {output_path}")
    return density_data
 
# ============================================================================
# MAIN
# ============================================================================
 
def analyze_parameters():
    print("\n" + "="*70)
    print(" ANALYSE: SOLITONS MIXTES (Section IV)")
    print("="*70)
    print(f"  γ = {gamma}, β = {-gamma}")
    print(f"  Soliton 1 Speed: {-2 * np.real(Omega1) / np.real(Theta1):.3f}")
    print(f"  Soliton 2 Speed: {-2 * np.real(Omega2) / np.real(Theta2):.3f}")
    print("="*70)
 
if __name__ == "__main__":
    analyze_parameters()
    
    # ========================================================================
    # APPEL AVEC TEMPS NÉGATIF
    # ========================================================================
    # AVANT: generate_plotly_plots()
    # APRÈS:  generate_plotly_plots(tmin=-10.0)
    
    generate_plotly_plots(tmin=-10.0)  # ← LIGNE 224: Commence à t = -10
    
    # Autres exemples possibles:
    # generate_plotly_plots(tmin=-15.0)           # Encore plus tôt
    # generate_plotly_plots(tmin=-5.0, tmax=40.0)  # De -5 à 40
    # generate_plotly_plots(tmin=0.0)              # Temps normal (0 à 50)