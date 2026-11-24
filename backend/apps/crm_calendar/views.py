import calendar as py_calendar
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.leads.models import LeadTask


@login_required
def index(request):
    today = date.today()

    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    month_matrix = py_calendar.monthcalendar(year, month)

    tasks = (
        LeadTask.objects.select_related("lead", "assigned_to")
        .filter(
            due_date__year=year,
            due_date__month=month,
        )
        .order_by("due_date", "priority")
    )

    task_lookup = {}

    for task in tasks:
        task_lookup.setdefault(task.due_date.day, []).append(task)

    calendar_weeks = []

    for week in month_matrix:
        week_data = []

        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                week_data.append({
                    "day": day,
                    "tasks": task_lookup.get(day, []),
                    "is_today": (
                        today.year == year
                        and today.month == month
                        and today.day == day
                    ),
                })

        calendar_weeks.append(week_data)

    context = {
        "today": today,
        "year": year,
        "month": month,
        "calendar_weeks": calendar_weeks,
    }

    return render(
        request,
        "crm_calendar/index.html",
        context,
    )