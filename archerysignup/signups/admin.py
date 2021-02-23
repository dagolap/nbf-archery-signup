from django.contrib import admin

from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse

from .models import Competition, ArcherClass, Signup, ResultDelivery

class SignupInline(admin.TabularInline):
    model = Signup

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "signup_count", "export_csv_button", "show_submitted_results")
    inlines = [SignupInline]

    def export_csv_button(self, obj):
        return format_html(
            '<a href="{}">CSV</a>',
            reverse('signups:participants_csv', kwargs={'competition_id': obj.id})
        )
    export_csv_button.short_description = "Deltakerliste"

    def show_submitted_results(self, obj):
        return format_html(
            '<a href="{}">Scorekort</a>',
            reverse('signups:submitted_scores', kwargs={'competition_id': obj.id})
        )
    show_submitted_results.short_description = "Resultater"


# Registering model admins
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(ArcherClass)
admin.site.register(Signup)
admin.site.register(ResultDelivery)

# Unregistering deafult models that we will not be using
# admin.site.unregister(Group)
# admin.site.unregister(User)