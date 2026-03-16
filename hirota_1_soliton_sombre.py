#!/usr/bin/env python3
"""
python hirota_1_soliton_sombre.py

COMPARAISON DE PLUSIEURS 1-SOLITONS SOMBRES
Basé sur le PDF: Two_Components_NLSE - Section III.A (équation 11)

Équation (11) du PDF:
|Ψ|² = 1 - sin²(θ/2) sech²(Λ/2)

où Λ = μx + λt + φ
avec:
  μ² = -4γ sin²(θ/2)
  λ = -κμ - γ sin(θ)

Figure 2 du PDF: Comparaison pour θ = π/4, π/2, 3π/4, π
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================================
# PARAMÈTRES DU FORMALISME DE HIROTA
# ============================================================================
gamma = -1.0      # γ = -1 (pour solitons sombres)
kappa = 1.0       # κ = 1
phi = 0.0         # φ = 0 (phase initiale)

# Valeurs de θ à tester (comme dans la Figure 2 du PDF)
theta_values = [
    np.pi / 4.0,      # θ = π/4
    np.pi / 2.0,      # θ = π/2
    3.0 * np.pi / 4.0, # θ = 3π/4
    np.pi             # θ = π
]

theta_labels = ['π/4', 'π/2', '3π/4', 'π']

# Couleurs pour chaque cas
colors = ['blue', 'green', 'red', 'purple']

# ============================================================================
# CALCUL DES PARAMÈTRES μ ET λ POUR CHAQUE θ
# ============================================================================

def compute_mu(theta):
    """μ² = -4γ sin²(θ/2)"""
    return np.sqrt(-4.0 * gamma * np.sin(theta / 2.0)**2)

def compute_lambda(mu, theta):
    """λ = -κμ - γ sin(θ)"""
    return -kappa * mu - gamma * np.sin(theta)

# Calculer μ et λ pour chaque θ
mu_values = [compute_mu(theta) for theta in theta_values]
lambda_values = [compute_lambda(mu, theta) for mu, theta in zip(mu_values, theta_values)]

print("="*70)
print(" COMPARAISON DE PLUSIEURS 1-SOLITONS SOMBRES")
print(" (Section III.A du PDF - Équation 11)")
print("="*70)

print("\nParamètres pour chaque valeur de θ:")
for i, (theta, theta_label, mu, lam) in enumerate(zip(theta_values, theta_labels, mu_values, lambda_values), 1):
    print(f"\nCas {i}: θ = {theta_label}")
    print(f"  θ = {theta:.6f} rad")
    print(f"  μ = {mu:.6f}")
    print(f"  λ = {lam:.6f}")
    print(f"  sin²(θ/2) = {np.sin(theta/2.0)**2:.6f}")

# ============================================================================
# CALCUL DE LA DENSITÉ (Équation 11 du PDF)
# ============================================================================

def compute_Lambda(x, t, mu, lam, phi):
    """Λ = μx + λt + φ"""
    return mu * x + lam * t + phi

def compute_density_1soliton(x, t, theta, mu, lam):
    """
    Équation (11) du PDF:
    |Ψ|² = 1 - sin²(θ/2) sech²(Λ/2)
    """
    Lambda = compute_Lambda(x, t, mu, lam, phi)
    
    sin_theta_half_sq = np.sin(theta / 2.0)**2
    sech_Lambda_half_sq = 1.0 / np.cosh(Lambda / 2.0)**2
    
    density = 1.0 - sin_theta_half_sq * sech_Lambda_half_sq
    
    return density

# ============================================================================
# DOMAINE DE SIMULATION
# ============================================================================

# Pour la comparaison 2D
x_2d = np.linspace(-20, 20, 1000)
t_2d = 15.0  # Temps fixe pour la comparaison 2D

# Pour les graphiques 3D
xmax = 30.0
tmax = 30.0
Nx = 512
Nt = 150

x_3d = np.linspace(-xmax, xmax, Nx)
tvec = np.linspace(0, tmax, Nt)

# ============================================================================
# GRAPHIQUE 1: COMPARAISON 2D - TOUS SUR LE MÊME REPÈRE
# ============================================================================

print("\n" + "="*70)
print(" GÉNÉRATION DES GRAPHIQUES")
print("="*70)
print("\nGraphique 1: Comparaison 2D (tous sur même repère)...")

fig1 = plt.figure("Comparaison 2D - Plusieurs 1-Solitons Sombres", figsize=(14, 10))

# Subplot 1: Profils à t fixe (comme Figure 2 du PDF)
ax1 = fig1.add_subplot(221)

for i, (theta, theta_label, mu, lam, color) in enumerate(zip(theta_values, theta_labels, mu_values, lambda_values, colors)):
    density = compute_density_1soliton(x_2d, t_2d, theta, mu, lam)
    ax1.plot(x_2d, density, color=color, linewidth=2.5, 
            label=f'θ = {theta_label}')

ax1.set_xlabel('Position $x$', fontsize=12)
ax1.set_ylabel('Densité $|\\Psi|^2$', fontsize=12)
ax1.set_title(f'Profils à t = {t_2d:.1f}\n(Équation 11 du PDF)', 
             fontsize=13, fontweight='bold')
ax1.legend(fontsize=11, loc='best')
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0, 1.1])

# Subplot 2: En fonction de Λ (comme Figure 2 du PDF)
ax2 = fig1.add_subplot(222)

Lambda_range = np.linspace(-10, 10, 1000)

for i, (theta, theta_label, color) in enumerate(zip(theta_values, theta_labels, colors)):
    sin_theta_half_sq = np.sin(theta / 2.0)**2
    sech_Lambda_half_sq = 1.0 / np.cosh(Lambda_range / 2.0)**2
    density_vs_Lambda = 1.0 - sin_theta_half_sq * sech_Lambda_half_sq
    
    ax2.plot(Lambda_range, density_vs_Lambda, color=color, linewidth=2.5,
            label=f'θ = {theta_label}')

ax2.set_xlabel('$\\Lambda$', fontsize=12)
ax2.set_ylabel('$|\\Psi|^2$', fontsize=12)
ax2.set_title('Densité en fonction de Λ\n(Figure 2 du PDF)', 
             fontsize=13, fontweight='bold')
ax2.legend(fontsize=11, loc='best')
ax2.grid(True, alpha=0.3)
ax2.set_ylim([0, 1.1])

# Subplot 3: Évolution temporelle au centre (x=0)
ax3 = fig1.add_subplot(223)

tvec_evolution = np.linspace(0, 30, 300)

for i, (theta, theta_label, mu, lam, color) in enumerate(zip(theta_values, theta_labels, mu_values, lambda_values, colors)):
    density_center = [compute_density_1soliton(np.array([0.0]), t, theta, mu, lam)[0] 
                     for t in tvec_evolution]
    ax3.plot(tvec_evolution, density_center, color=color, linewidth=2.5,
            label=f'θ = {theta_label}')

ax3.set_xlabel('Temps $t$', fontsize=12)
ax3.set_ylabel('$|\\Psi|^2$ à $x=0$', fontsize=12)
ax3.set_title('Évolution temporelle au centre', 
             fontsize=13, fontweight='bold')
ax3.legend(fontsize=11, loc='best')
ax3.grid(True, alpha=0.3)
ax3.set_ylim([0, 1.1])

# Subplot 4: Profondeur du creux en fonction de θ
ax4 = fig1.add_subplot(224)

theta_fine = np.linspace(0, np.pi, 100)
min_density = [1.0 - np.sin(th/2.0)**2 for th in theta_fine]

ax4.plot(theta_fine/np.pi, min_density, 'k-', linewidth=2.5)
ax4.scatter([th/np.pi for th in theta_values], 
           [1.0 - np.sin(th/2.0)**2 for th in theta_values],
           c=colors, s=150, zorder=5, edgecolors='black', linewidth=2)

for i, (th, label) in enumerate(zip(theta_values, theta_labels)):
    ax4.annotate(f'θ={label}', 
                xy=(th/np.pi, 1.0 - np.sin(th/2.0)**2),
                xytext=(10, 10), textcoords='offset points',
                fontsize=10, color=colors[i])

ax4.set_xlabel('θ/π', fontsize=12)
ax4.set_ylabel('Densité minimale', fontsize=12)
ax4.set_title('Profondeur du creux vs θ\n$|\\Psi|^2_{min} = 1 - \\sin^2(θ/2)$', 
             fontsize=13, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.set_ylim([0, 1.1])

plt.tight_layout()

output1 = 'C:\\Users\\myxim\\Ecole\\Ecole\\M1 Inge4\\R&D\\Code devoir bonus\\bpm-master\\bpm-master\\Simu resultats\\comparaison_1soliton_sombre_2d.png'
plt.savefig(output1, dpi=200, bbox_inches='tight')
print(f"  ✓ Sauvegardé: {output1}")

# ============================================================================
# GRAPHIQUE 2: VUES 3D CÔTE À CÔTE
# ============================================================================

print("\nGraphique 2: Vues 3D côte à côte...")

# Calculer les densités 3D pour chaque cas
print("  Calcul des densités 3D...")

densities_3d = []

for i, (theta, mu, lam) in enumerate(zip(theta_values, mu_values, lambda_values)):
    density_data = np.zeros((Nt, Nx))
    
    for j, t in enumerate(tvec):
        density_data[j, :] = compute_density_1soliton(x_3d, t, theta, mu, lam)
        
        if j % 30 == 0:
            print(f"    Cas {i+1}/{len(theta_values)}, t={j+1}/{Nt}", end="\r")
    
    densities_3d.append(density_data)

print(f"    Calcul terminé!{' '*30}")

# Créer la figure avec 4 subplots 3D
fig2 = plt.figure("Comparaison 3D - Plusieurs 1-Solitons Sombres", figsize=(16, 12))

# Meshgrid
tt, xx = np.meshgrid(tvec, x_3d, indexing='ij')

for i, (density_data, theta_label, color) in enumerate(zip(densities_3d, theta_labels, colors), 1):
    ax = fig2.add_subplot(2, 2, i, projection='3d')
    
    surf = ax.plot_surface(xx, tt, density_data,
                          cmap='twilight',
                          edgecolor='none',
                          antialiased=True,
                          linewidth=0,
                          rcount=150,
                          ccount=150,
                          alpha=0.9)
    
    ax.set_xlabel('Position $x$', fontsize=10, labelpad=8)
    ax.set_ylabel('Temps $t$', fontsize=10, labelpad=8)
    ax.set_zlabel('$|\\Psi|^2$', fontsize=10, labelpad=8)
    ax.set_title(f'θ = {theta_label}', fontsize=12, fontweight='bold', pad=15)
    ax.view_init(elev=25, azim=-60)
    ax.set_zlim([0, 1.1])
    
    # Colorbar
    cbar = plt.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)
    cbar.set_label('$|\\Psi|^2$', rotation=270, labelpad=15, fontsize=9)

plt.suptitle('1-Soliton Sombre pour Différentes Valeurs de θ\n(Équation 11 du PDF)', 
            fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.96])

output2 = 'C:\\Users\\myxim\\Ecole\\Ecole\\M1 Inge4\\R&D\\Code devoir bonus\\bpm-master\\bpm-master\\Simu resultats\\comparaison_1soliton_sombre_3d.png'
plt.savefig(output2, dpi=200, bbox_inches='tight')
print(f"  ✓ Sauvegardé: {output2}")

# ============================================================================
# GRAPHIQUE 3: VUE 3D AVEC PROJECTIONS (pour un cas)
# ============================================================================

print("\nGraphique 3: Vue 3D avec projections (θ = π/2)...")

# Choisir θ = π/2 (index 1)
idx_ref = 1
density_ref = densities_3d[idx_ref]
theta_ref_label = theta_labels[idx_ref]

fig3 = plt.figure("1-Soliton Sombre avec Projections", figsize=(12, 10))
ax3 = fig3.add_subplot(111, projection='3d')

# Surface semi-transparente
surf3 = ax3.plot_surface(xx, tt, density_ref,
                        cmap='twilight',
                        edgecolor='navy',
                        lw=0.5,
                        rstride=8,
                        cstride=8,
                        alpha=0.3)

# Projections
zmin = np.min(density_ref)
zmax = np.max(density_ref)
z_offset = zmin - (zmax - zmin) * 0.05

ax3.contourf(xx, tt, density_ref,
           zdir='z', offset=z_offset,
           cmap='coolwarm', levels=15, linewidths=1.5, alpha=0.8)

ax3.contourf(xx, tt, density_ref,
           zdir='y', offset=tmax,
           cmap='coolwarm', levels=15, linewidths=1.5, alpha=0.8)

ax3.contourf(xx, tt, density_ref,
           zdir='x', offset=xmax,
           cmap='coolwarm', levels=15, linewidths=1.5, alpha=0.8)

# Configuration
ax3.set(xlim=(-xmax, xmax),
       ylim=(0, tmax),
       zlim=(z_offset, 1.1),
       xlabel='Position $x$',
       ylabel='Temps $t$',
       zlabel='$|\\Psi|^2$')

ax3.set_title(f'1-Soliton Sombre avec Projections\nθ = {theta_ref_label}',
            fontsize=13, fontweight='bold', pad=20)
ax3.view_init(elev=25, azim=-60)

cbar3 = plt.colorbar(surf3, ax=ax3, shrink=0.6, aspect=15, pad=0.1)
cbar3.set_label('$|\\Psi|^2$', rotation=270, labelpad=20)

output3 = 'C:\\Users\\myxim\\Ecole\\Ecole\\M1 Inge4\\R&D\\Code devoir bonus\\bpm-master\\bpm-master\\Simu resultats\\1soliton_sombre_projections.png'
plt.savefig(output3, dpi=200, bbox_inches='tight')
print(f"  ✓ Sauvegardé: {output3}")

# ============================================================================
# RÉSUMÉ
# ============================================================================

print("\n" + "="*70)
print(" RÉSUMÉ")
print("="*70)

print("\nCaractéristiques pour chaque valeur de θ:")
print(f"\n{'θ':<10} {'Densité min':<15} {'Profondeur creux':<20}")
print("-"*50)

for theta, theta_label in zip(theta_values, theta_labels):
    min_dens = 1.0 - np.sin(theta/2.0)**2
    depth = np.sin(theta/2.0)**2
    print(f"{theta_label:<10} {min_dens:<15.4f} {depth:<20.4f}")

print("\nFormule utilisée (Équation 11 du PDF):")
print("  |Ψ|² = 1 - sin²(θ/2) sech²(Λ/2)")
print("\nOù:")
print("  Λ = μx + λt + φ")
print("  μ² = -4γ sin²(θ/2)")
print("  λ = -κμ - γ sin(θ)")

print("\nFichiers générés:")
print(f"  1. {output1}")
print(f"  2. {output2}")
print(f"  3. {output3}")

print("\n" + "="*70)
print(" COMPARAISON TERMINÉE")
print("="*70 + "\n")

plt.show()