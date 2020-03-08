from django.shortcuts import render,redirect,Http404
from . models import Image,Profile,Comment,Follow
from .forms import NewImageForm,CommentForm,ProfileUpdateForm


def homepage(request):
    if request.user.is_authenticated:
        return redirect(posted)
    else:
        return  redirect('/accounts/login')



def photos(request):
    current_user=request.user
    if request.method == 'POST':
        form=NewImageForm(request.POST , request.FILES)
        if form.is_valid():
            imagess=form.save(commit=False)
            imagess.profile=current_user
            imagess.save()
        return redirect('homepage')
    else:
        form=NewImageForm()
    return  render(request,'createimage.html',{"form":form})


def posted(request):
    posted=Image.allimages()
    return  render(request,'posted.html',{"posted":posted})
def imageid(request, image_id):
    try:
        posted = Image.allimages()
        image = Image.objects.get(id=image_id)
    except Exception:
        raise Http404()
    return render(request, "imageid.html", {"image":image,"posted":posted})


def comment(request, image_id):
    comments = Comment.objects.filter(image_id=image_id)
    current_image = Image.objects.get(id=image_id)
    current_user = request.user

    if request.method == 'POST':

        form = CommentForm(request.POST)


        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = current_user
            comment.image_id = current_image
            current_image.comments_number += 1
            current_image.save_image()
            comment.save()

            return redirect(posted)
    else:
        form = CommentForm()
    return render(request, 'comment.html', {"form": form, "comments": comments})







def updatemyprofile(request):
    current_user = request.user
    try:
        myprofile = Profile.objects.get(user_id = current_user.id)
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST,request.FILES)

            if form.is_valid():
                myprofile.profile_photo = form.cleaned_data['profile_photo']
                myprofile.bio = form.cleaned_data['bio']
                myprofile.username = form.cleaned_data['username']
                myprofile.save_profile()
                return redirect( myprofile )
        else:
            form = ProfileUpdateForm()
    except:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST,request.FILES)

            if form.is_valid():
                createprofile= Profile(profile_photo= form.cleaned_data['profile_photo'],bio = form.cleaned_data['bio'],username = form.cleaned_data['username'],user = current_user)
                createprofile.save_profile()
                return redirect( myprofile )
        else:
            form = ProfileUpdateForm()


    return render(request,'createprofile.html',{"current_user":current_user,"form":form})

def myprofile(request):
    current_user = request.user
    posted=Image.objects.filter(profile_id=current_user.id)
    profile = Profile.objects.get(user = current_user)
    following = Follow.objects.filter(follower=current_user)
    followers = Follow.objects.filter(user=profile)
    return render(request, 'profile.html',{"profile": profile, "current_user": current_user, "following": following, "followers": followers,"posted":posted})


def follow(request,profile_id):
    current_user = request.user
    requested_profile = Profile.objects.get(id = profile_id)
    personfollowing = Follow.objects.filter(follower = current_user,user = requested_profile).count()
    follow = Follow.objects.filter(follower = current_user,user = requested_profile)

    if personfollowing == 0:
        follower = Follow(follower = current_user,user = requested_profile)
        follower.save()
        return redirect(allfollowers)
    else:
        follow.delete()
        return redirect(allfollowers)

def allfollowers(request):
    allfollowers = Profile.objects.all()
    return render(request,'allfollowers.html',{"allfollowers":allfollowers})











# Create your views here.