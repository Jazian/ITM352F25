def determine_progress1(hits, spins):
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins

    if hits_spins_ratio > 0:
        progress = "On your way!"
        if hits_spins_ratio >= 0.25:
            progress = "Almost there!"
            if hits_spins_ratio >= 0.5:
                if hits < spins:
                    progress = "You win!"
    else:
        progress = "Get going!"

    return progress

def test_determine_progress(progress_function):
    assert progress_function(10, 0) == "Get going!", "Test case 1 fails"
    assert progress_function(1, 4) == "Almost there!", "Test case 2 fails"
    assert progress_function(2, 5) == "Almost there!", "Test case 3 fails"
    assert progress_function(5, 8) == "You win!", "Test case 4 fails"
    assert progress_function(4, 7) == "You win!", "Test case 5 fails"
    assert progress_function(3, 7) == "On your way!", "Test case 6 fails"

test_determine_progress(determine_progress1)
