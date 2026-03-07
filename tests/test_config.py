"""Tests for configuration module."""

import config


def test_config_has_required_attrs():
    assert hasattr(config, "AI_PROVIDER")
    assert hasattr(config, "MAX_TOKENS")
    assert hasattr(config, "TEMPERATURE")
    assert hasattr(config, "OPENAI_MODEL")
    assert hasattr(config, "ANTHROPIC_MODEL")
    assert hasattr(config, "STANFORD_CORENLP_PATH")


def test_temperature_in_range():
    assert 0.0 <= config.TEMPERATURE <= 2.0


def test_max_tokens_positive():
    assert config.MAX_TOKENS > 0


def test_ai_provider_valid():
    assert config.AI_PROVIDER.lower() in ("openai", "anthropic")
