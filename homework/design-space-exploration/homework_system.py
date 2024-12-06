import argparse
from typing import List

from gem5.components.boards.simple_board import SimpleBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
import gem5.utils.multisim as multisim

#Components from the course
from my_processor import BigProcessor, LittleProcessor
from three_level import PrivateL1PrivateL2SharedL3CacheHierarchy
from gem5.components.memory.multi_channel import ChanneledMemory #needed for ddr5 next
from gem5.components.memory.dram_interfaces.lpddr5 import LPDDR5_6400_1x16_BG_BL32

#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--cpu-type",
    type=str,
    choices=["Big", "Little"],
    required=True,
    help="Type of CPU to use for the simulation",
)
args = parser.parse_args()



##### PROCESSOR
# I prefer to parameterize the CPU type and request it when running the simulation
# instead of for p in [Big, Little] to handle output directories better
if args.cpu_type == "Big":
    processor = BigProcessor()
elif args.cpu_type == "Little":
    processor = LittleProcessor()
else:
    raise ValueError(f"Unknown CPU type: {args.cpu_type}")

##### MEMORY
memory = ChanneledMemory(LPDDR5_6400_1x16_BG_BL32, 4, 64)

##### CACHE HIERARCHY
cache_hierarchy = PrivateL1PrivateL2SharedL3CacheHierarchy(
            l1d_size="32KiB",
            l1i_size="32KiB",
            l2_size="256KiB",
            l3_size="2MiB",
)

# Maybe take in as sim argument
#bench_count = 2
#multisim.set_num_processes(bench_count)
#
#for benchmark in list(obtain_resource("riscv-getting-started-benchmark-suite"))[0:bench_count]:
#    board = SimpleBoard(
#        clk_freq="3GHz",
#        processor=processor,
#        memory=memory,
#        cache_hierarchy=cache_hierarchy,
#    )
#    board.set_workload(benchmark)
#    simulator = Simulator(
#        board=board, id=f"{processor_type.get_name()}-{benchmark.get_id()}"
#    )
#    multisim.add_simulator(simulator)


board = SimpleBoard(
        clk_freq="3GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )

#workload = obtain_resource("riscv-getting-started-benchmark-suite")
workload = list(obtain_resource("riscv-getting-started-benchmark-suite"))[-1]
board.set_workload(workload)
simulator = Simulator(board=board)
simulator.run()
