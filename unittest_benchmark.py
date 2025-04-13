import time
from typing import Callable, Any
from scipy.stats import mannwhitneyu
import unittest


class BenchmarkMixin:
    @staticmethod
    def _timeit(callable):
        start = time.perf_counter()
        callable()
        end = time.perf_counter()
        return end - start
    
    def assertIsFaster(self, faster: Callable[[], Any], benchmark: Callable[[], Any], samples: int = 20, p_value: float = 0.001, msg: Any = None) -> None:

        faster_samples = [self._timeit(faster) for _ in range(samples)]
        benchmark_samples = [self._timeit(benchmark) for _ in range(samples)]

        result = mannwhitneyu(faster_samples, benchmark_samples, alternative="less")
        test_p_value = result.pvalue

        if test_p_value >= p_value:
            standardMsg = (
                f"{unittest.util.safe_repr(faster)} is not "
                f"significantly faster than {unittest.util.safe_repr(benchmark)}"
            )
            msg = self._formatMessage(msg, standardMsg)
            raise self.failureException(msg)