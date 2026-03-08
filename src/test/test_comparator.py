from src.main.image_compare.comparator import compare_images


def test_compare_images_placeholder():
    # Purpose: keep a minimal unit test to validate compare contract.
    result = compare_images("baseline.png", "candidate.png")
    assert "match" in result
    assert "difference_score" in result
