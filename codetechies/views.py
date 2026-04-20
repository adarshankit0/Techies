from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q, Max
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse

import os
import requests
from datetime import datetime
from io import BytesIO

from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

from .models import Problem, Submission, Leaderboard, Certificate, TestCase

# ================= UPDATE LEADERBOARD =================
def update_leaderboard():
    users = Submission.objects.values('user').distinct()
    leaderboard = []

    for u in users:
        latest_submissions = (
            Submission.objects
            .filter(user=u['user'])
            .values('problem')
            .annotate(latest_id=models.Max('id'))
        )

        submissions = Submission.objects.filter(
            id__in=[item['latest_id'] for item in latest_submissions]
        )

        total = sum(sub.score for sub in submissions)
        leaderboard.append((u['user'], total))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    Leaderboard.objects.all().delete()

    rank = 1
    for user_id, score in leaderboard:
        Leaderboard.objects.create(
            user_id=user_id,
            total_score=score,
            rank=rank
        )
        rank += 1


# ================= HOME =================
def codeHome(request):
    problems = Problem.objects.all().order_by('id')

    query = request.GET.get('q')
    difficulty = request.GET.get('difficulty')

    if query:
        problems = problems.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if difficulty and difficulty != 'all':
        problems = problems.filter(difficulty__iexact=difficulty)

    paginator = Paginator(problems, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'codetechies/home.html', {
        'page_obj': page_obj,
        'query': query,
        'selected_difficulty': difficulty
    })


# ================= PROBLEM PAGE =================
@login_required
def problemPage(request, pk):
    problem = Problem.objects.get(id=pk)

    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language', '71')
        custom_input = request.POST.get('custom_input')
        is_submit = request.POST.get('submit')

        url = "https://ce.judge0.com/submissions?base64_encoded=false&wait=true"

        # =========================
        # ▶ RUN BUTTON (ONLY OUTPUT)
        # =========================
        if not is_submit:
            payload = {
                "language_id": int(language),
                "source_code": code,
                "stdin": custom_input or ""
            }

            try:
                response = requests.post(url, json=payload)
                result = response.json()
            except:
                return JsonResponse({'output': '⚠️ API Error. Try again.'})

            output = (
                result.get("stdout") or
                result.get("stderr") or
                result.get("compile_output") or
                "No Output"
            ).strip()

            return JsonResponse({
                'output': output,
                'score': 0
            })

        # =========================
        # 🚀 SUBMIT BUTTON (REAL JUDGE)
        # =========================
        testcases = TestCase.objects.filter(problem=problem)

        # 🔥 HANDLE NO TESTCASES (IMPORTANT FIX)
        if not testcases.exists():
            score = 0
            status = "attempted"

            Submission.objects.create(
                user=request.user,
                problem=problem,
                code=code,
                output="⚠️ No testcases found",
                score=score,
                status=status
            )

            update_leaderboard()

            Certificate.objects.get_or_create(
                user=request.user,
                problem=problem,
                cert_type='participation',
                defaults={
                    'title': f"{problem.title} - Participation"
                }
            )

            return JsonResponse({
                'output': '⚠️ No testcases found for this problem',
                'score': 0
            })

        # =========================
        # 🧪 RUN ALL TESTCASES
        # =========================
        passed = 0
        total = testcases.count()
        last_output = ""

        for tc in testcases:
            payload = {
                "language_id": int(language),
                "source_code": code,
                "stdin": tc.input_data
            }

            try:
                response = requests.post(url, json=payload)
                result = response.json()
            except:
                return JsonResponse({'output': '⚠️ API Error. Try again.'})

            output = (
                result.get("stdout") or
                result.get("stderr") or
                result.get("compile_output") or
                "No Output"
            ).strip()

            last_output = output

            if output == tc.expected_output.strip():
                passed += 1

        # =========================
        # 🎯 SCORING LOGIC
        # =========================
        score = int((passed / total) * problem.points)
        status = "completed" if passed == total else "attempted"

        # =========================
        # 💾 SAVE SUBMISSION
        # =========================
        Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            output=last_output,
            score=score,
            status=status
        )

        # =========================
        # 🏆 LEADERBOARD + CERTIFICATE
        # =========================
        update_leaderboard()

        cert_type = 'completion' if passed == total else 'participation'

        Certificate.objects.get_or_create(
            user=request.user,
            problem=problem,
            cert_type=cert_type,
            defaults={
                'title': f"{problem.title} - {cert_type.title()}"
            }
        )

        return JsonResponse({
            'output': last_output,
            'score': score,
            'passed': passed,
            'total': total
        })

    return render(request, 'codetechies/problem.html', {'problem': problem})

# ================= LEADERBOARD =================
@login_required
def leaderboardPage(request):
    data = Leaderboard.objects.all().order_by('rank')
    return render(request, 'codetechies/leaderboard.html', {'data': data})


# ================= MY SCORE =================
@login_required
def myScore(request):
    latest_submissions = (
        Submission.objects
        .filter(user=request.user)
        .values('problem')
        .annotate(latest_id=Max('id'))
    )

    submissions = Submission.objects.filter(
        id__in=[item['latest_id'] for item in latest_submissions]
    ).select_related('problem')

    total = sum(sub.score for sub in submissions)

    return render(request, 'codetechies/myscore.html', {
        'submissions': submissions,
        'total': total
    })


