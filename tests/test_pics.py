import os
from typing import List, Dict, Optional
import pytest
import json


@pytest.fixture(scope="module")
def image_directory_path():
    return "Pics/image(with difinition)"


@pytest.fixture(scope="module")
def english_words_data():
    with open("Data/english_words.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def create_image_structure_dict(
    image_directory_path: str,
) -> Dict[str, Dict[str, List[str]]]:
    image_structure = {}

    for root, dirs, files in os.walk(image_directory_path):
        if root == image_directory_path:
            continue

        level = os.path.basename(root)
        categories = {}

        for category in dirs:
            category_path = os.path.join(root, category)
            image_files = [
                file.lower()
                for file in os.listdir(category_path)
                if file.endswith(".png")
            ]
            categories[category] = image_files

        image_structure[level] = categories

    return image_structure


def test_image_filename_matches_word(
    image_directory_path: str, english_words_data: Dict[str, Dict]
):
    image_structure = create_image_structure_dict(image_directory_path)
    missing_words = []

    for level, categories in english_words_data.items():
        for category, words in categories.items():
            for word_data in words:
                word = word_data["word"].lower()
                word_images = image_structure[level.upper()][category]

                if f"{word}.png" not in word_images:
                    missing_words.append(
                        f"Missing image for word '{word}' in level '{level}', category '{category}'"
                    )

    assert not missing_words, "\n".join(missing_words)


def test_word_image_count_matches(
    image_directory_path: str, english_words_data: Dict[str, Dict]
):
    image_structure = create_image_structure_dict(image_directory_path)
    mismatched_counts = []

    for level, categories in english_words_data.items():
        for category, words in categories.items():
            word_images = image_structure[level.upper()][category]
            num_words = len(words)
            num_images = len(word_images)

            if num_words != num_images:
                mismatched_counts.append(
                    f"Level '{level}', category '{category}': {num_words} words, {num_images} images"
                )

    assert not mismatched_counts, "Mismatched word and image counts:\n" + "\n".join(
        mismatched_counts
    )
