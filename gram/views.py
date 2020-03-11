from django.shortcuts import render,redirect,Http404
from . models import Image,Profile,Comment,Follow,Like
from .forms import NewImageForm,CommentForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
    if request.user.is_authenticated:
        return redirect(posted)
    else:
        return  redirect('/accounts/login')


@login_required
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

@login_required
def posted(request):
    posted=Image.allimages()
    return  render(request,'posted.html',{"posted":posted})

@login_required
def imageid(request, image_id):
    try:
        posted = Image.allimages()
        image = Image.objects.get(id=image_id)
    except Exception:
        raise Http404()
    return render(request, "imageid.html", {"image":image,"posted":posted})

@login_required
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

@login_required
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




        else:
            form = ProfileUpdateForm()


    return render(request,'createprofile.html',{"current_user":current_user,"form":form})

@login_required
def myprofile(request):
    current_user = request.user
    try:
        profile = Profile.objects.get(user_id=current_user)
        following = Follow.objects.filter(follower=current_user)
        followers = Follow.objects.filter(user=profile)
    except:
        profile = Profile.objects.filter(user_id=current_user)
        following = Follow.objects.filter(follower=current_user)
        followers = Follow.objects.filter(user=profile)
    return render(request, 'profile.html',{"profile": profile, "current_user": current_user, "following": following, "followers": followers,"posted":posted})

@login_required
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


@login_required
def allfollowers(request):
    allfollowers = Profile.objects.all()
    return render(request,'allfollowers.html',{"allfollowers":allfollowers})

@login_required
def like(request, image_id):
    getimage = Image.objects.get(id=image_id)
    current_user = request.user
    likedpic= Like.objects.filter(image=getimage, user=current_user).count()
    unlikedpic = Like.objects.filter(image=getimage, user=current_user)

    if likedpic == 0:
        getimage.likes += 1
        getimage.save_image()
        like = Like(user=current_user, image=getimage)
        like.save_like()
        return redirect(posted)

    else:
        getimage.likes -= 1
        getimage.save_image()
        for unlike in unlikedpic:
            unlike.unlike()
        return redirect(posted)


def search_user(request):
    if 'name' in request.GET and request.GET["name"]:
        search_term=request.GET.get("name")
        searchednames=Profile.findprofile(search_term)
        message=f"{search_term}"
        return render(request,"search.html",{"message":message,"searched":searchednames})

    else:
        message="you haven't searched"
    return render(request,"search.html",{"message":message})


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')













# Create your views here.
