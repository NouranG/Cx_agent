"""
Standard request model used across the application.
"""

from dataclasses import dataclass


@dataclass
class SupportRequest:
    customer_id: int
    message: str