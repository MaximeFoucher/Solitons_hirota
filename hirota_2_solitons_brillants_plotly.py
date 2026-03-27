#!/usr/bin/env python3
"""
python hirota_2_solitons_brillants_plotly.py

2 SOLITONS BRILLANTS (3D) - VERSION PLOTLY INTERACTIVE (3D UNIQUEMENT)
Génération de la solution exacte des solitons brillants via le formalisme de Hirota
"""

import numpy as np
import plotly.graph_objects as go

# ============================================================================
# PARAMÈTRES DU FORMALISME DE HIROTA (équation 9 du PDF)
# ============================================================================
gamma = 1.0
kappa = 1.0
epsilon = 1.0
N = 2

# Paramètres des solitons
Theta1 = 0.25 - 2.0j
Theta2 = 0.25 + 1.0j
Phi1 = -10.0
Phi2 = 0.0

# Vecteurs de polarisation (équation 10)
v1 = np.array([1.0, 1.0j])
v2 = np.array([-1.0j, 1.0])

def compute_Omega(Theta):
    """Équation (6) du PDF"""
    return -kappa * Theta + 0.5j * Theta**2 - 1.0j * gamma

def compute_a_coefficients():
    """Équation (7) du PDF: a^q_p = (γ/N) * (v†_q · v_p) / (Θ_p + Θ*_q)²"""
    a11 = (gamma / N) * (np.dot(np.conj(v1), v1)) / ((Theta1 + np.conj(Theta1))**2)
    a21 = (gamma / N) * (np.dot(np.conj(v2), v1)) / ((Theta1 + np.conj(Theta2))**2)
    a12 = (gamma / N) * (np.dot(np.conj(v1), v2)) / ((Theta2 + np.conj(Theta1))**2)
    a22 = (gamma / N) * (np.dot(np.conj(v2), v2)) / ((Theta2 + np.conj(Theta2))**2)
    return a11, a21, a12, a22

def compute_a1212():
    """Équation (8) du PDF"""
    a11, a21, a12, a22 = compute_a_coefficients()
    term1 = (a11 * a22) / ((Theta1 + np.conj(Theta2)) * (Theta2 + np.conj(Theta1)))
    term2 = (a21 * a12) / ((Theta1 + np.conj(Theta1)) * (Theta2 + np.conj(Theta2)))
    a12_12 = np.abs(Theta1 - Theta2)**2 * (term1 - term2)
    return a12_12

def compute_G(x, t):
    """Équations (2-4) du PDF: G = 1 + ε²G₂ + ε⁴G₄"""
    Omega1 = compute_Omega(Theta1)
    Omega2 = compute_Omega(Theta2)
    
    Xi1 = Theta1 * x + Omega1 * t + Phi1
    Xi2 = Theta2 * x + Omega2 * t + Phi2
    Xi1_conj = np.conj(Theta1) * x + np.conj(Omega1) * t + np.conj(Phi1)
    Xi2_conj = np.conj(Theta2) * x + np.conj(Omega2) * t + np.conj(Phi2)
    
    a11, a21, a12, a22 = compute_a_coefficients()
    a1212 = compute_a1212()
    
    G2 = (a11 * np.exp(Xi1 + Xi1_conj) + 
          a21 * np.exp(Xi1 + Xi2_conj) + 
          a12 * np.exp(Xi2 + Xi1_conj) + 
          a22 * np.exp(Xi2 + Xi2_conj))
    
    G4 = a1212 * np.exp(Xi1 + Xi2 + Xi1_conj + Xi2_conj)
    G = 1.0 + epsilon**2 * G2 + epsilon**4 * G4
    return G

def compute_density(x, t):
    """Équation (1) du PDF: |Ψ|² = (1/γ) ∂²ₓ ln(G)"""
    beta = 0.0  
    dx = x[1] - x[0] if len(x) > 1 else 0.1
    G = compute_G(x, t)
    ln_G = np.log(np.abs(G) + 1e-30)
    d2_ln_G = np.gradient(np.gradient(ln_G, dx), dx)
    density = (1.0 / gamma) * d2_ln_G - beta / gamma
    return np.real(density)

# ============================================================================
# GÉNÉRATION DES GRAPHIQUES PLOTLY (MODIFIÉ POUR 3D UNIQUEMENT)
# ============================================================================

