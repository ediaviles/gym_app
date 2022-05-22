from email import message
from operator import attrgetter
from pdb import post_mortem
import re
from sqlite3 import Date
import datetime
from tracemalloc import start
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
import requests, json
from collections import defaultdict

# login_required is getting information from "settings.py -> LOGIN_URL" 
# to know where to direct to if the user isn't logged in
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from HealthWebsite.models import DailyDiary, ExerciseList, AddressInfo, TempDailyDiary, Profile
from HealthWebsite.forms import ExerciseForm, BreakfastForm, LunchForm, DinnerForm, ProfileInfoForm, DailyDiaryForm
from django.utils import timezone

import sys # for debugging purposes to print the current function name

# from socialnetwork.forms import LoginForm, RegisterForm, ProfileForm
# from socialnetwork.models import Post, Comment, Profile

import json

# from HealthWebsite.models import GymInfo
def profile_required(func):
    def wrapper(request, **kwargs):
        try :
            request.user.profile
        except:
            profile = Profile(user=request.user)
            profile.save()
        return func(request, **kwargs)
    return wrapper


def estimateOneRepMax(weight, reps) :
    print((int(weight)/(1.0278-0.0278*int(reps))))
    return ((int(weight)/(1.0278-0.0278*int(reps))))

def SanitizeNumbers(request):
    post_params = {"squat_weight"
                 , "squat_reps"
                 , "deadlift_weight"
                 , "deadlift_reps"
                 , "bench_weight"
                 , "bench_reps"

                 , "weight"

                 , "breakfastProtein"
                 , "breakfastCarbs"
                 , "breakfastFats"

                 , "lunchProtein"
                 , "lunchCarbs"
                 , "lunchFats"

                 , "dinnerProtein"
                 , "dinnerCarbs"
                 , "dinnerFats"}
    for param in post_params:
        inpt = request.POST[param]
        try: int(inpt)
        except: return False
    return True


@login_required
@profile_required
def DailyDiaryAction(request):
    print(f"\n\n\n--------{sys._getframe().f_code.co_name}") # print the name of the current function im in
    context = {}
    
    if request.method == 'GET':
        state = "new"
        context = {
               "exform": ExerciseForm() 
             , "bform": BreakfastForm()
             , "lform": LunchForm()
             , "dform": DinnerForm()
             , "ddform": DailyDiaryForm()
             , "state": state}
        return render(request, 'HealthWebsite/dd_page.html', context)
    
    dd_date = datetime.datetime.strptime(request.POST["dd_date"], "%Y-%m-%d")
    user_data = DailyDiary.objects.filter(
                                    owner=request.user
                                ).filter(
                                    creation_time__range=[dd_date, dd_date+datetime.timedelta(days = 1)]
                                )
    if (len(user_data) != 0): # there was already a daily dairy submitted for this date
        state = "completed"
    else: 
        state = "new"

    if (not SanitizeNumbers(request)):
        # TODO: give the user an actual error message rather than just reloading the page
        return redirect(reverse("daily-diary")) 

    # Must have been a post and therefore the user submitted data
    # FIXME: make sure to sanitize this data. NEVER trust input from the user
    exercises = ExerciseList(
                squat_weight=request.POST["squat_weight"]
                , squat_reps=request.POST["squat_reps"]
                , deadlift_weight=request.POST["deadlift_weight"]
                , deadlift_reps=request.POST["deadlift_reps"]
                , bench_weight=request.POST["bench_weight"]
                , bench_reps=request.POST["bench_reps"]
                )
    exercises.save()

    ddEntry = DailyDiary(
                    owner=request.user
                  , creation_time=dd_date
                  , exercises=exercises
                  , weight=request.POST["weight"]

                  , breakfastProtein=request.POST["breakfastProtein"]
                  , breakfastCarbs=request.POST["breakfastCarbs"]
                  , breakfastFats=request.POST["breakfastFats"]

                  , lunchProtein=request.POST["lunchProtein"]
                  , lunchCarbs=request.POST["lunchCarbs"]
                  , lunchFats=request.POST["lunchFats"]

                  , dinnerProtein=request.POST["dinnerProtein"]
                  , dinnerCarbs=request.POST["dinnerCarbs"]
                  , dinnerFats=request.POST["dinnerFats"]
                )
    ddEntry.save()
    print(f"ddEntry being entered: {ddEntry}")
    print(f"all ddObjects: {DailyDiary.objects.all()}")
    # Want to update user maxes
    oneRepBench = estimateOneRepMax(request.POST["bench_weight"], request.POST["bench_reps"])
    oneRepSquat = estimateOneRepMax(request.POST["squat_weight"], request.POST["squat_reps"])
    oneRepDeadlift = estimateOneRepMax(request.POST["deadlift_weight"], request.POST["deadlift_reps"])
    profile = Profile.objects.filter(
                                    user=request.user
                                    )
    if (len(profile)!=0) :
        #Check current maxes
        profileObject = profile.get()
        if (profileObject.maxBench < oneRepBench):
            profileObject.maxBench = oneRepBench
        if (profileObject.maxSquat < oneRepSquat):
            profileObject.maxSquat = oneRepSquat
        if (profileObject.maxDeadlift < oneRepDeadlift):
            profileObject.maxDeadlift = oneRepDeadlift
        profileObject.save()
    else :
        profile = Profile(user=request.user,
                            address="",
                            maxBench=oneRepBench,
                            maxSquat=oneRepSquat,
                            maxDeadlift=oneRepDeadlift)
        profile.save()

    context = {
               "exform": ExerciseForm() 
             , "bform": BreakfastForm()
             , "lform": LunchForm()
             , "dform": DinnerForm()
             , "ddform": DailyDiaryForm()
             , "state": state}
    return render(request, 'HealthWebsite/dd_page.html', context)

