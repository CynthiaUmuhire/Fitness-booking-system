from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from booking.models import FitnessClass, Booking

User = get_user_model()

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="testuser@example.com")   
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga Class",
            description="A relaxing yoga session.",
            instructor=self.user,
            schedule="2025-03-30 10:00:00"
        )
        self.client = Client()

    def test_user_login_view(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("class_list"))
        response = self.client.post(reverse("login"), {"username": "wronguser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid credentials")

    # def test_register_view(self):
    #     response = self.client.post(reverse("register"), {
    #         "username": "newuser",
    #         "password1": "password123",
    #         "password2": "password123",
    #         "email": "newuser@example.com",
    #         'bio': "I am a new user",
    #         'phoneNumber': "0788854672443"
    #         })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse("login"))

    def test_fitness_list_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("class_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yoga Class")
        self.client.logout()
        response = self.client.get(reverse("class_list"))
        self.assertEqual(response.status_code, 302)

    def test_join_class_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("join_class", args=[self.fitness_class.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("join_class", args=[self.fitness_class.id]))
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]), "You have already joined this class.")

    def test_logout_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))