def generate_plotly_plots(xmax=50.0, tmax=30.0, Nx=1024, Nt=1024):
    """Génère le graphique 3D uniquement sans les coupes 2D"""
    
    print("="*70)
    print(" CALCUL: 2 SOLITONS BRILLANTS (VERSION 3D EXCLUSIVE)")
    print("="*70)
    
    x = np.linspace(-15.0, 55.0, Nx)
    tvec = np.linspace(0, tmax, Nt)
    density_data = np.zeros((Nt, Nx))
    
    for i, t in enumerate(tvec):
        density_data[i, :] = compute_density(x, t)
    
    # Création du graphique avec uniquement la surface
    fig = go.Figure(data=[go.Surface(
        x=x, y=tvec, z=density_data,
        colorscale='Jet',
        colorbar=dict(
            title="|Ψ|²",
            thickness=15,          # Épaisseur fine
            len=0.8,               # Taille réduite pour ne pas dépasser
            x=1.05,                # Positionnée juste après le bord droit (1.0)
            y=0.5,
            yanchor='middle',
            title_font=dict(size=20),
            tickfont=dict(size=16)
            )
    )])

    # Mise à jour du layout pour utiliser toute la page
    fig.update_layout(
        scene=dict(
            xaxis_title='x',
            yaxis_title='t',
            #zaxis_title='|Ψ|²',
            aspectmode='manual',
            aspectratio=dict(x=2, y=1.5, z=1),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1.3)),
            # ===== POLICE ET FOND - LIGNES 132-170 =====
            xaxis=dict(
                title_font=dict(size=28),       # ← LIGNE 134: Police titre X (augmentée à 28)
                tickfont=dict(size=18),         # ← LIGNE 135: Police valeurs X (augmentée à 22)
                showbackground=False,           # ← LIGNE 136: Enlève fond gris
                showgrid=True,                  
                gridcolor='rgba(200,200,200,0.2)', # ← LIGNE 138: Grille très légère (presque invisible)
                showline=True,
                linewidth=2,
                linecolor='black',
                ticks='inside',                # ← Affiche les petites barres
                dtick=10,                       # ← Graduation tous les 10
                ticklen=8,                      # ← Longueur des barres
                tickwidth=2,                    # ← Épaisseur des barres
                tickcolor='black'               # ← Couleur des barres
            ),
            yaxis=dict(
                title_font=dict(size=28),       # ← LIGNE 144: Police titre Y
                tickfont=dict(size=18),         # ← LIGNE 145: Police valeurs Y
                showbackground=False,           # ← LIGNE 146: Enlève fond gris
                showgrid=True,
                gridcolor='rgba(200,200,200,0.2)',
                showline=True,
                linewidth=2,
                linecolor='black',
                ticks='inside',                # ← Affiche les petites barres
                dtick=10,                       # ← Graduation tous les 10
                ticklen=8,                      # ← Longueur des barres
                tickwidth=2,                    # ← Épaisseur des barres
                tickcolor='black'               # ← Couleur des barres
            ),
            zaxis=dict(
                title='',                       # ← Pas de titre
                showticklabels=False,           # ← Cache les valeurs (0.0, 0.5, 1.0...)
                showbackground=True,           # ← Pas de fond gris
                showgrid=False,                 # ← Pas de grille verticale
                showline=False,                 # ← Pas de ligne d'axe
                zeroline=False,                 # ← Pas de ligne zéro
                showspikes=False,               # ← Pas de pics au survol
                visible=True
            ),
            bgcolor='rgba(0,0,0,0)'  # ← LIGNE 163: Fond complètement transparent
        ),
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=50),
        height=850,
        font=dict(size=20)  # ← LIGNE 168: Police générale (augmentée à 20)
    )

    # Sauvegarde vers votre chemin spécifique
    output_path = 'C:\\Users\\myxim\\Ecole\\Ecole\\M1 Inge4\\R&D\\Code devoir bonus\\bpm-master\\bpm-master\\Simu resultats\\2_solitons_brillants_collision_plotly.html'
    config = {
        'editable': True,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'collision_2_solitons_brillants',
            'scale': 10  # Haute définition pour votre poster
        }
    }
    fig.write_html(output_path, config=config)
    
    return density_data, x, tvec

# ============================================================================
# ANALYSE
# ============================================================================

def analyze_collision():
    """Analyse les caractéristiques de la collision"""
    print("\n" + "="*70)
    print(" ANALYSE: 2 SOLITONS BRILLANTS (Formalisme de Hirota)")
    print("="*70)
    
    a11, a21, a12, a22 = compute_a_coefficients()
    a1212 = compute_a1212()
    
    v1_speed = -2 * np.real(compute_Omega(Theta1)) / np.real(Theta1)
    v2_speed = -2 * np.real(compute_Omega(Theta2)) / np.real(Theta2)
    
    print(f"  Coefficients: a11={a11:.4f}, a22={a22:.4f}, a1212={a1212:.4f}")
    print(f"  Vitesses: v1 ≈ {v1_speed:.3f}, v2 ≈ {v2_speed:.3f}")
    print("="*70)

if __name__ == "__main__":
    analyze_collision()
    density, x, t = generate_plotly_plots()
    
    print("\n✓ RÉSULTAT: Fichier sauvegardé sous '2_solitons_brillants_collision_plotly.html'")