@login_required
@profile_required
def RootAction(request):
    print(f"\n\n\n--------{sys._getframe().f_code.co_name}")
    context = {}
    return render(request, 'HealthWebsite/progress_page.html', context)

@login_required
@profile_required
def MapsAction(request):
    context = {}
    return render(request, 'HealthWebsite/maps.html', context)

def GraphJSON(graphing, graph_type, data, units):
    print(f"\n\n\n--------{sys._getframe().f_code.co_name}")
    # set up the expected fields for the JSON
    response_data = {
        "graphing": graphing
      , "graph_type": graph_type
      , "data": data
      , "units": units
    }

    # turn dict into json string and send it to a webpage for later parsing
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

@login_required
@profile_required
def UpdateGraph(request):
    print(f"\n\n\n--------{sys._getframe().f_code.co_name}")
    # Check if a graphing param was in the post request
    # if not, set the default to weight, otherwise display what the user
    # requested
    print(f"request.POST: {request.POST}")
    if ((not "graphing" in request.POST) or (not request.POST["graphing"])):
        graphing = "weight"
    else: 
        graphing = request.POST["graphing"]

    # casing on if start date was provided or if to use the default
    if ((not "startdate" in request.POST) or (not request.POST["startdate"]) or
        (request.POST["startdate"] == "")):
        startdate = datetime.date.today()
    else:
        startdate = request.POST["startdate"]

    # casing on if end date was provided or if to use the default
    if ((not "enddate" in request.POST) or (not request.POST["enddate"]) or
        (request.POST["enddate"] == "")):
        enddate = datetime.date.today() + datetime.timedelta(days=1)
    else:
        # print(request.POST["enddate"])
        enddate = datetime.datetime.strptime(request.POST["enddate"], "%Y-%m-%d") + datetime.timedelta(days=1)

    # define the data that will be passed into the json serializer
    user_data = DailyDiary.objects.filter(
                                    owner=request.user
                                ).filter(
                                    creation_time__range=[startdate, enddate]
                                ).order_by("creation_time")

    data_by_category = dict()

    # Get the exercise data out and add it to a dict
    def BenchSquatDeadliftDataLabels(user_data, attr_to_grab):
        dataset = ["Reps", "Weight"]
        labels = list()
        data = [[], [], []]
        for entry in user_data:
            form = entry
            entry = entry.exercises
            if (getattr(entry, attr_to_grab+"_reps") == 0): continue
            labels.append(form.creation_time.strftime("%a, %m-%d-%Y").__str__())
            data[0].append(getattr(entry, attr_to_grab+"_reps"))
            data[1].append(getattr(entry, attr_to_grab+"_weight"))
        data[2] = dataset
        return (data, labels)

    # Get t
    def GetDataAndLabels(user_data, attr_to_grab):
        labels = list()
        data = list()
        for entry in user_data:
            print(entry)
            if (getattr(entry, attr_to_grab) == 0): continue
            labels.append(entry.creation_time.strftime("%a, %m-%d-%Y").__str__())
            data.append(getattr(entry, attr_to_grab))
        return (data, labels)

    def GetMacroSums(user_data):
        # protein = index 0
        # carbs = index 1
        # fats = index 2
        macrosDict = defaultdict(lambda: [0,0,0])
        for entry in user_data:
            for time in {"breakfast", "lunch", "dinner"}:
                macrosDict[time][0] += getattr(entry, time+"Protein")
                macrosDict[time][1] += getattr(entry, time+"Carbs")
                macrosDict[time][2] += getattr(entry, time+"Fats")

                macrosDict["all"][0] += getattr(entry, time+"Protein")
                macrosDict["all"][1] += getattr(entry, time+"Carbs")
                macrosDict["all"][2] += getattr(entry, time+"Fats")
        return macrosDict

    # default values
    graph_type = "bar"
    units = "kilograms (kg)"

    # Collect and calculate the data from the users input
    for exer in {"deadlift", "bench", "squat"}:
        data_by_category[exer] = BenchSquatDeadliftDataLabels(user_data, exer)
    data_by_category["macros"] = (GetMacroSums(user_data), ["protein", "carbs", "fats"])
    data_by_category["weight"] = GetDataAndLabels(user_data, "weight")

    print(f"\n\n\n\n-----------UserData: {user_data}")
    print(f"\nnofilteredL {DailyDiary.objects.filter(owner=request.user)}")
    print(f"\n-----------DataByCategory: {data_by_category}\n\n\n\n")

    return GraphJSON(graphing, graph_type, data_by_category, units)

