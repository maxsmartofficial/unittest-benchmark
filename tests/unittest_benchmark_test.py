from unittest_benchmark import BenchmarkMixin
import unittest
import time


def slow_function():
    time.sleep(0.001)


def fast_function():
    time.sleep(0.0001)


class MockMostlyFastCounter:
    def __init__(self):
        self.counter = 0

    def call(self):
        self.counter += 1
        if self.counter % 5 == 0:
            time.sleep(0.0015)
        else:
            time.sleep(0.0001)


class BenchmarkTest(unittest.TestCase):
    def setUp(self):
        class MockTestCase(unittest.TestCase, BenchmarkMixin):
            pass

        self.mock_test_case = MockTestCase()
        self.mostly_fast_callable = MockMostlyFastCounter().call

        return super().setUp()

    def test_is_faster_succeeds(self):
        try:
            self.mock_test_case.assertIsFaster(fast_function, slow_function)
        except self.mock_test_case.failureException:
            self.fail("The faster function was not identified by the test")

    def test_is_faster_fails(self):
        with self.assertRaises(self.mock_test_case.failureException):
            self.mock_test_case.assertIsFaster(fast_function, fast_function)

    def test_strict_p_value_fails(self):
        with self.assertRaises(self.mock_test_case.failureException):
            self.mock_test_case.assertIsFaster(
                self.mostly_fast_callable, fast_function, p_value=0.0001
            )

    def test_lenient_p_value_succeeds(self):
        try:
            self.mock_test_case.assertIsFaster(
                self.mostly_fast_callable, slow_function, p_value=0.1
            )
        except self.mock_test_case.failureException:
            self.fail(
                "The faster function was not identified despite the lenient p-value"
            )

    def test_more_samples_succeeds(self):
        try:
            self.mock_test_case.assertIsFaster(
                self.mostly_fast_callable, slow_function, p_value=0.0001, samples=100
            )
        except self.mock_test_case.failureException:
            self.fail("The faster function was not identified despite more samples")


if __name__ == "__main__":
    unittest.main()
