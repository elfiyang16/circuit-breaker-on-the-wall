import abc
from enum import Enum


class Circuit_Breaker():
    """
    A Microservices pattern that prevent upstream failures flushing down the downstream,
    and causing cascading failures.
    This is done through a stateful proxy (with a counter) that monitors the number of failures,
    and implements retries in a carefully designed manner.
    """
    class State(Enum):
        CLOSED = 1
        OPEND = 2
        HALF_OPEN = 3

    THRESHOLD = 5
    TIMEOUT = 30
    state = State.CLOSED

    def __init__(self, counter_limit=THRESHOLD, timeout=TIMEOUT, **kwargs):
        self.counter_limit = counter_limit
        self.timout = timeout

    @abc.abstractmethod
    def ops_wrapper(self, **kwargs):
        """
        wraps the protected operation in this method
        """
        pass

    @ abc.abstractmethod
    def closed(self):
        """
        allow the request to go through to the application, while
        the proxy maintains the number of failed attempts.
        When the counter exceeds a threshold, it will close the connection
        """
        pass

    @ abc.abstractmethod
    def open(self):
        """
        requests  will fail immediately, and an exception will be returned.
        However, after a timeout, the Circuit Breaker will go to the “Half-Open” state.
        """
        pass

    @ abc.abstractmethod
    def open(self):
        """
        allows only a limited number of requests to pass through and invoke the operation.
        If these requests are successful, the circuit breaker will go back to the “Closed” state and reset the counter.
        However, if any request fails, it goes to the “Open” state and restart the timeout.
        This is helpful to prevent the in-recovery service been flooded with upcoming requests again, which can lead to failures once more.
        """
        pass
