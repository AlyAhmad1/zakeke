import traceback
import multiprocessing as mp

from src.utils.common import (
    wait_with_random_delay,
    remove_temp_folders,
)

from src.workflows.fetch_orders import execute_fetch_orders

if __name__ == "__main__":
    try:
        print("Starting Guest...")
        execute_fetch_orders()
        remove_temp_folders()

        # while True:
        #     execute_fetch_orders()
        #     # automation_process = mp.Process(
        #     #     target=execute_fetch_orders,
        #     # )
        #     # automation_process.start()
        #     # automation_process.join()
        #     remove_temp_folders()
        #
        #     # todo add logs.
        #     print("-[")
        #     wait_with_random_delay(10, 20)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        exception_data = traceback.format_exc()
