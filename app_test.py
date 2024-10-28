from app import process_query


def test_knows_about_dinosaurs():
    assert (
        process_query("dinosaurs") ==
        "Dinosaurs ruled the Earth 200 million years ago"
    )


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_27_plus_49():
    assert process_query("What is 27 plus 49?") == "76"


def test_largest_72_40_50():
    assert process_query("Which of the following numbers"
                         " is the largest: 72, 40, 50?") == "72"


def test_37_multiply_43():
    assert process_query("What is 37 multiplied by 43?") == "1591"


def test_sqrt_cbrt_2074_2809_64_8_1062_3894_3288():
    assert process_query("Which of the following numbers is both"
                         " a square and a cube: 2074, 2809, 64, 8, 1062, "
                         "3894, 3288?") == "64"
