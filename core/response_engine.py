"""
Standard response format for all support agents.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AgentResponse:
    """
    Standard response object returned by every agent.
    """

    success: bool
    agent: str
    message: str
    confidence: float = 1.0
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "success": self.success,
            "agent": self.agent,
            "message": self.message,
            "confidence": self.confidence,
            "data": self.data,
        }


class ResponseEngine:
    """
    Factory methods for standardized responses.
    """

    @staticmethod
    def success(agent: str,
                message: str,
                confidence: float = 1.0,
                data: Dict[str, Any] | None = None):

        return AgentResponse(
            success=True,
            agent=agent,
            message=message,
            confidence=confidence,
            data=data or {},
        )

    @staticmethod
    def failure(agent: str,
                message: str,
                confidence: float = 0.0,
                data: Dict[str, Any] | None = None):

        return AgentResponse(
            success=False,
            agent=agent,
            message=message,
            confidence=confidence,
            data=data or {},
        )