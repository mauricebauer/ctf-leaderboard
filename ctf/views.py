from typing import Dict, List
from django.urls import reverse
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from ctf.forms import SubmissionForm
from ctf.models import Content, Flag, Participant, Submission
from app.settings import CUSTOM_TITLE, env


def index(request):
    content = Content.objects.all()
    return render(request, "index.html", context={
        "content": content,
        "custom_title": CUSTOM_TITLE
    })


def submit(request):
    if request.method == "POST":
        if not request.session.session_key:
            request.session.create()
        form = SubmissionForm(request.POST)
        if form.is_valid():
            flag = Flag.objects.filter(
                secret=form.cleaned_data["secret"]).first()
            participant = form.cleaned_data["participant"]
            participant.custom_name = form.cleaned_data["name"]
            participant.save()
            submission = Submission(
                flag=flag, participant=participant, session_id=request.session.session_key)
            submission.save()
            request.session["participant"] = participant.name
            return HttpResponseRedirect(reverse("board"))
    else:
        initial = {}
        participant_name = request.session.get("participant", "")
        participant = Participant.objects.filter(name=participant_name).first()
        if participant:
            initial["participant"] = participant
            initial["name"] = participant.custom_name
        form = SubmissionForm(initial=initial)

    return render(request, "submit.html", context={
        "form": form,
        "custom_title": CUSTOM_TITLE
    })


def board(request):
    flags = Flag.objects.all()
    participants = Participant.objects.all()
    my_participant_name: str = ""
    if request.session.get("participant", ""):
        my_participant = Participant.objects.filter(
            name=request.session["participant"]).first()
        if my_participant:
            my_participant_name = my_participant.name

    table_entries: List[Dict] = []
    for participant in participants:
        entry = {"name": participant.name}
        entry["display_name"] = f"{participant.name}: {participant.custom_name}" if participant.custom_name else participant.name
        entry["flags"] = []
        for flag in flags:
            submission = Submission.objects.filter(
                flag=flag, participant=participant).first()
            entry["flags"].append({
                "datetime": "" if not submission else submission.created_at.strftime('%d.%m.%Y %H:%M:%S'),
                "time": "" if not submission else f"{submission.created_at.strftime('%H:%M')} 🚩",
            })
        table_entries.append(entry)

    context = {
        "flags": flags,
        "participants": participants,
        "my_participant_name": my_participant_name,
        "table_entries": table_entries,
        "refreshInMs": env("REFRESH_IN_S", cast=int, default=30) * 1000,
        "custom_title": CUSTOM_TITLE
    }

    return render(request, "board.html", context=context)
