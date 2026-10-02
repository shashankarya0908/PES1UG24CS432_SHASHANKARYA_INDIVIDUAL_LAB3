import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "5-Github_Copilot_Generated_Code"),
)

from vote_service import VoteService


class VoteServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = VoteService(lambda voter_ref: voter_ref.startswith("verified-"))

    def test_accepts_first_vote_and_rejects_duplicate_for_same_project(self) -> None:
        self.assertEqual(self.service.cast_vote("verified-a", "project-1"), "accepted")
        self.assertEqual(
            self.service.cast_vote("verified-a", "project-1"), "already_voted"
        )
        self.assertEqual(self.service.leaderboard(), [("project-1", 1)])

    def test_same_voter_can_vote_once_on_another_project(self) -> None:
        self.service.cast_vote("verified-a", "project-1")
        self.assertEqual(self.service.cast_vote("verified-a", "project-2"), "accepted")

    def test_unverified_voter_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "not verified"):
            self.service.cast_vote("unverified-a", "project-1")
        self.assertEqual(self.service.leaderboard(), [])

    def test_leaderboard_sorts_by_votes_then_project_id(self) -> None:
        self.service.cast_vote("verified-a", "project-b")
        self.service.cast_vote("verified-a", "project-a")
        self.service.cast_vote("verified-b", "project-a")
        self.assertEqual(
            self.service.leaderboard(), [("project-a", 2), ("project-b", 1)]
        )


if __name__ == "__main__":
    unittest.main()