@login_required
@profile_required
def ProfilePageAction(request):
    print(f"\n\n\n--------{sys._getframe().f_code.co_name}")
    try:
        profile = request.user.profile
    except:
        profile = Profile(user=request.user)
        profile.save()
    print(profile.address)
    context = {'profile': profile}
    return render(request, 'HealthWebsite/profile_page.html', context)

@login_required
@profile_required
def GoogleMapsAction(request):
    print(f"\n\n\n--------{sys._getframe().f_code.co_name}")
    context = {}
    return render(request, 'HealthWebsite/google_maps.html', context)

@login_required
@profile_required
def GymInfo(request):
    context = {}
    return render(request, 'HealthWebsite/gym_info.html', context)

@login_required
@profile_required
def GymBuddies(request):
    context = {}
    if request.method == 'GET':
        addressForm = ProfileInfoForm()
        context = {"addressForm": addressForm}
        return render(request, 'HealthWebsite/gym_buddies.html', context)
    addressEntry = AddressInfo(
                    user=request.POST["user"],
                    addressLine1=request.POST["addressLine1"],
                    addressLine2=request.POST["addressLine2"],
                    addressCity=request.POST["addressCity"],
                    addressState=request.POST["addressState"],
                    addressZipCode=request.POST["addressZipCode"]
    )
    addressEntry.save()
    return render(request, 'HealthWebsite/gym_buddies.html', context)

@login_required
@profile_required
def GymLocations(request, loc=None):
    if(loc == None):
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522%2C151.1957362&radius=2000&type=gym&key=AIzaSyDtdUoI-AHQhiY6OO3qLCX6yIJNWAg7R0k'
    else:
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+loc+'&radius=2000&keyword=gym&key=AIzaSyDtdUoI-AHQhiY6OO3qLCX6yIJNWAg7R0k'
    # keyword=gym
    payload={}
    headers = {}
    context = dict()
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    # print(json_object['results'][0])
    for key in json_object.keys():
        if(key == "results"):
            for gym in json_object['results']:
                # print(gym)
                bussiness_hours = gym['business_status'] if "business_status" in gym else None #0
                name = gym['name'] if "name" in gym else None #1
                opening_hours = gym['opening_hours'] if "opening_hours" in gym else None #2
                scope = gym['scope'] if "scope" in gym else None #3
                types = gym['types'] if "types" in gym else None #4
                vicinity = gym['vicinity'] if "vicinity" in gym else None #5
                location = gym['geometry']['location'] if ('geometry' in gym) and 'location' in gym['geometry'] else None #6
                obj = (bussiness_hours, name, opening_hours, scope, types, vicinity, location)
                if("results" not in context):
                    context["results"] = [obj]
                else:
                    context["results"].append(obj)
    response_json = json.dumps(context['results'])    
    return HttpResponse(response_json, content_type='application/json')
        #render(request, 'HealthWebsite/maps.html', context)

@login_required
@profile_required
def TestAction(request):
    print(f"\n\n\n--------{sys._getframe().f_code.co_name}")
    context = {}
    return render(request, 'HealthWebsite/homepage.html', context)

@login_required
@profile_required
def MainPageAction(request):
    print(f"\n\n\n--------{sys._getframe().f_code.co_name}")
    context = {}
    return render(request, 'HealthWebsite/progress_page.html', context)

