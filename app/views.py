import zipfile
from io import StringIO
from django.http import FileResponse
import io
# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Apply_form, RegForm, login_form, adddata, jobForm
from .models import *
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import EmailMessage
from . import certificate_py, offer
from uuid import uuid4

# Google calender
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Create your views here.


def sign_up(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = RegForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.is_staff = True
            data.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(
                email=email, password=raw_password, is_staff=True)
            login(request, account)
            return redirect("admin")
        else:
            return render(request, "page/signup.html", {"form": RegForm(request.POST)})
    login_data = {
        "form": RegForm(),
    }
    return render(request, "page/signup.html", login_data)


def logout_view(request):
    logout(request)
    return redirect("admin")


def login_view(request, *args, **kwaegs):
    user = request.user
    if user.is_authenticated:
        return redirect("admin")
    if request.POST:
        form = login_form(request.POST)
        email = request.POST['email']
        raw_password = request.POST['password']
        account = authenticate(email=email, password=raw_password)
        if account is not None and account.is_staff == True:
            login(request, account)
            return redirect("admin")
        else:
            return render(request, "page/login.html", {"form": login_form(), "nologin": f" Email id or Password is incorrect"})
    return render(request, "page/login.html", {"form": login_form()})

def home(request):

    data = request.session.get('score', False)
    if data:
        del request.session['score']
    con = {
        "data": Job.objects.all(),
        "score": data,
    }
    return render(request, "page/home.html", con)


@login_required(login_url='/login/')
def admin(request):
    data = Apply.objects.all()
    if request.POST:
        # try:
        summary = request.POST["summary"]
        description = request.POST["description"]
        start = request.POST["start"] + ":00"
        end = request.POST["end"] + ":00"
        interview = request.POST["interview"]
        creds = None
        if os.path.exists('app/credentials/token.json'):
            creds = Credentials.from_authorized_user_file(
                'app/credentials/token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'app/credentials/desktop.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('app/credentials/token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end,
                'timeZone': 'Asia/Kolkata',
            },
            "conferenceData": {"createRequest": {"requestId": str(uuid4()), "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
        }
        event = service.events().insert(calendarId='primary', body=event,
                                        conferenceDataVersion=1).execute()
        interviewData = Apply.objects.get(pk=interview)
        saveData = EventDb(title=summary, description=description, meetUrl=event.get(
            'hangoutLink'), email=interviewData.email_id, start_time=start, end_time=end)
        saveData.save()
        emailid = interviewData.email_id
        name = interviewData.f_name
        googlemeet = str(event.get('hangoutLink'))
        try:
            temp = InterviewTemp.objects.get(pk=1)
        except:
            data = InterviewTemp(id = 1,text = "hi {name},<br>The google meet link for {name} <br>email id - {emailid}<br><h3>{googlemeet}<h3>")
            data.save()
            temp = InterviewTemp.objects.get(pk=1)
        message = (temp.text).replace('\r\n', "<br>").replace(
            "{emailid}", emailid).replace("{name}", name).replace("{googlemeet}", googlemeet)
        msg = EmailMessage(
            'Interview',
            message,
            'pallavraj23102000@gmail.com',
            [f'{interviewData.email_id}']
        )
        msg.content_subtype = "html"
        msg.send()
        # except:
        #     return redirect("nosuccess")
        return redirect("success")
    return render(request, "page/admin_main.html", {"data": data})


@login_required(login_url='/login/')
def sendassignment(request, id):
    seereq = AssignmentTemp.objects.all()
    if request.POST:
        type = request.POST["type"]
        reqData = AssignmentTemp.objects.get(type=type)
        return render(request, "page/sendassignment.html", {"typeData": reqData, "seetype": seereq, "id": id})
    return render(request, "page/sendassignment.html", {"seetype": seereq, "id": id})


@login_required(login_url='/login/')
def mail(request):
    try:
        data = InterviewTemp.objects.get(pk=1)
    except:
        data = ""
    if request.POST:
        try:
            reqData = InterviewTemp(id=1, text=request.POST["text"])
            reqData.save()
            return redirect("mail")
        except:
            return redirect("nosuccess")

    return render(request, "page/emailTemp.html", {"typeData": data})


@login_required(login_url='/login/')
def assignmentMail(request):
    seereq = AssignmentTemp.objects.all()
    if request.POST:
        type = request.POST["type"]
        reqData = AssignmentTemp.objects.get(type=type)
        return render(request, "page/assignTemp.html", {"typeData": reqData, "seetype": seereq, "id": id})
    return render(request, "page/assignTemp.html", {"seetype": seereq})


@login_required(login_url='/login/')
def sendassignmentlast(request, id):
    if request.POST:
        try:
            allData = Apply.objects.get(pk=id)
            emailid = allData.email_id
            name = allData.f_name
            stringdata = (request.POST["text"]).replace('\r\n', "<br>").replace(
                "{emailid}", emailid).replace("{name}", name)
            msg = EmailMessage(
                "Assignment",
                stringdata,
                'pallavraj23102000@gmail.com',
                [emailid]
            )
            msg.content_subtype = "html"
            msg.send()
            return redirect("admin")
        except:
            return redirect("nosuccess")
    return redirect("sendassignment")


@login_required(login_url='/login/')
def add_type(request):
    if request.POST["newType"] == "":
        return redirect("nosuccess")
    try:
        data = AssignmentTemp(type=(request.POST["newType"]).lower(), text="")
        data.save()
    except:
        return redirect("nosuccess")
    return redirect("assignment")


@login_required(login_url='/login/')
def delete_type(request):
    data = AssignmentTemp.objects.get(type=request.POST["type"])
    data.delete()
    return redirect("assignment")


@login_required(login_url='/login/')
def success(request):
    return render(request, "page/success.html")


@login_required(login_url='/login/')
def nosuccess(request):
    return render(request, "page/nosuccess.html")


@login_required(login_url='/login/')
def assign_save(request):
    try:
        stringdata = (request.POST["text"])
        see = AssignmentTemp.objects.get(type=request.POST["type"])
        see.text = stringdata
        see.save()
    except:
        return redirect("nosuccess")
    return redirect("success")


@login_required(login_url='/login/')
def interviewDone(request, id):
    data = Apply.objects.get(pk=id)
    data.interview = 1
    data.save()
    return redirect("admin")


@login_required(login_url='/login/')
def assignmentDone(request, id):
    data = Apply.objects.get(pk=id)
    data.assignment = 1
    data.save()
    return redirect("admin")


@login_required(login_url='/login/')
def hire(request, id):
    data = Apply.objects.get(pk=id)
    try:
        data.hired = 1
        data.save()
        a = Apply_candidate(Applyid=data)
        a.save()
        message = f'Hi {data.f_name},<br>' + 'You are Hired'
        msg = EmailMessage(
            'Test',
            message,
            'pallavraj23102000@gmail.com',
            [f'{data.email_id}']
        )
        msg.content_subtype = "html"
        msg.send()
        return redirect("success")
    except:
        return redirect("nosuccess")

def replacern(data):
    arr = []
    for i in data:
        arr.append(i.replace("\r\n",""))
    return arr
@login_required(login_url='/login/')
def admin_add(request):

    con = {
        "form": jobForm(),
        "skill": skill.objects.all()
    }
    if request.POST:
        m = jobForm(request.POST)
        if m.is_valid():
            newForm = m.save(commit=False)
            newForm.creation_date = str(datetime.datetime.now())
            newForm.skills = replacern(request.POST.getlist('skills'))
            newForm.location = replacern(request.POST.getlist('location'))
            newForm.save()
            return redirect("question_edit_home")
        else:
            return render(request, "page/admin_profile.html", con)
    return render(request, "page/admin_profile.html", con)


@login_required(login_url='/login/')
def question_edit_home(request):
    con = {
        "data": Job.objects.all()
    }
    return render(request, "page/question-edit-home.html", con)


@login_required(login_url='/login/')
def formoffer(request):
    data = Apply_candidate.objects.all()
    skillData = skill.objects.all()
    roleData = role.objects.all()
    return render(request,'page/offer.html',{"range":range(1,25),"data":data,"skill":skillData,"role":roleData})
@login_required(login_url='/login/')
def makeformoffer(request):
    if request.POST:
        date = request.POST["date"]
        months = request.POST["months"]
        amount = request.POST["amount"]
        supervisor = request.POST["supervisor"]
        applicant = request.POST.getlist('applicant')
        rolePost = request.POST["role"]
        for i in request.POST:
            if request.POST[i] == "":
                return redirect("nosuccess")
        buff = io.BytesIO()
        archive = zipfile.ZipFile(buff,'w',compression=zipfile.ZIP_DEFLATED)
        for i in applicant:
            see = (Apply_candidate.objects.get(customid=i)).Applyid
            data = offer.offer(date,months,amount,supervisor,see,rolePost)
            buffer = data[0]
            archive.writestr(f'offer_letter_{data[1]}.pdf',buffer.getvalue())
            
        archive.close()
        buff.seek(0) 
        return FileResponse(buff, as_attachment=True, filename='offer.zip')
    return redirect("admin")

@login_required(login_url='/login/')
def formcertificate(request):
    data = Apply_candidate.objects.all()
    skillData = skill.objects.all()
    roleData = role.objects.all()
    return render(request,'page/formcertificate.html',{"range":range(1,25),"data":data,"skill":skillData,"role":roleData})
@login_required(login_url='/login/')
def makeformcertificate(request):
    if request.POST:
        date = request.POST["date"]
        monthPost = request.POST["months"]
        supervisor = request.POST["supervisor"]
        applicant = request.POST.getlist('applicant')
        rolePost = request.POST["role"]
        year, month, day = map(int, date.split('-'))
        date = datetime.date(year, month, day)
        dateto = datetime.date(year, month+ int(monthPost), day)
        for i in request.POST:
            if request.POST[i] == "":
                return redirect("nosuccess")
        buff = io.BytesIO()
        archive = zipfile.ZipFile(buff,'w',compression=zipfile.ZIP_DEFLATED)
        for i in applicant:
            see = (Apply_candidate.objects.get(customid=i)).Applyid
            data = certificate_py.Certificate(date,dateto,supervisor,see,rolePost.replace("\r\n",""))
            buffer = data[0]
            archive.writestr(f'certificate_{data[1]}.pdf',buffer.getvalue())
            
        archive.close()
        buff.seek(0) 
        return FileResponse(buff, as_attachment=True, filename='certificate.zip')
    return redirect("admin")
    

@login_required(login_url='/login/')
def certificate(request):
    return render(request, "page/gencertificate.html")


@login_required(login_url='/login/')
def question_edit_add(request, myid):
    if request.POST:
        data = adddata(request.POST)
        que = Job.objects.get(pk=myid)
        p = data.save(commit=False)
        p.jobid = que
        p.save()
        return redirect("question_edit_home")
    return render(request, "page/question-edit-add.html",{"id":myid})


@login_required(login_url='/login/')
def question_edit_delete(request, myid):
    que = Job.objects.get(pk=myid)
    con = {
        "data": Mcq.objects.filter(jobid=que),
        "id": myid
    }
    return render(request, "page/question-edit-delete.html", con)


@login_required(login_url='/login/')
def question_edit_delete_main(request, myid, delid):
    obj = Mcq.objects.get(pk=delid)
    obj.delete()
    return redirect("question_edit_home")


@login_required(login_url='/login/')
def question_edit_update(request, myid):
    que = Job.objects.get(pk=myid)
    con = {
        "data": Mcq.objects.filter(jobid=que),
        "id": myid
    }
    return render(request, "page/question-edit-update.html", con)


@login_required(login_url='/login/')
def question_edit_update_main(request, myid, delid):
    if request.POST:
        obj = Mcq.objects.get(pk=delid)
        try:
            if request.POST["text"]:
                text = request.POST["text"]
                obj.question = text
                obj.save()
        except:
            pass
        try:
            if request.POST["answer"]:
                answer = request.POST["answer"]
                obj.answer = answer
                obj.save()
        except:
            pass
        try:
            if request.POST["option2"]:
                option2 = request.POST["option2"]
                obj.option2 = option2
                obj.save()
        except:
            pass
        try:
            if request.POST["option3"]:
                option3 = request.POST["option3"]
                obj.option3 = option3
                obj.save()
        except:
            pass

        try:
            if request.POST["option4"]:
                option4 = request.POST["option4"]
                obj.option4 = option4
                obj.save()
        except:
            pass
    return redirect("question_edit_home")


def apply_job(request, myid):
    jobCheck = Job.objects.get(pk=myid)
    if request.POST:
        add = 0
        countData = Mcq.objects.filter(jobid=jobCheck).count()
        for i in Mcq.objects.all().filter(jobid=jobCheck):
            try:
                see = Mcq.objects.get(pk=i.id)
                if see.answer == request.POST[str(i.id)]:
                    add = add + 1
            except:
                pass
        if add == countData:
            first = request.POST["f_name"]
            second = request.POST["l_name"]
            form = Apply_form(request.POST, request.FILES)
            if form.is_valid():
                try:
                    post_added = form.save(commit=False)
                    post_added.jobid = jobCheck
                    post_added.f_name = first.capitalize()
                    post_added.l_name = second.capitalize()
                    arr = []
                    for i in request.POST.getlist("skill"):
                        arr.append(i.replace("\r\n",""))
                    post_added.skill = arr
                    post_added.apply_date = str(
                        datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
                    post_added.score = add
                    post_added.save()
                    request.session['score'] = "Congratulations you have been selected."
                except:
                    request.session['score'] = "Something Went WRONG."
                return redirect('home')
            else:
                apply_job_data = {
                    "form": form,
                    "id": myid,
                    "skill":skill.objects.all()
                }
                return render(request, "page/apply.html", apply_job_data)
        else:
            request.session['score'] = f"You are have scored {add} out of {countData}. Unfortunatly you are not selected"
            return redirect('home')
    mcq = Mcq.objects.all().filter(jobid=jobCheck)
    data = []
    for i in mcq:
        arr = [i.answer, i.option2, i.option3, i.option4]
        random.shuffle(arr)
        if data == []:
            data = [{"question": i.question, "id": i.id, "other": arr}]
        else:
            data.append({"question": i.question, "id": i.id, "other": arr})
    apply_job_data = {
        "data": data,
        "form": Apply_form(),
        "id": myid,
        "skill":skill.objects.all()
    }
    return render(request, "page/apply.html", apply_job_data)


def apply_job_question(request, myid):
    jobCheck = Job.objects.get(pk=myid)
    apply_job_data = {
        "id": myid,
        "que": Mcq.objects.filter(jobid=jobCheck),
    }
    return render(request, "page/apply.html", apply_job_data)


def job_details(request, myid):
    data = Job.objects.get(pk=myid)
    job_details_data = {
        "id": myid,
        "data": data,
        "location": ', '.join(data.location),
        "skills": ', '.join(data.skills),
    }
    return render(request, "page/detail.html", job_details_data)
