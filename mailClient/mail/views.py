from django.http import HttpResponse
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from mail.models import Email

def loginUser(request):

    username = password = ''

    if request.method == 'GET':
        
        context = ''
        return render(request, 'login.html', {'context': context})

    if request.POST:

        username = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        user = authenticate(request, username=username, password=password)

        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")

            else:
                context = {'error': 'Wrong credentials'}
                return render(request, 'login.html', {'context': context})

@login_required(login_url="login/")
def home(request):
    res = Email.objects.raw('SELECT * FROM mail_email WHERE recipient_email=%s ORDER BY date DESC', [request.user])
    return render(request, "home.html", {'res': res})

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect("/login/")

def send_email(request):

    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from', '')
    to_email = request.POST.get('recipient', '')
    # uploaded_file = request.FILES['attachment']

    # print(subject, message, from_email, to_email, uploaded_file)

    if subject and message and from_email:
        try:
            
            email = EmailMessage(
                subject,
                message,
                from_email,
                [ to_email ],
                headers={'Reply-To': from_email},
            )

            if request.FILES:
                uploaded_file = request.FILES['attachment']
                email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

                email.send(fail_silently=False)

                sent = Email(
                    user_email = from_email,
                    recipient_email = to_email,
                    subject = subject,
                    text = message,
                    attachment = uploaded_file
                )

                sent.save()

            else:
                email.send(fail_silently=False)

                sent = Email(
                    user_email = from_email,
                    recipient_email = to_email,
                    subject = subject,
                    text = message
                )

                sent.save()
            
            

        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Make sure all fields are entered and valid.')

def sent(request):
    res = Email.objects.raw('SELECT * FROM mail_email WHERE user_email=%s ORDER BY date DESC', [request.user])
    return render(request, "sent.html", {'res': res})
