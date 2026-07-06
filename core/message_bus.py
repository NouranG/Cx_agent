"""
Simple in-memory message bus.

The message bus allows agents to communicate without
knowing about each other directly.
"""

from collections import defaultdict
from typing import Callable, Dict, List


class MessageBus:
    def __init__(self):
        # event_name -> list of callbacks
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event: str, callback: Callable):
        """
        Register a callback for an event.
        """
        self.subscribers[event].append(callback)

    def publish(self, event: str, data=None):
        """
        Publish an event to all subscribers.
        """
        if event not in self.subscribers:
            return

        for callback in self.subscribers[event]:
            callback(data)

    def clear(self):
        """
        Remove all subscribers.
        """
        self.subscribers.clear()