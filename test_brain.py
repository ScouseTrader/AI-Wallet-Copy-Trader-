import unittest
from brain import Brain


class TestBrain(unittest.TestCase):
    def setUp(self):
        self.brain = Brain()

    def test_mock_scoring(self):
        # Test that scoring is deterministic and within range
        wallet = "0x1234567890abcdef"
        score = self.brain._calculate_mock_score(wallet)
        self.assertTrue(0 <= score <= 100)

        # Ensure same wallet gets same score
        score2 = self.brain._calculate_mock_score(wallet)
        self.assertEqual(score, score2)

    def test_sorting(self):
        # Create dummy wallets with known mock scores
        # We know the mock score function: sum(ord(c)) % 100
        # Let's just trust the sort logic

        wallets = ["0xAAA", "0xBBB", "0xCCC"]
        ranked = self.brain.score_wallets(wallets)

        self.assertEqual(len(ranked), 3)
        # Check if sorted descending by score
        scores = [w["score"] for w in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main()
