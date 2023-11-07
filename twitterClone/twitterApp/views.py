from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . models import Profile,Meep
from .forms import MeepForm,SignUpForm,ProfilePicForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, ("Your meep has been posted"))
                return redirect('home')
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'meeps': meeps,'form':form})
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request,'home.html',{'meeps':meeps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request,'profile_list.html',{"profiles":profiles})
    else:
        messages.success(request,("You must be logged in to view this page"))
        return redirect('home')

def profile(request,pk):
    if request.user.is_authenticated:

        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")
        # post form logic
        if request.method == "POST":
            #get current user id
            current_user_profile = request.user.profile
            #get form data
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follow.remove(profile)
            elif action == "follow":
                current_user_profile.follow.add(profile)
            #save profile
            current_user_profile.save()


        return render(request,"profile.html",{'profile':profile,'meeps':meeps})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ("You have been logged in.."))
            return redirect('home')
        else:
            messages.success(request, ("There was an error"))
            return redirect('login')
    else:
        return render(request,"login.html",{})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logout"))
    return redirect('login')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
           # password2 = form.cleaned_data['password2']
           # first_name = form.cleaned_data['first_name']
            #lass_name = form.cleaned_data['last_name']
            #email = form.cleaned_data['email']

            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request, ("You have successfully registered"))
            return redirect('home')

    return render(request, "register.html", {'form':form})

def update_user(request):
    if request.user.is_authenticated:
            current_user = User.objects.get(id=request.user.id)
            user_form = SignUpForm(request.POST or None,request.FILES or None,instance=current_user)
            profile_user = Profile.objects.get(user__id = request.user.id)
            profile_form = ProfilePicForm(request.POST or None,request.FILES or None,instance=profile_user)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

                login(request,current_user)
                messages.success(request, ("Your profile has been updated"))
                return redirect('home')

            return render(request, "update_user.html", {'user_form':user_form,'profile_form':profile_form})
    else:
        messages.success(request,("You must logged in to view that page"))
        return redirect('home')

def meep_like(request,pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep,id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request,("You must be logged In"))
        return redirect('home')

def meep_show(request,pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep,id=pk)
        if meep:
            return render(request,'show_meep.html',{'meep':meep})
        else:
            messages.success(request, ("That meep doesn't exist.."))
            return redirect('home')


    else:
        messages.success(request, ("You must be logged In"))
        return redirect('home')

def unfollows(request,pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follow.remove(profile)
        # Save our profile
        request.user.profile.save()
        # Return message
        messages.success(request, (f"You have successfully unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))



    else:
        messages.success(request, ("You must be logged In"))
        return redirect('home')

def follows(request,pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follow.add(profile)
        # Save our profile
        request.user.profile.save()
        # Return message
        messages.success(request, (f"You have successfully followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must be logged In"))
        return redirect('home')

def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request,'followers.html',{"profiles":profiles})
        else:
            messages.success(request, ("Thats not your profile page"))
            return redirect('home')

    else:
        messages.success(request,("You must be logged in to view this page"))
        return redirect('home')

def follows(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request,'follows.html',{"profiles":profiles})
        else:
            messages.success(request, ("Thats not your profile page"))
            return redirect('home')

    else:
        messages.success(request,("You must be logged in to view this page"))
        return redirect('home')

def delete_meep(request,pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if request.user.username == meep.user.username:
            meep.delete()
            messages.success(request, ("The meep has been deleted!!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("NO! You don't own that meep"))
            return redirect('home')
    else:
        messages.success(request, ("Please login to delete"))
        return redirect(request.META.get("HTTP_REFERER"))

def edit_meep(request,pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if request.user.username == meep.user.username:
            form = MeepForm(request.POST or None,instance=meep)
            if request.method == "POST":
                if form.is_valid():
                    meep = form.save(commit=False)
                    meep.user = request.user
                    meep.save()
                    messages.success(request, ("Your meep has been updated"))
                    return redirect('home')

            else:
                return render(request,'edit_meep.html',{'form':form,'meep':meep})

        else:
            messages.success(request, ("NO! You don't own that meep"))
            return redirect('home')
    else:
        messages.success(request, ("Please login to continue..."))
        return redirect('home')

def search(request):
    if request.method == "POST":
        search = request.POST['search']
        # Search The database
        searched = Meep.objects.filter(body__contains = search)
        return render(request, 'search.html', {'search':search,'searched':searched})


    else:
        return render(request,'search.html',{})


def search_user(request):
    if request.method == "POST":
        search = request.POST['search']
        # Search The database
        searched = User.objects.filter(username__contains = search)
        return render(request, 'search_user.html', {'search':search,'searched':searched})


    else:
        return render(request,'search_user.html',{})