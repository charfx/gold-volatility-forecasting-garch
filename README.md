# 📈 Prévision de la volatilité de l’or (Gold – GC=F) avec un modèle GARCH

Ce projet a pour objectif de prédire la volatilité journalière future du prix de l’or (GC=F)
à l’aide d’un modèle GARCH(1,1). La volatilité est un élément essentiel en finance :

- Elle influence le risque d’un actif
- Elle affecte le dimensionnement des positions (position sizing)
- Elle aide à déterminer si un marché est calme ou dangereux
- Elle permet à un trader ou un risk manager d’adapter son exposition

Ce projet montre comment utiliser les log-returns pour modéliser la volatilité et obtenir
une prévision fiable sur plusieurs jours.

---

## 🔍 Objectifs du projet

- Télécharger les données du Gold via **yfinance**
- Calculer les **log-returns**
- Ajuster un modèle **GARCH(1,1)** via la librairie **arch**
- Générer une **prévision de la volatilité future** sur plusieurs jours
- Visualiser la volatilité historique et future
- Expliquer les implications pour :
  - les traders  
  - les gestionnaires de risque  
  - les investisseurs  

---

## 🧠 Pourquoi le GARCH ?

Les marchés montrent une propriété de **volatilité en grappes** :  
les périodes calmes et les périodes violentes ont tendance à se regrouper.

Le modèle GARCH :

- capte cette dynamique,
- s’adapte aux log-returns (stationnaires),
- est très utilisé en finance quantitative.

---

## 📊 Résultats principaux

- Le modèle prédit la volatilité future sur les 5 prochains jours.
- La volatilité future peut informer :
  - le **risque** de l’actif,
  - la **taille de position**,
  - la **probabilité de sortir de sa distribution journalière**.

Exemple :  
> Si la volatilité prévue est élevée demain, un trader peut réduire le levier  
> ou un gestionnaire de risque peut ajuster les limites de perte.

---

## 🖼️ Visualisations

Les graphiques suivants sont inclus dans le dossier `images/` :

- **Volatilité quotidienne vs annualisée**
- **Prévision de volatilité future (GARCH)**

---

## 🛠️ Technologies utilisées

- Python  
- pandas  
- numpy  
- matplotlib  
- yfinance  
- arch  

---

## 🚀 Commenter exécuter pour plus d'information d'usage .


