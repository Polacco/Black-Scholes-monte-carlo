"""Utilidades de simulación de Monte Carlo para pricing de opciones.

Incluye la generación de trayectorias de precios bajo el modelo de
Black-Scholes (movimiento browniano geométrico) y el pricing de opciones
por Monte Carlo.
"""

import numpy as np


def simulate_gbm(S0, r, sigma, T, n_steps, n_paths, q=0.0, random_state=None):
    """Simula trayectorias de un movimiento browniano geométrico.

    Parámetros
    ----------
    S0 : float
        Precio inicial del subyacente.
    r : float
        Tasa libre de riesgo anual (continua).
    sigma : float
        Volatilidad anual.
    T : float
        Horizonte temporal en años.
    n_steps : int
        Número de pasos temporales por trayectoria.
    n_paths : int
        Número de trayectorias a simular.
    q : float, opcional
        Tasa de dividendos continua anual, por defecto 0.0.
    random_state : int o None
        Semilla para reproducibilidad.

    Retorna
    -------
    np.ndarray
        Matriz de forma (n_paths, n_steps + 1) con los precios simulados.
        La primera columna contiene S0.
    """
    rng = np.random.default_rng(random_state)
    dt = T / n_steps
    Z = rng.standard_normal(size=(n_paths, n_steps))

    # Rendimientos logarítmicos
    log_returns = (r - q - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z

    # Construimos precios acumulando log-returns
    log_prices = np.zeros((n_paths, n_steps + 1))
    log_prices[:, 0] = np.log(S0)
    log_prices[:, 1:] = np.log(S0) + np.cumsum(log_returns, axis=1)

    return np.exp(log_prices)


def mc_call_price(S0, K, T, r, sigma, n_paths=100_000, n_steps=1, q=0.0, random_state=None):
    """Precio de una call europea por Monte Carlo.

    Parámetros
    ----------
    S0, K, T, r, sigma, q : ver simulate_gbm.
    n_paths : int, opcional
        Número de trayectorias, por defecto 100_000.
    n_steps : int, opcional
        Pasos temporales, por defecto 1 (solo se necesita el valor final).
    random_state : int o None, opcional
        Semilla para reproducibilidad.

    Retorna
    -------
    tuple[float, float]
        (precio estimado, error estándar de la estimación).
    """
    paths = simulate_gbm(S0, r, sigma, T, n_steps, n_paths, q, random_state)
    payoffs = np.maximum(paths[:, -1] - K, 0)
    discounted = np.exp(-r * T) * payoffs
    price = np.mean(discounted)
    se = np.std(discounted, ddof=1) / np.sqrt(n_paths)
    return price, se


def mc_put_price(S0, K, T, r, sigma, n_paths=100_000, n_steps=1, q=0.0, random_state=None):
    """Precio de una put europea por Monte Carlo.

    Parámetros y retorno: ver mc_call_price.
    """
    paths = simulate_gbm(S0, r, sigma, T, n_steps, n_paths, q, random_state)
    payoffs = np.maximum(K - paths[:, -1], 0)
    discounted = np.exp(-r * T) * payoffs
    price = np.mean(discounted)
    se = np.std(discounted, ddof=1) / np.sqrt(n_paths)
    return price, se
