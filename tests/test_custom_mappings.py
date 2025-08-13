from typing import Dict, List

import pytest
from plexanisync import custom_mappings
from plexanisync.custom_mappings import AnilistCustomMapping
import logging
import tempfile

LOGGER = logging.getLogger(__name__)


def test_file_doesnt_exist(caplog):
    result: Dict[str, List[AnilistCustomMapping]]

    with caplog.at_level(logging.INFO):
        result = custom_mappings.read_custom_mappings("non_existent_file.yaml")
    assert result == {}
    assert "Custom map file not found: non_existent_file.yaml" in caplog.text


def test_broken_yaml_exits(caplog):
    result: Dict[str, List[AnilistCustomMapping]] = {}

    f = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
    f.write("invalid_yaml_content...")

    with caplog.at_level(logging.INFO):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            result = custom_mappings.read_custom_mappings(f.name)

    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 1

    assert result == {}
    assert "Custom Mappings validation failed!" in caplog.text


def test_example_mapping(caplog):
    result: Dict[str, List[AnilistCustomMapping]]

    with caplog.at_level(logging.INFO):
        result = custom_mappings.read_custom_mappings("./custom_mappings.yaml.example")
    print(result.keys())
    re_zero_name = "Re:ZERO -Starting Life in Another World-".lower()
    assert re_zero_name in result

    re_zero: List[AnilistCustomMapping] = result[re_zero_name]
    assert len(re_zero) >= 2
    assert re_zero[0].anime_id == 108632
    assert re_zero[0].start == 1
    assert re_zero[1].anime_id == 119661
    assert re_zero[1].start == 14
