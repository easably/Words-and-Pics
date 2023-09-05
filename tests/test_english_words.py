from typing import List, Dict, Optional
import pytest
import json


@pytest.fixture(scope="module")
def english_words_data():
    with open("Data/english_words.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def test_json_structure_1(english_words_data: Dict[str, Dict]):
    data = english_words_data

    expected_keys: List[str] = ["a1", "a2", "b1", "b2", "c1", "c2"]
    assert list(data.keys()) == expected_keys

    for key, value in data.items():
        assert isinstance(value, dict)


def test_json_structure_2(english_words_data: Dict[str, Dict]):
    data = english_words_data

    expected_categories: List[str] = [
        "Politics and society",
        "Science and technology",
        "Sport",
        "Natural world",
        "Time and space",
        "Travelling",
        "Work and business",
        "Animals",
        "Appearance",
        "Culture",
        "Food and drink",
        "Health",
        "Homes and buildings",
        "Leisure",
        "People",
    ]

    for level, categories in data.items():
        for category in expected_categories:
            assert (
                category in categories
            ), f"Missing category '{category}' in level '{level}'"
            assert isinstance(categories, dict)


def test_word_data_types(english_words_data: Dict[str, Dict]):
    for level, categories in english_words_data.items():
        for category, words in categories.items():
            for word_data in words:
                assert isinstance(
                    word_data, dict
                ), f"Invalid word data format in level '{level}', category '{category}'. Word - '{word_data['word']}'"

                assert (
                    "word" in word_data
                    and isinstance(word_data["word"], str)
                    and len(word_data["word"]) >= 1
                ), f"Invalid 'word' data type in level '{level}', category '{category}'. Word - '{word_data['word']}'"

                assert (
                    "part_of_speech" in word_data
                    and isinstance(word_data["part_of_speech"], str)
                    and len(word_data["word"]) >= 1
                ), f"Invalid 'part_of_speech' data type in level '{level}', category '{category}'. Word - '{word_data['word']}'"

                assert (
                    "examples" in word_data
                    and isinstance(word_data["examples"], list)
                    and len(word_data["examples"]) > 0
                ), f"Invalid 'examples' data type in level '{level}', category '{category}'. Word - '{word_data['word']}'"

                for i in word_data["examples"]:
                    assert isinstance(i, str)

                assert (
                    "definition" in word_data
                    and isinstance(word_data["definition"], list)
                    and len(word_data["definition"]) > 0
                ), f"Invalid 'definition' data type in level '{level}', category '{category}'. Word - '{word_data['word']}'"

                for i in word_data["definition"]:
                    assert isinstance(i, str)

                phonetics_data: Optional[Dict[str, str]] = word_data.get("phonetics")
                if phonetics_data is not None:
                    assert isinstance(
                        phonetics_data, dict
                    ), f"Invalid 'phonetics' data type in level '{level}', category '{category}'. Word - '{word_data['word']}'"
                    assert "mp3" in phonetics_data and (
                        phonetics_data["mp3"] is None
                        or isinstance(phonetics_data["mp3"], str)
                    ), f"Invalid 'mp3' data type in level '{level}', category '{category}'. Word - '{word_data['word']}'"
                    assert "transcription" in phonetics_data and (
                        phonetics_data["transcription"] is None
                        or isinstance(phonetics_data["transcription"], str)
                    ), f"Invalid 'transcription' data type in level '{level}', category '{category}'. Word - '{word_data['word']}'"

                assert (
                    len(word_data.keys()) == 5
                ), f"Invalid number of keys in word data in level '{level}', category '{category}'. Word - '{word_data['word']}'"


def test_word_data_lowercase(english_words_data: Dict[str, Dict]):
    for level, categories in english_words_data.items():
        for category, words in categories.items():
            for word_data in words:
                assert isinstance(
                    word_data, dict
                ), f"Invalid word data format in level '{level}', category '{category}'"

                for key, value in word_data.items():
                    if isinstance(value, str):
                        assert (
                            value.islower()
                        ), f"Invalid case for '{key}' in level '{level}', category '{category}'. Word - '{word_data['word']}'"

                    if isinstance(value, list):
                        for item in value:
                            assert (
                                item.islower()
                            ), f"Invalid case for '{key}' in level '{level}', category '{category}'. Word - '{word_data['word']}'"

                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if isinstance(sub_value, str):
                                assert (
                                    sub_value.islower()
                                ), f"Invalid case for '{sub_key}' in '{key}' in level '{level}', category '{category}'. Word - '{word_data['word']}'"
