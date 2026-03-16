#!/usr/bin/env python3
"""
python hirota_3_solitons_sombres.py

3 SOLITONS SOMBRES - VERSION PLOTLY 3D UNIQUEMENT
Basé sur le PDF: Two_Components_NLSE - Section III.B
Modifié pour n'afficher que la vue 3D interactive sur toute la page.
"""

import numpy as np
import plotly.graph_objects as go

# ============================================================================
# PARAMÈTRES (Figure 3 du PDF)
# ============================================================================
gamma = -1.0      # γ = -1 pour solitons sombres
kappa = 1.0
epsilon = 1.0

# Paramètres des solitons (θ_j)
theta1 = (5*np.pi) / 8.0
theta2 = (7*np.pi) / 8.0
theta3 = (9*np.pi) / 8.0

# Phases (φ_j)
phi1 = 0.0
phi2 = 0.0
phi3 = 0.0

def compute_mu(theta):
    """Équation (14)"""
    return np.sqrt(-4.0 * gamma) * np.sin(theta / 2.0)
 
def compute_lambda(theta, mu):
    """Équation (15)"""
    return -kappa * mu - gamma * np.sin(theta)
 
def compute_A(theta_p, theta_q):
    """Équation (16)"""
    num = np.sin((theta_p - theta_q) / 4.0)**2
    den = np.sin((theta_p + theta_q) / 4.0)**2
    return num / den
 
def compute_G_sombres(x, t):
    """Formules (12-13) pour 3 solitons sombres"""
    mu1, mu2, mu3 = compute_mu(theta1), compute_mu(theta2), compute_mu(theta3)
    lam1, lam2, lam3 = compute_lambda(theta1, mu1), compute_lambda(theta2, mu2), compute_lambda(theta3, mu3)
    
    L1 = mu1 * x + lam1 * t + phi1
    L2 = mu2 * x + lam2 * t + phi2
    L3 = mu3 * x + lam3 * t + phi3
    
    A12 = compute_A(theta1, theta2)
    A13 = compute_A(theta1, theta3)
    A23 = compute_A(theta2, theta3)
    
    G1 = np.exp(L1) + np.exp(L2) + np.exp(L3)
    G2 = A12 * np.exp(L1 + L2) + A13 * np.exp(L1 + L3) + A23 * np.exp(L2 + L3)
    G3 = A12 * A13 * A23 * np.exp(L1 + L2 + L3)
    
    return 1.0 + epsilon * G1 + epsilon**2 * G2 + epsilon**3 * G3
 
def compute_density_sombres(x, t):
    """|Ψ|² = 1 + (1/γ) ∂²ₓ ln(G)"""
    dx = x[1] - x[0] if len(x) > 1 else 0.1
    G = compute_G_sombres(x, t)
    ln_G = np.log(np.abs(G) + 1e-30)
    d2_ln_G = np.gradient(np.gradient(ln_G, dx), dx)
    return 1.0 + (1.0 / gamma) * d2_ln_G
 
# ============================================================================
# GÉNÉRATION DU GRAPHIQUE PLOTLY (3D UNIQUEMENT)
# ============================================================================
 
def generate_3d_plots(xmax=20.0, tmax=20.0, Nx=1024, Nt=1024, tmin=-20.0):  # ← LIGNE 77: Ajout paramètre tmin
    """Génère uniquement la surface 3D sans les graphiques 2D latéraux
    
    Args:
        xmax: Position maximale
        tmax: Temps maximal
        Nx: Nombre de points en x
        Nt: Nombre de points en t
        tmin: Temps minimal (NOUVEAU - peut être négatif!)
    """
    
    print("Calcul de la simulation des 3 solitons sombres...")
    print(f"  Plage temporelle: t = {tmin} à {tmax}")
    
    x = np.linspace(-xmax, xmax, Nx)
    tvec = np.linspace(tmin, tmax, Nt)  # ← LIGNE 92: MODIFIÉ - Commence à tmin au lieu de 0
    density_data = np.zeros((Nt, Nx))
    
    for i, t in enumerate(tvec):
        density_data[i, :] = compute_density_sombres(x, t)
    
    # Création de la figure simple (pas de subplots)
    fig = go.Figure(data=[go.Surface(
        x=x, 
        y=tvec, 
        z=density_data,
        colorscale='Jet',
        colorbar=dict(title="|Ψ|²", thickness=20)
    )])
 
    # Mise à jour du layout pour occuper tout l'écran
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
                dtick=10,
                ticklen=8,
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
                dtick=10,  # ← Graduations tous les 10 (même avec temps négatif)
                ticklen=8,
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
                ticklen=8,
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
    output_path = 'C:\\Users\\myxim\\Ecole\\Ecole\\M1 Inge4\\R&D\\Code devoir bonus\\bpm-master\\bpm-master\\Simu resultats\\solitons_sombres_collision_3_plotly.html'
    fig.write_html(output_path)
    
    print(f"✓ Fichier sauvegardé : {output_path}")
    return density_data, x, tvec
 
# ============================================================================
# ANALYSE ET EXÉCUTION
# ============================================================================
 
def analyze_parameters():
    print("\n" + "="*70)
    print(" PARAMÈTRES: 3 SOLITONS SOMBRES")
    print("="*70)
    for i, th in enumerate([theta1, theta2, theta3], 1):
        mu = compute_mu(th)
        lam = compute_lambda(th, mu)
        print(f"  Soliton {i}: θ={th:.2f}, μ={mu:.3f}, λ={lam:.3f}")
    print("="*70)
 
if __name__ == "__main__":
    analyze_parameters()
    
    # ========================================================================
    # APPEL AVEC TEMPS NÉGATIF
    # ========================================================================
    # AVANT: generate_3d_plots()
    # APRÈS:  generate_3d_plots(tmin=-20.0)
    
    generate_3d_plots(tmin=-20.0)  # ← LIGNE 196: Commence à t = -20
    
    # Autres exemples possibles:
    # generate_3d_plots(tmin=-30.0)           # Encore plus tôt
    # generate_3d_plots(tmin=-10.0, tmax=40.0) # De -10 à 40
    # generate_3d_plots(tmin=0.0)             # Temps normal (0 à 50)