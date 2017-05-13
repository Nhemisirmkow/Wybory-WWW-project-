import django.forms as forms

# from .models import SeriousQuestion, SeriousAnswer
#
# class SeriousQuestionForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ["username"]
#
# class SeriousAnswerForm(forms.Form):
#     answer = forms.CharField(max_length=200)
#
#     def clean(self):
#         if len(self.cleaned_data["answer"]) == 0 or self.cleaned_data["answer"][-1] != ".":
#             raise forms.ValidationError("Answer should end with a dot.")
from zadanie2.models import Gmina


class GminaQuestionForm(forms.ModelForm):
    class Meta:
        model = Gmina
        fields = ["nazwa"]


class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2