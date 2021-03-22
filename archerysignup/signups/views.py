import codecs
import logging

from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import csv

from .models import Competition, Signup, ResultDelivery
from .forms import SignupForm, ResultsDeliveryForm

logger = logging.getLogger(__name__)

def competition_page(request, competition_id):
    comp = get_object_or_404(Competition, pk=competition_id)
    form = SignupForm(request.POST or None, competition_id=competition_id)
    if comp.signup_deadline < timezone.now():
        return render(request, 'thanks.html', { 'message': "Men... påmeldingsfristen er dessverre utgått"})
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            Signup.objects.create(
                name=name,
                competition_id=competition_id,
                archer_id=form.cleaned_data['archer_id'],
                email=email,
                archer_class=form.cleaned_data['archer_class'])
            try:
                send_mail(
                    'Påmeldingsbekreftelse %s' % (comp.name),
                    'Vi bekrefter din påmelding til stevnet %s.\n\nNår stevnedato nærmer seg vil du motta epost med videre informasjon om gjennomføring og resultatleveranse, samt scorekort.\n\n\nLykke til på stevnet,\n\nNorges Bueskytterforbund' % (comp.name),
                    'NBF Stevnepåmelding <%s>' % (settings.SERVER_EMAIL),
                    ['%s <%s>' % (name, email)],
                    fail_silently=False,
                )
                return render(request, "thanks.html", { 'message': "Din påmelding er mottatt. Bekreftelse og videre informasjon har blitt sendt til oppgitt epost-adresse." })
            except Exception as e:
                logger.error("Could not send email during signup confirmation: ", e)
                return render(request, "thanks.html", { 'message': "Din påmelding er mottatt. På grunn av en teknisk feil klarte vi dessverre ikke å sende deg en epostbekreftelse, men du er nå påmeldt - vi lover." })

    return render(request, 'competition.html', {'competition': comp, 'form': form})

def submit_results_page(request, signup_id):
    previously_delivered = ResultDelivery.objects.filter(signup__pk=signup_id)
    if len(previously_delivered) > 0:
        return render(request, 'thanks.html', { 'message': "Dine resultater er allerede mottatt" })

    signup = get_object_or_404(Signup, pk=signup_id)

    if signup.competition.end_date < timezone.now():
        return render(request, "thanks.html", { "title": "Dessverre", "message": "Frist for innsending av scorekort er utgått." })

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
            try:

                send_mail(
                    'Resultatbevis mottatt for %s' % (signup.competition.name),
                    'Vi bekrefter å ha mottatt dokumentasjon i forbindelse med din deltakelse på stevnet %s.\n\nTakk for at du deltok.\n\n\nMvh,\n\nNorges Bueskytterforbund' % (signup.competition.name),
                    'NBF Stevnepåmelding <%s>' % (settings.SERVER_EMAIL),
                    ['%s <%s>' % (signup.name, signup.email)],
                    fail_silently=False,
                )
                return render(request, "thanks.html", { 'message': "Dine resultater er mottatt. En epost med bekreftelse er sendt til din epost." })
            except Exception as e:
                logger.error("Could not send email during results delivery: ", e)
                return render(request, "thanks.html", { 'message': "Dine resultater er mottatt. På grunn av en teknisk feil klarte vi dessverre ikke å sende deg en epostbekreftelse, men vi har mottatt alt vi trenger - tusen takk." })

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

    response.write(codecs.BOM_UTF8)

    writer = csv.writer(response)
    for p in participants:
        writer.writerow([p.archer_id, p.name, p.email, p.archer_class.code, p.archer_class.description, request.build_absolute_uri(p.get_score_submission_url())])

    return response

def submitted_scores(request, competition_id):
    if not request.user.has_perm("signups.view_competition"):
        return HttpResponseForbidden()

    comp = get_object_or_404(Competition, pk=competition_id)
    scores = ResultDelivery.objects.select_related('signup').filter(signup__competition_id=competition_id).order_by('signup__archer_id')

    return render(request, "results.html", {'scores': scores, 'comp': comp})