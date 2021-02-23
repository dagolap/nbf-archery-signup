from django.urls import path

from . import views

app_name="signups"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:competition_id>', views.competition_page, name="competition"),
    path('<int:competition_id>/participants/csv', views.competition_participants_csv, name="participants_csv"),
    path('<int:competition_id>/participants/scores', views.submitted_scores, name="submitted_scores"),
    path('results/<uuid:signup_id>', views.submit_results_page, name="result_delivery"),
]