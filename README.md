![PNS](logo-pns.png)
## MAM5/M2-INUM
# Projet de fin d'étude
# 2024-25

# Virtual-element-method

## Overview

La Virtual Elements Method (VEM) est une approche numérique innovante utilisée pour résoudre des problèmes d'ingénierie et de physique dans des domaines tels que la mécanique des fluides, la mécanique des solides et les problèmes électromagnétiques. Développée pour surmonter les limitations des méthodes d'éléments finis classiques, la VEM permet de traiter des géométries complexes et des maillages non structurés sans nécessiter un maillage précis.

Principales caractéristiques :
    - Flexibilité géométrique : La VEM est particulièrement efficace pour les domaines avec des formes irrégulières et des singularités, ce qui la rend idéale pour les applications industrielles.
    - Utilisation d'éléments virtuels : Contrairement aux méthodes traditionnelles, la VEM repose sur des éléments virtuels qui ne nécessitent pas d'intégration numérique dans le domaine réel, mais plutôt dans un domaine de référence, simplifiant ainsi le calcul.
    - Stabilité et précision : La méthode offre une meilleure stabilité numérique et une précision accrue, notamment pour les problèmes de grande déformation et de discontinuïté.
    - Adaptabilité : La VEM s'adapte facilement à différents types de problèmes, y compris ceux avec des conditions aux limites complexes.
    
Cette méthode représente une avancée significative dans le domaine de l'analyse numérique, offrant aux ingénieurs et aux chercheurs un outil puissant pour modéliser des systèmes physiques de manière efficace.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [License](#license)

## Requirements

- Python 3.12.7
- NumPy
- Matplotlib
- Scipy

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/RaphaelGrger/Virtual-element-method.git
```
```bash
cd Virtual-element-method
```

## Usage

To print meshes, execute the following command:

```bash 
python main.py
```

## Functions:
- **`read_meshes.py :`** returns meshes in the good format.
- **`functions.py :`** different functions like boundary, geometry proprieties.
- **`vem.py :`** the vem function, plots and errors.
- **`main.py :`** select a mesh .npz and it returns a solution.
- **`main_convergence.py :`** convergence test of the method.

## Meshes:
Different meshes are given, and we create different meshes.
## License

This project is licensed under the MIT License - see the LICENSE file for details.
