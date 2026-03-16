# Simulation de Solitons via le Formalisme de Hirota

## 📋 Description

Implémentation Python de solutions exactes de solitons pour l'équation de Schrödinger non linéaire (NLSE) à deux composantes, basée sur le formalisme de Hirota.

Ce projet génère des visualisations 3D interactives de différents types de solitons:
- **1-solitons sombres** (comparaison pour différentes valeurs de θ)
- **3-solitons sombres** (collision multiple)
- **2-solitons brillants** (collision binaire)
- **Solitons mixtes** (brillants)

## 📚 Référence

Basé sur le document: **Two_Components_NLSE**
- Section II: Solitons brillants
- Section III: Solitons sombres
- Section IV: Solitons mixtes

## 🎯 Fonctionnalités

### Visualisations Interactives (Plotly)
✅ Graphiques 3D rotatifs et zoomables  
✅ Affichage des valeurs au survol (hover)  
✅ Export HTML autonome  
✅ Police augmentée pour présentations  
✅ Fond transparent (sans grille grise)  
✅ Graduations visibles sur les axes  
✅ Support des temps négatifs (voir collision complète)  

### Formats de Sortie
- **HTML** (Plotly): Graphiques interactifs
- **PNG** (Matplotlib): Images statiques pour rapports

## 📁 Structure du Projet

```
├── hirota_1_soliton_sombre.py              # Comparaison 1-solitons (4 cas)
├── hirota_3_solitons_sombres.py            # 3-solitons sombres (collision)
├── hirota_2_solitons_brillants_plotly.py   # 2-solitons brillants
├── hirota_solitons_mixtes.py               # Solitons mixtes
├── Two_Components_NLSE.pdf                 # Document de référence
└── Simu resultats/                         # Dossier des résultats
    ├── *.html                              # Fichiers Plotly interactifs
    └── *.png                               # Images Matplotlib statiques
```

## 💻 Utilisation

### 1. Comparaison de 1-Solitons Sombres

Compare 4 valeurs de θ (π/4, π/2, 3π/4, π):

```bash
python hirota_1_soliton_sombre.py
```

**Sorties:**
- `comparaison_1soliton_sombre_2d.png` (4 graphiques 2D)
- `comparaison_1soliton_sombre_3d.png` (4 vues 3D côte à côte)
- `1soliton_sombre_projections.png` (vue avec projections)

### 2. Collision de 3 Solitons Sombres

Simulation de 3 solitons sombres en interaction:

```bash
python hirota_3_solitons_sombres.py
```

**Paramètres modifiables:**
```python
generate_3d_plots(
    xmax=20.0,      # Domaine spatial
    tmax=20.0,      # Temps final
    tmin=-20.0,     # Temps initial (négatif!)
    Nx=1024,        # Résolution en x
    Nt=1024         # Résolution en t
)
```

**Sortie:**
- `solitons_sombres_collision_3_plotly.html` (graphique 3D interactif)

### 3. Collision de 2 Solitons Brillants

Simulation de 2 solitons brillants:

```bash
python hirota_2_solitons_brillants_plotly.py
```

**Sortie:**
- `2_solitons_brillants_collision_plotly.html`

### 4. Solitons Mixtes

Interaction de solitons brillants et sombres:

```bash
python hirota_solitons_mixtes.py
```

**Sortie:**
- `solitons_brillants_mixtes_plotly.html`

## 🎨 Personnalisation

### Modifier la Plage Temporelle

Pour voir la collision depuis le début, utilisez un temps négatif:

```python
# Dans le fichier .py
generate_plotly_plots(tmin=-10.0)  # Commence à t = -10
```

### Ajuster les Graduations

Dans la configuration de chaque axe:

```python
xaxis=dict(
    dtick=10,       # Espacement entre graduations
    ticklen=8,      # Longueur des barres
    tickwidth=2     # Épaisseur des barres
)
```

### Changer la Palette de Couleurs

```python
# Dans go.Surface()
colorscale='Jet'     # Options: 'Viridis', 'Plasma', 'Twilight', 'RdYlBu_r'
```

### Modifier la Taille de Police

```python
# Dans fig.update_layout()
xaxis=dict(
    title_font=dict(size=28),  # Titre de l'axe
    tickfont=dict(size=18)     # Valeurs de l'axe
)
```

## 📊 Équations Implémentées

### Équation Générale (Équation 1 du PDF)
```
|Ψ|² = (1/γ) ∂²ₓ ln(G) - β/γ
```

### 1-Soliton Sombre (Équation 11)
```
|Ψ|² = 1 - sin²(θ/2) sech²(Λ/2)
```
où `Λ = μx + λt + φ`

### 3-Solitons Sombres (Équations 12-16)
```
G = 1 + εG₁ + ε²G₂ + ε³G₃
```

### 2-Solitons Brillants (Équations 2-8)
```
G = 1 + ε²G₂ + ε⁴G₄
Ξⱼ = Θⱼx + Ωⱼt + Φⱼ
```

### Solitons Mixtes (Équations 17-21)
```
G = 1 + ε²G₂ + ε⁴G₄  (avec β = -γ)
```

## 🔧 Paramètres Physiques

### Constantes du Système
- **γ (gamma)**: -1 pour solitons sombres, 1 pour brillants
- **κ (kappa)**: 1 (standard)
- **ε (epsilon)**: 1 (amplitude)
- **N**: 2 (dimension système vectoriel)

### Paramètres Ajustables

**Pour solitons sombres:**
```python
theta1 = 5*np.pi/8    # Angle du soliton 1
theta2 = 7*np.pi/8    # Angle du soliton 2
theta3 = 9*np.pi/8    # Angle du soliton 3
```

**Pour solitons brillants:**
```python
Theta1 = 0.25 - 2.0j  # Paramètre complexe 1
Theta2 = 0.25 + 1.0j  # Paramètre complexe 2
Phi1 = -10.0          # Phase initiale 1
Phi2 = 0.0            # Phase initiale 2
```

## 📈 Résultats Typiques

### Densité Minimale vs θ (1-soliton sombre)

**Formule:** `Profondeur = sin²(θ/2)`

### Vitesses des Solitons

**Solitons sombres:**
```
v = -λ/μ
```

**Solitons brillants:**
```
v ≈ -2·Re(Ω) / Re(Θ)
```

## 🔬 Cas d'Usage Scientifiques

### Étude de Collisions
- Observer l'interaction élastique de solitons
- Mesurer les décalages de phase après collision
- Analyser la conservation de l'énergie

### Comparaisons
- Effet du paramètre θ sur la profondeur des solitons sombres
- Différences entre solitons brillants et sombres
- Dynamique des solitons mixtes

### Validation
- Vérification des solutions exactes du formalisme de Hirota
- Comparaison avec simulations numériques (BPM, split-step)

## 📊 Performances

### Temps de Calcul (approximatif)

| Configuration     | Nx×Nt      | Temps     |
|-------------------|------------|-----------|
| Basse résolution  | 256×100    | ~1s       |
| Moyenne résolution| 512×150    | ~1s       |
| Haute résolution  | 1024×1024  | ~3s       |

## 📝 Licence

Projet académique - M1 Ingénierie 4  
R&D - Simulation de Solitons

## 🔗 Références

1. Hirota, R. (1971). "Exact solution of the Korteweg-de Vries equation for multiple collisions of solitons"
2. Document PDF: "Two_Components_NLSE" (fourni avec le projet)
3. Plotly Documentation: https://plotly.com/python/



---

