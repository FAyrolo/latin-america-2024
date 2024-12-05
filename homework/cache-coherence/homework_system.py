import argparse

from components.boards import HWX86Board
from components.cache_hierarchies import HWMESITwoLevelCacheHierarchy
from components.memories import HWDDR4
from components.processors import HWO3CPU
# from components.network import

from gem5.simulate.simulator import Simulator
from workloads.roi_manager import exit_event_handler

from workloads.array_sum_workload import NaiveArraySumWorkload
from workloads.array_sum_workload import ChunkingArraySumWorkload
from workloads.array_sum_workload import NoResultRaceArraySumWorkload
from workloads.array_sum_workload import ChunkingNoResultRaceArraySumWorkload
from workloads.array_sum_workload import NoCacheBlockRaceArraySumWorkload
from workloads.array_sum_workload import ChunkingNoBlockRaceArraySumWorkload

#clkFrecuency = 3GHz

parser = argparse.ArgumentParser()
parser.add_argument("workload", type=str)
parser.add_argument("numCores", type=int)
parser.add_argument("latency", type=int)
args = parser.parse_args()

# cambiar aqui los parametros de workloads
def workload_parser(name: str):
    arr_length = 32768
    num_threads = args.numCores

    if (name == "1"):
        workload = NaiveArraySumWorkload(arr_length, num_threads)

    elif(name == "2"):
        workload = ChunkingArraySumWorkload(arr_length, num_threads)

    elif(name == "3"):
        workload = NoResultRaceArraySumWorkload(arr_length, num_threads)

    elif(name == "4"):
        workload = ChunkingNoResultRaceArraySumWorkload(arr_length, num_threads)

    elif(name == "5"):
        workload = NoCacheBlockRaceArraySumWorkload(arr_length, num_threads)

    else:
        workload = ChunkingNoBlockRaceArraySumWorkload(arr_length, num_threads)

    return workload

proc = HWO3CPU(
        num_cores= args.numCores,
    )

memory = HWDDR4()

cache_hierarchy = HWMESITwoLevelCacheHierarchy(
        xbar_latency = args.latency,
    )

board = HWX86Board(
        clk_freq= "3GHz",
        processor=proc,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )

board.set_workload(workload= workload_parser(args.workload))

sim = Simulator(board)
sim.run()