# ================= CERTIFICATE =================
@login_required
def certificatePage(request):
    cert = Certificate.objects.filter(user=request.user).order_by('-issued_date')
    return render(request, 'codetechies/certificate.html', {'cert': cert})


# ================= DOWNLOAD CERTIFICATE =================
@login_required
def downloadCertificate(request, cert_id):
    cert = Certificate.objects.get(id=cert_id, user=request.user)

    problem = cert.problem if cert.problem else None
    problem_name = problem.title if problem else "General Participation"
    difficulty = problem.difficulty.upper() if problem else "N/A"

    cert_title = "CERTIFICATE OF COMPLETION" if cert.cert_type == "completion" else "CERTIFICATE OF PARTICIPATION"
    action_text = "for successfully completing the coding problem" if cert.cert_type == "completion" else "for participating in the coding problem"

    buffer = BytesIO()
    width, height = 11 * inch, 8.5 * inch
    p = canvas.Canvas(buffer, pagesize=(width, height))

    # 🌈 BACKGROUND
    p.setFillColorRGB(0.95, 0.97, 1)
    p.rect(0, 0, width, height, fill=1)

    # 🟡 OUTER BORDER
    p.setStrokeColorRGB(0.8, 0.6, 0.1)
    p.setLineWidth(6)
    p.rect(40, 40, width-80, height-80)

    # INNER BORDER
    p.setLineWidth(2)
    p.rect(60, 60, width-120, height-120)

    # 🏆 LOGO (FIXED POSITION ✅)
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')
    if os.path.exists(logo_path):
        logo_width = 80
        logo_height = 80
        logo_x = (width - logo_width) / 2
        logo_y = height - 190   # 🔥 moved down to avoid border overlap

        p.drawImage(ImageReader(logo_path), logo_x, logo_y, width=logo_width, height=logo_height)

    # 🏅 TITLE (adjusted spacing)
    p.setFont("Helvetica-Bold", 30)
    p.setFillColorRGB(0.1, 0.1, 0.4)
    p.drawCentredString(width/2, height-240, cert_title)

    # SUBTITLE
    p.setFont("Helvetica", 16)
    p.setFillColorRGB(0.2, 0.2, 0.2)
    p.drawCentredString(width/2, height-280, "CodeTechies by Techies proudly presents this certificate to")

    # 👤 USER NAME (HIGHLIGHTED)
    p.setFont("Helvetica-Bold", 36)
    p.setFillColorRGB(0.0, 0.3, 0.8)
    p.drawCentredString(width/2, height-330, request.user.username.upper())

    # DESCRIPTION
    p.setFont("Helvetica", 16)
    p.setFillColorRGB(0.2, 0.2, 0.2)
    p.drawCentredString(width/2, height-370, action_text)

    # 📌 PROBLEM NAME (HIGHLIGHTED)
    p.setFont("Helvetica-Bold", 22)
    p.setFillColorRGB(0.6, 0.1, 0.1)
    p.drawCentredString(width/2, height-410, problem_name)

    # 🎯 DIFFICULTY (HIGHLIGHTED)
    p.setFont("Helvetica-Bold", 18)
    p.setFillColorRGB(0.2, 0.5, 0.2)
    p.drawCentredString(width/2, height-445, f"Difficulty Level: {difficulty}")

    # 📅 CERT DETAILS
    cert_code = str(cert.id).zfill(6)
    p.setFont("Helvetica", 12)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(90, 110, f"Certificate ID: TECH-{cert_code}")
    p.drawString(90, 90, f"Date: {datetime.now().strftime('%d %B %Y')}")

    # ✍ SIGNATURE
    sign_path = os.path.join(settings.BASE_DIR, 'static/images/signature.png')
    if os.path.exists(sign_path):
        p.drawImage(ImageReader(sign_path), width-220, 100, width=130, height=45)

    p.setFont("Helvetica", 12)
    p.drawCentredString(width-155, 85, "Authorized Signature")

    # 🔥 FOOTER BRANDING
    p.setFont("Helvetica-Bold", 16)
    p.setFillColorRGB(0.1, 0.1, 0.5)
    p.drawCentredString(width/2, 80, "CodeTechies by Techies")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

# ================= DASHBOARD =================
@login_required
def dashboard(request):
    user = request.user

    total_problems = Problem.objects.count()

    latest_submissions = (
        Submission.objects
        .filter(user=user)
        .values('problem')
        .annotate(latest_id=models.Max('id'))
    )

    submissions = Submission.objects.filter(
        id__in=[item['latest_id'] for item in latest_submissions]
    ).select_related('problem')

    solved = sum(1 for sub in submissions if sub.score > 0)

    attempted = submissions.count()
    accuracy = int((solved / attempted) * 100) if attempted > 0 else 0

    rank_obj = Leaderboard.objects.filter(user=user).first()
    rank = rank_obj.rank if rank_obj else "N/A"

    recent = Submission.objects.filter(user=user).order_by('-id')[:5]

    progress = int((solved / total_problems) * 100) if total_problems > 0 else 0

    return render(request, 'codetechies/dashboard.html', {
        'total_problems': total_problems,
        'solved': solved,
        'accuracy': accuracy,
        'rank': rank,
        'recent': recent,
        'progress': progress
    })