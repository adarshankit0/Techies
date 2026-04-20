from django.core.management.base import BaseCommand
from codetechies.models import Problem
import random


class Command(BaseCommand):
    help = 'Generate high-quality 1000+ problems with structure'

    def handle(self, *args, **kwargs):

        topics = [
            "Arrays", "Strings", "Math", "Loops",
            "Recursion", "Sorting", "Searching",
            "Dynamic Programming", "Graphs", "Greedy"
        ]

        problem_templates = [
            "Find the {object} in a {topic}",
            "Check if a number is {object}",
            "Compute {object} using {topic}",
            "Return the {object} from given input",
            "Determine the {object} efficiently",
            "Calculate the {object} using optimal approach"
        ]

        objects = [
            "sum of elements",
            "maximum value",
            "minimum value",
            "factorial",
            "prime number",
            "palindrome",
            "fibonacci sequence",
            "longest substring",
            "subarray sum",
            "pair combinations"
        ]

        difficulties = ['easy', 'medium', 'hard']

        count = 1000
        created = 0

        for i in range(count):

            topic = random.choice(topics)
            obj = random.choice(objects)
            template = random.choice(problem_templates)

            title = template.format(object=obj, topic=topic)

            description = f"""
Problem:
{title}

Description:
Write a program to {title.lower()}.

Input:
- Input will be provided as per the problem.

Output:
- Return the correct result.

Constraints:
- 1 ≤ n ≤ 10^5

Example:
Input: sample input
Output: sample output

Note:
Try to optimize your solution for better performance.
"""

            difficulty = random.choices(
                difficulties,
                weights=[50, 30, 20],  # more easy, fewer hard
                k=1
            )[0]

            obj, is_created = Problem.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'difficulty': difficulty
                }
            )

            if is_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ {created} problems generated successfully!"
        ))