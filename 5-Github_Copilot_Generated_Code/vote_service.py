"""Illustrative in-memory voting logic; not a production voting service."""

from __future__ import annotations

from threading import Lock
from typing import Callable, Literal

VoteStatus = Literal["accepted", "already_voted"]


class VoteService:
    """Accept one vote per verified voter and project for this process lifetime."""

    def __init__(self, is_verified_voter: Callable[[str], bool]) -> None:
        self._is_verified_voter = is_verified_voter
        self._votes: set[tuple[str, str]] = set()
        self._counts: dict[str, int] = {}
        self._lock = Lock()

    def cast_vote(self, voter_ref: str, project_id: str) -> VoteStatus:
        if not voter_ref or not project_id:
            raise ValueError("voter_ref and project_id are required")
        if not self._is_verified_voter(voter_ref):
            raise ValueError("voter identity is not verified")

        key = (voter_ref, project_id)
        with self._lock:
            if key in self._votes:
                return "already_voted"
            self._votes.add(key)
            self._counts[project_id] = self._counts.get(project_id, 0) + 1
            return "accepted"

    def leaderboard(self) -> list[tuple[str, int]]:
        with self._lock:
            return sorted(self._counts.items(), key=lambda item: (-item[1], item[0]))