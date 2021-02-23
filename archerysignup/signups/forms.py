from django import forms

from .models import Signup, ResultDelivery, Competition

class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ["archer_id", "name", "email", "archer_class"]
    
    def __init__(self, *args, **kwargs):
        competition_id = kwargs.pop('competition_id')
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['archer_class'].queryset = Competition.objects.get(pk=competition_id).allowed_classes


class ResultsDeliveryForm(forms.ModelForm):
    class Meta:
        model = ResultDelivery
        fields = ["scorecard", "proof_image1", "proof_image2", "proof_image3", "proof_image4"]