from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import *
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, template_name="store/home.html")


def patient(request):

    if request.method == "POST":
        
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        image= request.FILES['image']

        fs = FileSystemStorage()
        filename = fs.save(image.name, image) # Storing image in database with auto generated name:
        url = fs.url(filename)

  

        if User.objects.filter(email=email).exists():
            messages.error(request, "Sorry E-mail is taken")
            return redirect('patient')

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Sorry Username is taken")
            return redirect('patient')

        elif password != confirmpassword:
            messages.error(request,"Password and Confirm password didn't match")
            return redirect('patient')

        else:
            user = User(username=username,first_name=firstname, last_name=lastname,email=email)
            user.set_password(password)                         
            user.save()

            patient = Patient.objects.create(user=user,image=url,address=address,city=city,state=state,pincode=pincode)

            messages.info(request, "Account Created Successfully")
            return redirect('/')

    return render(request, template_name='store/patient.html')


def doctor(request):
    if request.method == "POST":
        
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        image= request.FILES['image']
        
        fs = FileSystemStorage()
        filename = fs.save(image.name, image) # Storing image in database with auto generated name:
        url = fs.url(filename)
 

        if User.objects.filter(email=email).exists():
            messages.error(request, "Sorry E-mail is taken")
            return redirect('patient')

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Sorry Username is taken")
            return redirect('patient')

        elif password != confirmpassword:
            messages.error(request,"Password and Confirm password didn't match")
            return redirect('patient')

        else:
            user = User(username=username,first_name=firstname, last_name=lastname,email=email,is_staff=True)
            user.set_password(password)                         
            user.save()

            doctor = Doctor.objects.create(user=user,image=url,address=address,city=city,state=state,pincode=pincode)

            messages.info(request, "Account Created Successfully")
            return redirect('/')

    return render(request, template_name='store/doctor.html')


def logout_page(request):
    logout(request)
    messages.info(request,"You Logged Out")
    return redirect('/')


def login_page(request):
    if request.method == 'POST':
        is_doctor = request.POST.get('doctor')
        is_patient = request.POST.get('patient')
        login_username = request.POST['usernameL']
        login_password = request.POST['passwordL']
        # print(is_doctor)

        try:
            if is_doctor=='doctor':

                user = authenticate(username = login_username,password = login_password)

                if user:
                    login(request, user)
                    request.session['user_type'] = is_doctor
                    messages.info(request,'You are Logged In')
                    return redirect('/profile')
                
                else:
                    messages.warning(request, 'Invalid Credentials')
                    return redirect('/login')

            if is_patient=='patient':

                user = authenticate(username = login_username,password = login_password)

                if user:
                    request.session['user_type'] = is_patient
                    login(request, user)
                    messages.info(request,'You are Logged In')
                    return redirect('/profile')
                
                else:
                    messages.warning(request, 'Invalid Credentials')
                    return redirect('/login')


        except Exception as e:
            messages.warning(request,'INVALID CREDENTIALS')
            messages.info(request,f'An Error Occured {e}')
            return redirect('/')

    return render(request, template_name='store/login.html')


@login_required
def profile(request):
    # print(request.user)
    user_type = request.session['user_type']
    if user_type == "doctor":        
        user_profile = Doctor.objects.get(user=request.user)
        # print(user_profile.image)

    if user_type == "patient":
        user_profile = Patient.objects.get(user=request.user)

    
    
    context = {'user_profile': user_profile}

    return render(request, 'store/profile.html', context)



@login_required
def bloghome(request):

    mentalhealth = Blogpost.objects.filter(category='mentalhealth')
    heartdisease = Blogpost.objects.filter(category='heartdisease')
    covid19 = Blogpost.objects.filter(category='covid19')
    immunization = Blogpost.objects.filter(category='immunization')

    mh_list=[]
    for mh in mentalhealth:
        if mh.draft == False:
            mh_list.append(mh)

    hd_list=[]
    for hd in heartdisease:
        if hd.draft == False:
            hd_list.append(hd)
    
    cd_list = []
    for cd in covid19:
        if cd.draft == False:
            cd_list.append(cd)
    
    im_list = []
    for im in immunization:
        if im.draft == False:
            im_list.append(im)

    context = { 'mentalhealth':mh_list, 'heartdisease':hd_list, 'covid19':cd_list, 'immunization':im_list }
    print(covid19)
    
    return render(request,'blog/bloghome.html',context)


@login_required
def newpost(request):
    if request.method == "POST":
        author = request.POST.get('author')
        title = request.POST.get('title')
        category = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")
        is_draft = request.POST.get("is_draft")

        # IMAGE
        image= request.FILES['image']
        
        fs = FileSystemStorage()
        filename = fs.save(image.name, image) # Storing image in database with auto generated name:
        url = fs.url(filename)

        user = User.objects.get(username=author)
        writer = Doctor.objects.get(user=user)


        if is_draft == 'on':
            draft = True
        else:
            draft = False

        Blogpost.objects.create(author=writer, title=title, image=url, category=category, summary=summary, content=content, draft=draft)

        messages.success(request, 'The post have been uploaded successfully.')
        return redirect('/mypost')

        
    user_type = request.session['user_type']
    if user_type == "patient":
        # user_profile = Patient.objects.get(user=request.user)
        messages.warning(request, "Sorry Patient can't create a post")
        return redirect('/bloghome')
    
    return render(request, template_name='blog/newpost.html')


@login_required
def mypost(request):

    # user = User.objects.filter(username=request.user).last()
    # author = Doctor.objects.filter(user=user).last()

    user = User.objects.get(username=request.user)
    author = Doctor.objects.get(user=user)
    mypost = Blogpost.objects.filter(author=author)
    
    # print(user,author,mypost)

    user_type = request.session['user_type']
    if user_type == "patient":
        user_profile = Patient.objects.get(user=request.user)
        messages.warning(request, "Sorry Patient can't open MY POST")
        return redirect('/bloghome')

    context = {'mypost':mypost}
    
    return render(request, 'blog/mypost.html',context)

@login_required
def postview(request,id):
    post = Blogpost.objects.get(id=id)

    return render(request, 'blog/postview.html',{'post':post})


@login_required
def updatepost(request,id):
    post = Blogpost.objects.get(id=id)
    # print(post)

    if request.method == "POST":
        # print(post.id)
        # postId = request.POST.get("postId")
        title = request.POST.get("title")
        category = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")
        is_draft = request.POST.get("is_draft")

        post = Blogpost.objects.get(id=post.id)
    
        try:
            image= request.FILES['image']
        
            fs = FileSystemStorage()
            filename = fs.save(image.name, image) # Storing image in database with auto generated name:
            url = fs.url(filename)
        except Exception as e:
            url = post.image

        if summary == "":
            summary = post.summary

        if content == "":
            content = post.content

        if is_draft == 'on':
            draft = True
        else:
            draft = False

        # print(post.title,post.image,post.categorsy,post.summary,post.content,post.draft)
        post.title = title
        post.image = url
        post.category = category
        post.summary = summary
        post.content = content
        post.draft = draft
        post.save()
        # print(post.title,post.image,post.category,post.summary,post.content,post.draft)
        messages.success(request, 'The post have been updated successfully.')
        return redirect('/mypost')

    return render(request, 'blog/updatepost.html',{'post':post})