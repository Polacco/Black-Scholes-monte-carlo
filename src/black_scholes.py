"""Fórmulas analíticas de Black-Scholes para opciones europeas.

Este módulo implementa el precio de opciones call y put europeas,
junto con las principales griegas (delta, gamma, vega, theta, rho).
"""

import numpy as np
from scipy.stats import norm


def d1_d2(S, K, T, r, sigma, q=0.0):
    """Calcula d1 y d2 de Black-Scholes.

    Parámetros
    ----------
    S : float
        Precio spot del subyacente.
    K : float
        Precio de ejercicio (strike).
    T : float
        Tiempo al vencimiento en años.
    r : float
        Tasa libre de riesgo anual (continua).
    sigma : float
        Volatilidad anual.
    q : float, opcional
        Tasa de dividendos continua anual, por defecto 0.0.

    Retorna
    -------
    tuple[float, float]
        Valores (d1, d2).
    """
    T_arr = np.asarray(T)
    sigma_arr = np.asarray(sigma)
    if np.any(T_arr <= 0):
        raise ValueError("T debe ser positivo")
    if np.any(sigma_arr <= 0):
        raise ValueError("sigma debe ser positivo")

    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def call_price(S, K, T, r, sigma, q=0.0):
    """Precio de una call europea por Black-Scholes.

    Parámetros
    ----------
    S, K, T, r, sigma, q : ver d1_d2.

    Retorna
    -------
    float
        Precio de la call.
    """
    d1, d2 = d1_d2(S, K, T, r, sigma, q)
    return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def put_price(S, K, T, r, sigma, q=0.0):
    """Precio de una put europea por Black-Scholes.

    Parámetros
    ----------
    S, K, T, r, sigma, q : ver d1_d2.

    Retorna
    -------
    float
        Precio de la put.
    """
    d1, d2 = d1_d2(S, K, T, r, sigma, q)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)


def call_delta(S, K, T, r, sigma, q=0.0):
    """Delta de una call europea."""
    d1, _ = d1_d2(S, K, T, r, sigma, q)
    return np.exp(-q * T) * norm.cdf(d1)


def put_delta(S, K, T, r, sigma, q=0.0):
    """Delta de una put europea."""
    d1, _ = d1_d2(S, K, T, r, sigma, q)
    return np.exp(-q * T) * (norm.cdf(d1) - 1)


def gamma(S, K, T, r, sigma, q=0.0):
    """Gamma de una opción europea (igual para call y put)."""
    d1, _ = d1_d2(S, K, T, r, sigma, q)
    return np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))


def vega(S, K, T, r, sigma, q=0.0):
    """Vega de una opción europea (igual para call y put).

    Retorna la vega respecto a la volatilidad en puntos porcentuales
    (es decir, derivada respecto a sigma, no a sigma en porcentaje).
    """
    d1, _ = d1_d2(S, K, T, r, sigma, q)
    return S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)


def call_theta(S, K, T, r, sigma, q=0.0):
    """Theta de una call europea (derivada respecto al tiempo en años)."""
    d1, d2 = d1_d2(S, K, T, r, sigma, q)
    term1 = -S * np.exp(-q * T) * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
    term2 = -r * K * np.exp(-r * T) * norm.cdf(d2)
    term3 = q * S * np.exp(-q * T) * norm.cdf(d1)
    return term1 + term2 + term3


def put_theta(S, K, T, r, sigma, q=0.0):
    """Theta de una put europea (derivada respecto al tiempo en años)."""
    d1, d2 = d1_d2(S, K, T, r, sigma, q)
    term1 = -S * np.exp(-q * T) * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
    term2 = r * K * np.exp(-r * T) * norm.cdf(-d2)
    term3 = -q * S * np.exp(-q * T) * norm.cdf(-d1)
    return term1 + term2 + term3


def call_rho(S, K, T, r, sigma, q=0.0):
    """Rho de una call europea (derivada respecto a r)."""
    _, d2 = d1_d2(S, K, T, r, sigma, q)
    return K * T * np.exp(-r * T) * norm.cdf(d2)


def put_rho(S, K, T, r, sigma, q=0.0):
    """Rho de una put europea (derivada respecto a r)."""
    _, d2 = d1_d2(S, K, T, r, sigma, q)
    return -K * T * np.exp(-r * T) * norm.cdf(-d2)


def put_call_parity(S, K, T, r, q=0.0):
    """Relación de paridad put-call.

    Retorna C - P, que debe ser igual a S*exp(-qT) - K*exp(-rT).
    """
    return S * np.exp(-q * T) - K * np.exp(-r * T)


def implied_volatility(target_price, S, K, T, r, q=0.0, option_type="call", tol=1e-8, max_iter=100):
    """Calcula la volatilidad implícita con el método de Newton-Raphson.

    Parámetros
    ----------
    target_price : float
        Precio de mercado de la opción.
    S, K, T, r, q : ver d1_d2.
    option_type : str, opcional
        "call" o "put", por defecto "call".
    tol : float, opcional
        Tolerancia de convergencia.
    max_iter : int, opcional
        Número máximo de iteraciones.

    Retorna
    -------
    float
        Volatilidad implícita estimada.

    Lanza
    -----
    ValueError
        Si no converge o el tipo de opción no es válido.
    """
    if option_type not in ("call", "put"):
        raise ValueError("option_type debe ser 'call' o 'put'")

    price_fn = call_price if option_type == "call" else put_price
    sigma = 0.2  # semilla inicial

    for _ in range(max_iter):
        price = price_fn(S, K, T, r, sigma, q)
        diff = target_price - price
        v = vega(S, K, T, r, sigma, q)

        if abs(diff) < tol:
            return sigma
        if abs(v) < 1e-12:
            raise ValueError("Vega demasiado pequeña; no se puede continuar")

        sigma = sigma + diff / v
        if sigma <= 0:
            sigma = 1e-6

    raise ValueError("No convergió en el número máximo de iteraciones")
