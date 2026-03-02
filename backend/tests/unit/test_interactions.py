"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_includes_interaction_with_different_learner_id():
    interaction = _make_log(id=3, learner_id=2, item_id=1)
    result = _filter_by_item_id([interaction], item_id=1)
    assert len(result) == 1

def test_filter_returns_empty_when_no_matching_item_id() -> None:
    interactions = [_make_log(1, 1, 10), _make_log(2, 2, 20)]
    result = _filter_by_item_id(interactions, 99)
    assert result == []


def test_filter_returns_multiple_matching_interactions() -> None:
    interactions = [_make_log(1, 1, 5), _make_log(2, 2, 5), _make_log(3, 3, 9)]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 2


def test_filter_does_not_return_wrong_item_id() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 2)
    assert all(i.item_id == 2 for i in result)


def test_filter_returns_single_matching_from_many() -> None:
    interactions = [_make_log(i, i, i) for i in range(1, 6)]
    result = _filter_by_item_id(interactions, 3)
    assert len(result) == 1
    assert result[0].item_id == 3

def test_filter_excludes_interaction_with_different_learner_id() -> None:
    interaction = _make_log(id=1, learner_id=1, item_id=2)
    result = _filter_by_item_id([interaction], item_id=1)
    assert len(result) == 0