import argparse
from gem5.components.boards.test_board import TestBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.simple import SingleChannelSimpleMemory
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.memory.multi_channel import ChanneledMemory
from gem5.components.memory.dram_interfaces.lpddr5 import LPDDR5_6400_1x16_BG_BL32
from gem5.components.processors.linear_generator import LinearGenerator
from gem5.components.processors.random_generator import RandomGenerator
from gem5.simulate.simulator import Simulator
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy

parser = argparse.ArgumentParser()
parser.add_argument("l1_size", type=str)#, help="The rate of the generator")
parser.add_argument("l2_size", type=str)#, help="The read percentage of the generator")
parser.add_argument("stress_target", type=str)
args = parser.parse_args()

board = TestBoard(
    clk_freq="3GHz",
    generator=RandomGenerator(num_cores=1, max_addr=2**18,#(args.l1_size, args.l2_size)[args.stress_target == "L2"],
                              rate="16GiB/s", rd_perc=100),
                              #rate=args.rate, rd_perc=args.read_percent),
    cache_hierarchy=PrivateL1PrivateL2CacheHierarchy(
        l1d_size=args.l1_size,#"32KiB",
        l1i_size=args.l1_size,#"32KiB",
        l2_size=args.l2_size,#"256KiB",
        #l1d_size="32KiB",
        #l1i_size="32KiB",
        #l2_size="256KiB",
    ),
    #memory=SingleChannelSimpleMemory(latency="20ns", bandwidth="32GiB/s", latency_var="0s", size="1GiB"),
    #memory=SingleChannelDDR4_2400(),
    #memory=ChanneledMemory(LPDDR5_6400_1x16_BG_BL32, 4, 64),
    memory=DualChannelDDR4_2400(size="1GiB"),
    #cache_hierarchy=NoCache(),
)

simulator = Simulator(board=board)
simulator.run()

stats = simulator.get_simstats()
seconds = stats.simTicks.value / stats.simFreq.value
total_bytes = (
    stats.board.processor.cores[0].generator.bytesRead.value
    + stats.board.processor.cores[0].generator.bytesWritten.value
)
latency = (
    stats.board.processor.cores[0].generator.totalReadLatency.value
    / stats.board.processor.cores[0].generator.totalReads.value
)

print(f"MEM: DualChannelLDDR4_2400, cache: L1={args.l1_size}, L2={args.l2_size}, stress_target={args.stress_target}")
print(f"Total bandwidth: {total_bytes / seconds / 2**30:0.2f} GiB/s")
print(f"Average latency: {latency / stats.simFreq.value * 1e9:0.2f} ns")

