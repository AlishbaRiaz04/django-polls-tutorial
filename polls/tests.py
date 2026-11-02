import datetime

from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_old_question_is_not_recent(self):
        old_date = timezone.now() - datetime.timedelta(days=2)

        question = Question(
            question_text="Old question",
            pub_date=old_date,
        )

        self.assertFalse(question.was_published_recently())

    def test_future_question_is_not_recent(self):
        future_date = timezone.now() + datetime.timedelta(hours=1)

        question = Question(
            question_text="Future question",
            pub_date=future_date,
        )

        self.assertFalse(question.was_published_recently())

    def test_recent_question_is_recent(self):
        old_date = timezone.now() - datetime.timedelta(hours=2)
        question = Question(question_text="old question", pub_date=old_date)

        self.assertTrue(question.was_published_recently())

    @patch("polls.models.timezone.now")
    def test_question_published_one_day_before_is_recent(self, mock_now):
        now = datetime.datetime(2026, 10, 21, 0, tzinfo=datetime.timezone.utc)
        mock_now.return_value = now

        question = Question(
            question_text="question one day before",
            pub_date=now - datetime.timedelta(days=1),
        )

        self.assertTrue(question.was_published_recently())


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get("/polls/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_five_most_recent_questions(self):
        for i in range(1, 8):
            question = Question.objects.create(
                question_text=f"Question {i}",
                pub_date=timezone.now() - datetime.timedelta(days=i),
            )
            question.choice_set.create(choice_text="A choice")

        response = self.client.get("/polls/")

        question_texts = [
            question.question_text
            for question in response.context["latest_question_list"]
        ]

        expected_question_texts = [
            "Question 1",
            "Question 2",
            "Question 3",
            "Question 4",
            "Question 5",
        ]

        self.assertEqual(question_texts, expected_question_texts)

    def test_future_question(self):
        future_date = timezone.now() + datetime.timedelta(days=1)

        Question.objects.create(
            question_text="Future question",
            pub_date=future_date,
        )
        response = self.client.get("/polls/")

        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

    def test_questions_without_choices_are_excluded(self):
        question_without_choices = Question.objects.create(
            question_text="No choices",
            pub_date=timezone.now() - datetime.timedelta(days=2),
        )

        question_with_choices = Question.objects.create(
            question_text="Has choices",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )
        question_with_choices.choice_set.create(choice_text="Python")
        question_with_choices.choice_set.create(choice_text="Django")

        response = self.client.get(reverse("polls:index"))

        question_ids = [
            question.id for question in response.context["latest_question_list"]
        ]

        self.assertNotIn(question_without_choices.id, question_ids)
        self.assertEqual(question_ids.count(question_with_choices.id), 1)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=1),
        )

        response = self.client.get(reverse("polls:detail", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = Question.objects.create(
            question_text="Past question",
            pub_date=timezone.now() - datetime.timedelta(days=5),
        )
        past_question.choice_set.create(choice_text="Python")

        response = self.client.get(reverse("polls:detail", args=(past_question.id,)))

        self.assertContains(response, past_question.question_text)

    def test_question_without_choices_returns_404(self):
        question = Question.objects.create(
            question_text="No choices",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )

        response = self.client.get(reverse("polls:detail", args=(question.id,)))

        self.assertEqual(response.status_code, 404)

class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        future_question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=1),
        )
        response = self.client.get(reverse("polls:results", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = Question.objects.create(
            question_text="Past question",
            pub_date=timezone.now() - datetime.timedelta(days=5),
        )
        past_question.choice_set.create(choice_text="Python")

        response = self.client.get(reverse("polls:results", args=(past_question.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

    def test_question_without_choices_returns_404(self):
        question = Question.objects.create(
            question_text="No choices",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )

        response = self.client.get(reverse("polls:results", args=(question.id,)))

        self.assertEqual(response.status_code, 404)

class VoteViewTests(TestCase):
    def test_future_question_cannot_be_voted_on(self):
        future_question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=3),
        )
        choice = future_question.choice_set.create(
            choice_text="A future choice",
        )

        response = self.client.post(
            reverse("polls:vote", args=(future_question.id,)),
        )
        self.assertEqual(response.status_code, 404)
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 0)

    def test_non_numeric_choice_id_does_not_crash(self):
        question = Question.objects.create(
            question_text="Test question",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )
        question.choice_set.create(choice_text="Python")
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)), {"choice": "abc"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You didn&#x27;t select a choice.")

    def test_successful_vote_increment_count(self):
        question = Question.objects.create(
            question_text="Test voting",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )
        choice = question.choice_set.create(
            choice_text="Python",
        )
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {"choice": choice.id},
        )
        self.assertRedirects(
            response,
            reverse("polls:results", args=(question.id,)),
        )
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_get_request_does_not_record_vote(self):
        question = Question.objects.create(
            question_text="Test GET request.",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )
        choice = question.choice_set.create(
            choice_text="Python",
        )
        response = self.client.get(
            reverse("polls:vote", args=(question.id,)),
        )

        self.assertEqual(response.status_code, 405)
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 0)
