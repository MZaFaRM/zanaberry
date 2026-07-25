import multiprocessing
import time


def cpu_stress_worker(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        _ = [i**2 for i in range(10000)]


def ram_stress_worker(size_in_mb):
    """Allocates a specific amount of RAM and holds it."""
    try:
        print(f"Allocating {size_in_mb} MB of RAM...")
        # Allocate roughly size_in_mb * 1MB of data (integers)
        chunk = [0] * (size_in_mb * 250000)
        print("RAM allocated. Holding for stress test...")
        # Keep the memory alive by sleeping
        time.sleep(60)
    except MemoryError:
        print("Out of memory! Reduce the RAM allocation size.")


if __name__ == "__main__":
    DURATION = 60  # Duration of the test in seconds
    RAM_ALLOCATION_MB = 4096  # Amount of RAM to allocate (e.g., 4096 MB = 4 GB)

    num_cores = multiprocessing.cpu_count()
    print(
        f"Starting CPU stress test on all {num_cores} cores for {DURATION} seconds..."
    )
    print(f"Starting RAM stress test for {RAM_ALLOCATION_MB} MB...")
    print("Press Ctrl+C to abort at any time.\n")

    ram_process = multiprocessing.Process(
        target=ram_stress_worker, args=(RAM_ALLOCATION_MB,)
    )
    ram_process.start()

    cpu_processes = []
    for _ in range(num_cores):
        p = multiprocessing.Process(target=cpu_stress_worker, args=(DURATION,))
        p.start()
        cpu_processes.append(p)

    try:
        for p in cpu_processes:
            p.join()
    except KeyboardInterrupt:
        print("\nStopping stress test manually...")
        for p in cpu_processes:
            p.terminate()
        ram_process.terminate()

    if ram_process.is_alive():
        ram_process.terminate()

    print("\nStress test completed.")
