import os
import pytest
import json


@pytest.fixture(scope="module")
def english_words_data():
    with open("Data/english_words.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def test_audio_files_exist(english_words_data):
    missing_audio_files = []

    for level, categories in english_words_data.items():
        for category, words in categories.items():
            for word_data in words:
                if word_data["phonetics"]:
                    word_audio_filename = os.path.join(
                        "phonetics", level.upper(), category, f"{word_data['word']}.mp3"
                    )
                    if not os.path.exists(word_audio_filename):
                        missing_audio_files.append(
                            f"Missing audio file for word '{word_data['word']}' in level '{level}', category '{category}'"
                        )

    assert not missing_audio_files, "\n".join(missing_audio_files)
