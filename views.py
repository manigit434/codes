from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel, UserCipherModel
from django.db.models import Q
# pip install eciespy
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import binascii


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHome.html', {})

def dataview(request):
    import pandas as pd 
    from django.conf import settings
    import numpy
    path = settings.MEDIA_ROOT + '//' + 'tripadvisor_hotel_reviews.csv'
    dataset = pd.read_csv(path)
    dataset = dataset.to_html
    return render(request,'users/dataset.html',{'dataset':dataset})

def Model_Results(request):
    from .utility import ml
    nb_report = ml.build_naive_bayes()
 
    dt_report = ml.build_decsionTree()
    rf_report = ml.build_randomForest()
    svm_report = ml.build_svm()
    return render(request, 'users/Training.html', {'nb': nb_report, 'dt': dt_report, 'rf': rf_report, 'svm': svm_report})

def prediction1(request):
    if request.method=='POST':
        from .utility import ml
        joninfo  = request.POST.get('joninfo')
        result = ml.predict_userInput(joninfo)
        print(request)
        return render(request, 'users/Prediction.html', {'result': result})
    else:
        return render(request,'users/Prediction.html',{})


def prediction(request):
    if request.method=='POST':
        from .utility import sentiment_analysis
        joninfo  = request.POST.get('joninfo')
        aspect_clauses,mapped_feature,sentiment = sentiment_analysis.prediction1(joninfo)
        print(request)
        if sentiment > 0.5:
            msg='Good Review'
        elif sentiment>0 and sentiment<0.5:
            msg='partially Review or neutral Review'
        else:
            msg='Its a negitive Review'
        return render(request, 'users/testform.html', {'result': aspect_clauses,'mapped_feature':mapped_feature,'sentiment':msg})
    else:
        return render(request,'users/testform.html',{})
