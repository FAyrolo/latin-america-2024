from typing import List

from ...utils.override import overrides
from ..boards.abstract_board import AbstractBoard
from ..boards.mem_mode import MemMode
from .abstract_generator import AbstractGenerator
from .random_generator_core import RandomGeneratorCore


class RandomGenerator(AbstractGenerator):
    def __init__(
        self,
        num_cores: int = 1,
        duration: str = "1ms",
        rate: str = "100GB/s",
        block_size: int = 64,
        min_addr: int = 0,
        max_addr: int = 32768,
        rd_perc: int = 100,
        data_limit: int = 0,
    ) -> None:
        super().__init__(
            cores=self._create_cores(
                num_cores=num_cores,
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=min_addr,
                max_addr=max_addr,
                rd_perc=rd_perc,
                data_limit=data_limit,
            )
        )
        """The random generator

        This class defines an external interface to create a list of random
        generator cores that could replace the processing cores in a board.

        :param num_cores: The number of linear generator cores to create.
        :param duration: The number of ticks for the generator to generate
                         traffic.
        :param rate: The rate at which the synthetic data is read/written.
        :param block_size: The number of bytes to be read/written with each
                           request.
        :param min_addr: The lower bound of the address range the generator
                         will read/write from/to.
        :param max_addr: The upper bound of the address range the generator
                         will read/write from/to.
        :param rd_perc: The percentage of read requests among all the generated
                        requests. The write percentage would be equal to
                        ``100 - rd_perc``.
        :param data_limit: The amount of data in bytes to read/write by the
                           generator before stopping generation.
        """

    def _create_cores(
        self,
        num_cores: int,
        duration: str,
        rate: str,
        block_size: int,
        min_addr: int,
        max_addr: int,
        rd_perc: int,
        data_limit: int,
    ) -> List[RandomGeneratorCore]:
        """
        The helper function to create the cores for the generator, it will use
        the same inputs as the constructor function.
        """
        return [
            RandomGeneratorCore(
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=min_addr,
                max_addr=max_addr,
                rd_perc=rd_perc,
                data_limit=data_limit,
            )
            for _ in range(num_cores)
        ]

    @overrides(AbstractGenerator)
    def start_traffic(self) -> None:
        """
        This function will start the assigned traffic to this generator.
        """
        for core in self.cores:
            core.start_traffic()
