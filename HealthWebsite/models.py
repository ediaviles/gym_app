from codecs import backslashreplace_errors
from email import message
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Person(models.Model):
#     user        = models.OneToOneField(User, on_delete=models.CASCADE) # UNSURE: refer back to Cascade
#     zipcode     = models.CharField(blank=True, max_length=10)
#     def __str__(self):
#         return f'Person({self.user.first_name})'

class ExerciseList(models.Model):
    squat_weight       = models.IntegerField(default=0)
    squat_reps         = models.IntegerField(default=0)
    deadlift_weight    = models.IntegerField(default=0)
    deadlift_reps      = models.IntegerField(default=0)
    bench_weight       = models.IntegerField(default=0)
    bench_reps         = models.IntegerField(default=0)

    def __str__(self):
        return f'Excercises(Squat: {self.squat_weight}-{self.squat_reps}, Deadlift: {self.deadlift_weight}-{self.deadlift_reps}, Bench: {self.bench_weight}-{self.bench_reps})'

class DailyDiary(models.Model):
    owner           = models.ForeignKey(User, on_delete=models.PROTECT) # changed from Person. May not need Person model anymore
    creation_time   = models.DateTimeField()

    exercises       = models.OneToOneField(ExerciseList, on_delete=models.CASCADE)
    
    breakfastProtein = models.IntegerField(default=0)
    breakfastCarbs = models.IntegerField(default=0)
    breakfastFats = models.IntegerField(default=0)

    lunchProtein = models.IntegerField(default=0)
    lunchCarbs = models.IntegerField(default=0)
    lunchFats = models.IntegerField(default=0)

    dinnerProtein = models.IntegerField(default=0)
    dinnerCarbs = models.IntegerField(default=0)
    dinnerFats = models.IntegerField(default=0)
    weight          = models.IntegerField(default=0)

    def __str__(self):
        return f'DailyDiary({self.owner}:{self.creation_time})' # id: {self.id}, 

class Message(models.Model):
    sender          = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    recipient       = models.ForeignKey(User, on_delete=models.PROTECT, related_name="recipient")
    creation_time   = models.DateTimeField()
    message         = models.CharField(max_length=500)

class AddressInfo(models.Model):
    user            = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user")
    creation_time   = models.DateTimeField()
    addressLine1    = models.CharField(max_length=500)
    addressLine2    = models.CharField(max_length=500)
    addressCity     = models.CharField(max_length=500)
    addressState    = models.CharField(max_length=500)
    addressZipCode  = models.CharField(max_length=500)
    def __str__(self):
        return f'AddressInfo(User: {self.user})'

class TempDailyDiary(models.Model):
    owner           = models.ForeignKey(User, on_delete=models.PROTECT) # changed from Person. May not need Person model anymore
    creation_time   = models.DateTimeField()

    exercises       = models.OneToOneField(ExerciseList, on_delete=models.CASCADE)
    
    breakfastProtein = models.IntegerField(default=0)
    breakfastCarbs = models.IntegerField(default=0)
    breakfastFats = models.IntegerField(default=0)

    lunchProtein = models.IntegerField(default=0)
    lunchCarbs = models.IntegerField(default=0)
    lunchFats = models.IntegerField(default=0)

    dinnerProtein = models.IntegerField(default=0)
    dinnerCarbs = models.IntegerField(default=0)
    dinnerFats = models.IntegerField(default=0)

    weight          = models.IntegerField(default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=750)
    gymBuddies = models.ManyToManyField(User, related_name="gym_buddies")
    friends = models.ManyToManyField(User, related_name="friends")
    rejected = models.ManyToManyField(User, related_name="rejected")
    maxBench = models.IntegerField(default=0)
    maxSquat = models.IntegerField(default=0)
    maxDeadlift = models.IntegerField(default=0)
