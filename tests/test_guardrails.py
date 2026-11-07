"""Tests: guardrails — secrets and personal numbers never go onward."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nyayavault.guardrails import guard_question


class TestGuardrails(unittest.TestCase):
    def test_normal_question_passes(self) -> None:
        self.assertIsNone(guard_question("Someone stole my password — what does the law say?"))

    def test_empty_question_refused(self) -> None:
        self.assertIsNotNone(guard_question("   "))

    def test_overlong_question_refused(self) -> None:
        self.assertIsNotNone(guard_question("x" * 801))

    def test_aws_key_refused(self) -> None:
        self.assertIsNotNone(guard_question("my key is AKIAIOSFODNN7EXAMPLE please help"))

    def test_github_token_refused(self) -> None:
        self.assertIsNotNone(guard_question("token ghp_abcdefghij1234567890abcd"))

    def test_password_assignment_refused(self) -> None:
        self.assertIsNotNone(guard_question("password: hunter2hunter2"))

    def test_card_number_refused(self) -> None:
        self.assertIsNotNone(guard_question("my card 4111 1111 1111 1111 was used"))

    def test_twelve_digit_number_refused(self) -> None:
        self.assertIsNotNone(guard_question("my number is 123456789012 please check"))

    def test_private_key_refused(self) -> None:
        self.assertIsNotNone(guard_question("-----BEGIN PRIVATE KEY-----\nabc"))


if __name__ == "__main__":
    unittest.main()
