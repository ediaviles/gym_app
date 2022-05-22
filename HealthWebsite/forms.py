from cProfile import label
from email.headerregistry import Address
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from HealthWebsite.models import DailyDiary, ExerciseList, AddressInfo

class BreakfastForm(forms.ModelForm):
    class Meta:
        model = DailyDiary
        fields = ("breakfastProtein"
                , "breakfastCarbs"
                , "breakfastFats")
        widgets = {
            "breakfastProtein": forms.NumberInput(),
            "breakfastCarbs": forms.NumberInput(),
            "breakfastFats": forms.NumberInput(),
        }
        labels = {
            "breakfastProtein": "Proteins(g)",
            "breakfastCarbs": "Carbs(g)",
            "breakfastFats": "Fats(g)"
        }

class LunchForm(forms.ModelForm):
    class Meta:
        model = DailyDiary
        fields = ("lunchProtein"
                , "lunchCarbs"
                , "lunchFats")
        widgets = {
            "lunchProtein": forms.NumberInput(),
            "lunchCarbs": forms.NumberInput(),
            "lunchFats": forms.NumberInput(),
        }
        labels = {
            "lunchProtein": "Proteins(g)",
            "lunchCarbs": "Carbs(g)",
            "lunchFats": "Fats(g)"
        }

class DinnerForm(forms.ModelForm):
    class Meta:
        model = DailyDiary
        fields = ("dinnerProtein"
                , "dinnerCarbs"
                , "dinnerFats")
        widgets = {
            "dinnerProtein": forms.NumberInput(),
            "dinnerCarbs": forms.NumberInput(),
            "dinnerFats": forms.NumberInput(),
        }
        labels = {
            "dinnerProtein": "Proteins(g)",
            "dinnerCarbs": "Carbs(g)",
            "dinnerFats": "Fats(g)"
        }

class DailyDiaryForm(forms.ModelForm):
    class Meta: 
        model = DailyDiary
        fields = ("weight", )
        widgets = {
            "weight": forms.NumberInput()
        }
        labels = {
            "weight": "Current Weight"
        }

class ExerciseForm(forms.ModelForm):
    class Meta: 
        model = ExerciseList
        fields = ("squat_weight"
                , "squat_reps"
                , "deadlift_weight"
                , "deadlift_reps"
                , "bench_weight"
                , "bench_reps")
        widgets = {
            "squat_weight":     forms.NumberInput(),
            "bench_reps":       forms.NumberInput(),
            "squat_reps":       forms.NumberInput(),
            "deadlift_weight":  forms.NumberInput(),
            "deadlift_reps":    forms.NumberInput(),
            "bench_weight":     forms.NumberInput(),
        }
        labels = {
            "squat_weight":    "Squat Weight"
          , "squat_reps":      "Squat Reps"
          , "deadlift_weight": "Deadlift Weight"
          , "deadlift_reps":   "Deadlift Reps"
          , "bench_weight":    "Bench Weight"
          , "bench_reps":      "Bench Reps"
        }

class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = AddressInfo
        fields = (
            "addressLine1",
            "addressLine2",
            "addressCity",
            "addressState",
            "addressZipCode"
        )
        widgets = {
            "addressLine1"  : forms.TextInput(),
            "addressLine2"  : forms.TextInput(),
            "addressCity"   : forms.TextInput(),
            "addressState"  : forms.TextInput(),
            "addressZipCode": forms.TextInput()
        }
        labels = {
            "addressLine1"  : "Address Line 1:",
            "addressLine2"  : "Address Line 2:",
            "addressCity"   : "City:",
            "addressState"  : "State:",
            "addressZipCode": "Zip Code:"
        }
