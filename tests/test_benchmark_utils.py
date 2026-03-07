"""Tests for sentiment benchmark utility functions."""

from sentiment_benchmark import interpret_sentiment, sentiment_to_score, compare_sentiments


def test_interpret_very_negative():
    assert interpret_sentiment(0.3) == "Very Negative"


def test_interpret_negative():
    assert interpret_sentiment(1.0) == "Negative"


def test_interpret_neutral():
    assert interpret_sentiment(2.0) == "Neutral"


def test_interpret_positive():
    assert interpret_sentiment(3.0) == "Positive"


def test_interpret_very_positive():
    assert interpret_sentiment(4.5) == "Very Positive"


def test_interpret_boundaries():
    assert interpret_sentiment(0.5) == "Very Negative"
    assert interpret_sentiment(1.5) == "Negative"
    assert interpret_sentiment(2.5) == "Neutral"
    assert interpret_sentiment(3.5) == "Positive"


def test_sentiment_to_score_mapping():
    assert sentiment_to_score("Very Negative") == 0
    assert sentiment_to_score("Negative") == 1
    assert sentiment_to_score("Neutral") == 2
    assert sentiment_to_score("Positive") == 3
    assert sentiment_to_score("Very Positive") == 4


def test_sentiment_to_score_unknown():
    assert sentiment_to_score("Unknown") == 2  # defaults to Neutral


def test_compare_exact_match():
    assert compare_sentiments("Positive", 3.0) is True


def test_compare_off_by_one():
    assert compare_sentiments("Positive", 2.1) is True  # within 1 level


def test_compare_too_far():
    assert compare_sentiments("Very Positive", 0.3) is False
