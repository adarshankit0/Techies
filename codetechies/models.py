from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# ================= PROBLEM =================
class Problem(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy'
    )

    expected_output = models.TextField(blank=True, null=True)
    points = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.title} ({self.difficulty})"


# ================= TEST CASE =================
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return f"{self.problem.title} TestCase"


# ================= SUBMISSION =================
class Submission(models.Model):
    STATUS_CHOICES = (
        ('attempted', 'Attempted'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    code = models.TextField()
    output = models.TextField(blank=True, null=True)

    score = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='attempted'
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.problem} - {self.status}"


# ================= LEADERBOARD =================
class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.total_score}"


# ================= CERTIFICATE =================
class Certificate(models.Model):
    CERT_TYPES = (
        ('participation', 'Participation'),
        ('completion', 'Completion'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    cert_type = models.CharField(max_length=20, choices=CERT_TYPES)
    title = models.CharField(max_length=200)

    issued_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.problem} - {self.cert_type}"