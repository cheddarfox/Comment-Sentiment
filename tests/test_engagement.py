"""Tests for engagement score calculation (no external dependencies)."""

from ai_discussion_analyzer import calculate_engagement_score


def test_engagement_returns_expected_keys():
    result = calculate_engagement_score("I like this product!")
    expected = {"score", "likes", "dislikes", "replies", "questions", "exclamations", "raw_score", "text_length"}
    assert set(result.keys()) == expected


def test_engagement_detects_likes():
    result = calculate_engagement_score("I liked it and she likes it too")
    assert result["likes"] == 2


def test_engagement_detects_dislikes():
    result = calculate_engagement_score("I dislike this and disliked that")
    assert result["dislikes"] == 2


def test_engagement_detects_questions():
    result = calculate_engagement_score("What do you think? Is it good?")
    assert result["questions"] == 2


def test_engagement_detects_exclamations():
    result = calculate_engagement_score("Amazing! Wow! Great!")
    assert result["exclamations"] == 3


def test_engagement_detects_replies():
    result = calculate_engagement_score("She replied to my comment and there are 3 replies")
    assert result["replies"] >= 1


def test_engagement_score_non_negative():
    result = calculate_engagement_score("boring text with nothing special")
    assert result["score"] >= 0


def test_engagement_score_higher_for_active_text():
    low = calculate_engagement_score("nothing happens here")
    high = calculate_engagement_score("I like this! Do you? Great replies!! She liked it too!")
    assert high["score"] > low["score"]


def test_engagement_empty_text():
    result = calculate_engagement_score("")
    assert result["score"] == 0
    assert result["text_length"] == 0


def test_engagement_text_length():
    result = calculate_engagement_score("one two three four five")
    assert result["text_length"] == 5