@login_required
@profile_required
def UserAddress(request):
    # print("We here")
    if request.method == 'GET':
        context = {}
        print("prof add",request.user.profile.address)
        if (request.user.profile.address != "") :
            profile = Profile.objects.get(user=request.user)
            address = request.user.profile.address
            for buddy in profile.gymBuddies.all():
                print("buddy",buddy)
                profile.gymBuddies.remove(buddy)
                print("after delete",profile.gymBuddies.all())
                profile.save()
            profileList = Profile.objects.all()
            for p in profileList:
                print("Profile",request.user.profile)
                if p.user == request.user :
                    continue
                elif p.user in request.user.profile.friends.all() or p.user in request.user.profile.rejected.all():
                    continue
                else :
                    if(p.address == ""): continue
                    distance = GetDistance(address, p.address)
                    # val = 0
                    print("Here's distance", distance)
                    # if(distance[-2:] != "km" or distance[-2:] != "ft"): val = float(distance[:-2])/1000
                    # elif(distance[-2:] != "km"): val = float(distance[:-3])/3281
                    # else: float(distance[:-3])
                    dist = distance.split(" ")
                    dist_num = float(dist[0])
                    if (dist[1] == "ft"): dist_num *= 0.000305
                    elif (dist[1] == "m"): dist_num /= 1000.0
                    elif (dist[1] == "mi"): dist_num *= 1.60934
                    elif (dist[1] == "km"): pass
                    else: print("\n\n\n\nI Don'T KNOW THESE UNITS\n\n\n\n")
                    if(dist_num < 5.0):
                        # print("val for get distance", val)
                        profileObject = Profile.objects.get(user=request.user)
                        profileObject.gymBuddies.add(p.user)
                        # print(profileObject.gymBuddies.all())
                        profileObject.save()
        return render(request, "HealthWebsite/gym_buddies.html", context)
    print("Entered UserAddress-------->")
    address = request.POST["address"]
    try:
        profile = Profile.objects.get(user=request.user)
    except :
        profile = Profile(user=request.user,address=address)
    if (profile) :
        #Check current maxes
        # profileObject = profile.get()
        profile.address = address
        profile.save()
    else :
        profile = Profile(user=request.user,
                            address=address)
        profile.save()
    if(address != ""):
        # print(profile.get())
        # Remove all old gymBuddies
        print("gym buddies", profile.gymBuddies.all())
        for buddy in profile.gymBuddies.all():
            print("buddy",buddy)
            profile.gymBuddies.remove(buddy)
            print("after delete",profile.gymBuddies.all())
            profile.save()
        profileList = Profile.objects.all()
        for p in profileList:
            if p.user == request.user :
                continue
            else :
                if(p.address == ""): continue
                distance = GetDistance(address, p.address)
                dist = distance.split(" ")
                dist_num = float(dist[0])
                if (dist[1] == "ft"): dist_num *= 0.000305
                elif (dist[1] == "m"): dist_num /= 1000.0
                elif (dist[1] == "mi"): dist_num *= 1.60934
                elif (dist[1] == "km"): pass
                else: print("\n\n\n\nI Don'T KNOW THESE UNITS\n\n\n\n")
                if(dist_num < 5.0):
                    profileObject = Profile.objects.get(user=request.user)
                    profileObject.gymBuddies.add(p.user)
                    # print(profileObject.gymBuddies.all())
                    profileObject.save()
    # profile = Profile.objects.filter(user=request.user)
    print("after all changes",profile.gymBuddies.all())
    context = {'profile': profile.user.profile}
    return redirect(reverse('user-address')) #'HealthWebsite/gym_buddies.html', context)


def GetDistance(source, dest):
    # enter your api key here
    api_key ='AIzaSyDtdUoI-AHQhiY6OO3qLCX6yIJNWAg7R0k'

    # url variable store url
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + source + '&destinations=' +dest+ '&key=' + api_key

    # Get method of requests module
    # return response object
    r = requests.get(url)
                        
    # json method of response object
    # return json format result
    x = r.json()

    # by default driving mode considered

    # print the value of x
    print(x['rows'], source, dest)
    return x['rows'][0]['elements'][0]['distance']['text']

@login_required
@profile_required
def AcceptDecline(request):
    if request.method == "GET" :
        return 
    print(request.POST)
    friend = request.POST['friend']
    print(friend)
    if 'accept' in request.POST :
        # Want to add to request.user friends
        profile = Profile.objects.get(user=request.user)
        if (friend in profile.friends.all()) :
            print('in friends')
        else :
            print(Profile.objects.get(user=friend))
            profile.friends.add(friend)
            profile.gymBuddies.remove(friend)
            profile.save()
    elif 'decline' in request.POST :
        profile = Profile.objects.get(user=request.user)
        print(profile.gymBuddies)
        friendObject = Profile.objects.get(user=friend)
        print("friendObject", friendObject.user)
        if friendObject.user in profile.friends.all() :
            print("we are already friends")
            profile.friends.remove(friendObject.user)
            profile.gymBuddies.add(friendObject.user)
        else :
            profile.gymBuddies.remove(friendObject.user)
            profile.rejected.add(friendObject.user)
        profile.save()
    print(profile.friends.all())
    print("Done with AcceptDecline--->")
    return redirect(reverse('user-address'))
