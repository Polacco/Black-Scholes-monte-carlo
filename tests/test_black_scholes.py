"""Tests unitarios para el módulo de Black-Scholes."""

import sys
from pathlib import Path

# Agregar src al path para importaciones
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
import pytest

from black_scholes import (
    call_delta,
    call_price,
    call_rho,
    call_theta,
    d1_d2,
    gamma,
    implied_volatility,
    put_call_parity,
    put_delta,
    put_price,
    put_rho,
    put_theta,
    vega,
)


class TestD1D2:
    def test_basic_values(self):
        d1, d2 = d1_d2(S=100, K=100, T=1.0, r=0.05, sigma=0.2)
        assert d1 == pytest.approx(0.35, abs=0.01)
        assert d2 == pytest.approx(0.15, abs=0.01)

    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            d1_d2(S=100, K=100, T=0, r=0.05, sigma=0.2)
        with pytest.raises(ValueError):
            d1_d2(S=100, K=100, T=1.0, r=0.05, sigma=0)


class TestPrices:
    def test_at_the_money_call(self):
        price = call_price(S=100, K=100, T=1.0, r=0.05, sigma=0.2)
        # Precio aproximado conocido para estos parámetros
        assert price == pytest.approx(10.45, abs=0.05)

    def test_at_the_money_put(self):
        price = put_price(S=100, K=100, T=1.0, r=0.05, sigma=0.2)
        assert price == pytest.approx(5.57, abs=0.05)

    def test_put_call_parity(self):
        S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2
        c = call_price(S, K, T, r, sigma)
        p = put_price(S, K, T, r, sigma)
        assert c - p == pytest.approx(put_call_parity(S, K, T, r), abs=1e-6)

    def test_deep_out_of_the_money(self):
        call = call_price(S=50, K=150, T=0.5, r=0.05, sigma=0.2)
        put = put_price(S=150, K=50, T=0.5, r=0.05, sigma=0.2)
        assert call < 1e-6
        assert put < 1e-6


class TestGreeks:
    def test_call_delta_range(self):
        delta = call_delta(S=100, K=100, T=1.0, r=0.05, sigma=0.2)
        assert 0 < delta < 1

    def test_put_delta_range(self):
        delta = put_delta(S=100, K=100, T=1.0, r=0.05, sigma=0.2)
        assert -1 < delta < 0

    def test_gamma_positive(self):
        g = gamma(S=100, K=100, T=1.0, r=0.05, sigma=0.2)
        assert g > 0

    def test_vega_positive(self):
        v = vega(S=100, K=100, T=1.0, r=0.05, sigma=0.2)
        assert v > 0

    def test_call_put_theta_sign(self):
        # Theta suele ser negativa para opciones compradas
        assert call_theta(S=100, K=100, T=1.0, r=0.05, sigma=0.2) < 0
        assert put_theta(S=100, K=100, T=1.0, r=0.05, sigma=0.2) < 0

    def test_rho_sign(self):
        assert call_rho(S=100, K=100, T=1.0, r=0.05, sigma=0.2) > 0
        assert put_rho(S=100, K=100, T=1.0, r=0.05, sigma=0.2) < 0


class TestImpliedVolatility:
    def test_round_trip_call(self):
        S, K, T, r, sigma_true = 100, 100, 1.0, 0.05, 0.25
        market_price = call_price(S, K, T, r, sigma_true)
        sigma_iv = implied_volatility(market_price, S, K, T, r, option_type="call")
        assert sigma_iv == pytest.approx(sigma_true, abs=1e-6)

    def test_round_trip_put(self):
        S, K, T, r, sigma_true = 100, 100, 1.0, 0.05, 0.25
        market_price = put_price(S, K, T, r, sigma_true)
        sigma_iv = implied_volatility(market_price, S, K, T, r, option_type="put")
        assert sigma_iv == pytest.approx(sigma_true, abs=1e-6)

    def test_invalid_option_type(self):
        with pytest.raises(ValueError):
            implied_volatility(10, 100, 100, 1.0, 0.05, option_type="straddle")
