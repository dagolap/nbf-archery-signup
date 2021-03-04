from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import csv

from .models import Competition, Signup, ResultDelivery
from .forms import SignupForm, ResultsDeliveryForm

def competition_page(request, competition_id):
    comp = get_object_or_404(Competition, pk=competition_id)
    form = SignupForm(request.POST or None, competition_id=competition_id)
    if comp.signup_deadline < timezone.now():
        return render(request, 'thanks.html', { 'message': "Men... påmeldingsfristen er dessverre utgått"})
    if request.method == "POST":
        if form.is_valid():
            Signup.objects.create(
                name=form.cleaned_data['name'],
                competition_id=competition_id,
                archer_id=form.cleaned_data['archer_id'],
                email=form.cleaned_data['email'],
                archer_class=form.cleaned_data['archer_class'])
            return render(request, "thanks.html", { 'message': "Din påmelding er mottatt." })

    return render(request, 'competition.html', {'competition': comp, 'form': form})

def submit_results_page(request, signup_id):
    previously_delivered = ResultDelivery.objects.filter(signup__pk=signup_id)
    if len(previously_delivered) > 0:
        return render(request, 'thanks.html', { 'message': "Dine resultater er allerede mottatt" })

    signup = get_object_or_404(Signup, pk=signup_id)
    form = ResultsDeliveryForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if (form.is_valid()):
            ResultDelivery.objects.create(
                signup_id=signup_id,
                scorecard=request.FILES['scorecard'],
                proof_image1=request.FILES.get('proof_image1', None),
                proof_image2=request.FILES.get('proof_image2', None),
                proof_image3=request.FILES.get('proof_image3', None),
                proof_image4=request.FILES.get('proof_image4', None)
            )
            return render(request, "thanks.html", { 'message': "Dine resultater er mottatt." })

    return render(request, 'result_delivery.html', { 'form': form, 'signup': signup })

def index(request):
    comps = Competition.objects.filter(end_date__gte=datetime.now()).order_by("start_date")
    now = timezone.now()

    return render(request, 'competition_list.html', {'comps': comps, 'now': now})

def competition_participants_csv(request, competition_id):
    if not request.user.has_perm("signups.view_competition"):
        return HttpResponseForbidden()

    comp = Competition.objects.get(pk=competition_id)
    
    participants = Signup.objects.filter(competition__id=competition_id)
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="%s-deltakere.csv"' % (comp.name)

    writer = csv.writer(response)
    for p in participants:
        writer.writerow([p.archer_id, p.name, p.email, p.archer_class.code, p.archer_class.description, request.build_absolute_uri(p.get_score_submission_url())])

    return response

def submitted_scores(request, competition_id):
    if not request.user.has_perm("signups.view_competition"):
        return HttpResponseForbidden()

    scores = ResultDelivery.objects.select_related('signup').filter(signup__competition_id=competition_id).order_by('signup__archer_id')
    comp = Competition.objects.get(pk=competition_id)

    return render(request, "results.html", {'scores': scores, 'comp': comp})