# -*- coding: utf-8 -*-
"""
Prédiction de la volatilité de l'or (GC=F) avec un modèle GARCH(1,1)
Auteur : Charifi saad
Description :
    - Téléchargement des prix de l'or via Yahoo Finance
    - Calcul des log-returns (stationnaires par construction)
    - Estimation d'un modèle GARCH(1,1)
    - Prévision de la volatilité future (5 jours ouvrables)
    - Visualisation de la volatilité passée et prédite
"""

# === Imports ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from arch import arch_model


# =====================================================================
# 1. Téléchargement des données (or : GC=F)
# =====================================================================
gold = yf.download("GC=F", start="2015-01-01")

# Nettoyage des colonnes (MultiIndex -> simple index)
gold.columns = gold.columns.get_level_values(0)

# =====================================================================
# 2. Calcul du rendement logarithmique (stationnaire)
# =====================================================================
gold['log_return'] = np.log(gold['Close'] / gold['Close'].shift(1))
gold.dropna(inplace=True)   # Retirer le premier NA


# =====================================================================
# 3. Visualisation de la volatilité historique (quotidienne et annualisée)
# =====================================================================
gold['vol_daily'] = gold['log_return'].rolling(5).std()
gold['vol_annual'] = gold['vol_daily'] * np.sqrt(252)

plt.figure(figsize=(18, 6))
gold['vol_daily'].plot(label='Volatilité quotidienne', alpha=0.7)
gold['vol_annual'].plot(label='Volatilité annualisée', alpha=0.7)

# Moyenne et niveaux clés
vix_like = gold['vol_annual'].mean()
vix_res = gold['vol_annual'].quantile(0.90)
vix_sup = gold['vol_annual'].quantile(0.10)

plt.axhline(vix_like, color='blue', linestyle='--', label=f'Moyenne VIX maison ~ {vix_like:.2f}')
plt.axhline(vix_res, color='red', linestyle=':', label=f'90e pct ~ {vix_res:.2f}')
plt.axhline(vix_sup, color='green', linestyle=':', label=f'10e pct ~ {vix_sup:.2f}')

plt.title("Volatilité de l'or : quotidienne vs annualisée (GC=F)")
plt.xlabel("Date")
plt.ylabel("Volatilité")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =====================================================================
# 4. Modèle GARCH(1,1) sur les log-returns
# =====================================================================
log_returns_scaled = gold['log_return'] * 100  # Améliore la convergence

model = arch_model(log_returns_scaled, vol='Garch', p=1, q=1)
model_fitted = model.fit(disp='off')

print("\n=== Résumé du modèle GARCH(1,1) ===")
print(model_fitted.summary())


# =====================================================================
# 5. Prévision de la volatilité sur 5 jours ouvrés
# =====================================================================
forecast = model_fitted.forecast(horizon=5)
variance_scaled = forecast.variance.iloc[-1]

# Conversion variance → volatilité réelle
vol_pred = np.sqrt(variance_scaled) / 100     # revenir à l'échelle originale
vol_pred_pct = vol_pred * 100                 # en %

# Création du DataFrame avec les dates futures
last_date = gold.index[-1]
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1),
                             periods=5, freq='B')

df_forecast = pd.DataFrame({
    'Volatilite_Predite_%': vol_pred_pct.values
}, index=future_dates)

print("\n=== Prévisions de volatilité (5 jours ouvrés) ===")
print(df_forecast)


# =====================================================================
# 6. Utilisation (exemple) : intervalle de prix prévu pour demain
# =====================================================================
dernier_prix = gold['Close'].iloc[-1]
vol_jour = vol_pred_pct.iloc[0] / 100

prix_min = dernier_prix * (1 - vol_jour)
prix_max = dernier_prix * (1 + vol_jour)

print(f"\nIntervalle de prix attendu pour demain : [{prix_min:.2f}, {prix_max:.2f}]")


# =====================================================================
# 7. Visualisation : Volatilité observée vs prévisions GARCH
# =====================================================================
plt.figure(figsize=(18, 6))

# Volatilité passée (2025 comme exemple)
vol_obs = gold.loc['2025-01-01':, 'vol_daily']
vol_obs.plot(label="Volatilité observée", color='steelblue')

# Volatilité future prédite
df_forecast['Volatilite_Predite'] = df_forecast['Volatilite_Predite_%'] / 100
df_forecast['Volatilite_Predite'].plot(label="Volatilité prédite (GARCH)", linestyle='--', color='orange')

plt.title("Volatilité observée vs prévisions futures (GARCH)")
plt.xlabel("Date")
plt.ylabel("Volatilité")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
