from util.get_progress import get_progress


progress = get_progress()


def test():
    progress.save_start_time()

    print("This is a test")

    progress.save_end_time()
