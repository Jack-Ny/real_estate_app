from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from contacts.models import Contact
#from contacts.models import Contact

# Create your views here.
def register(request):
    if request.method == "POST":
        # Get forms values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nom d\'utilisateur deja pris')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Adresse mail deja utilise')
                    return redirect('register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'Adresse mail deja utilise')
                        return redirect('register')
                    else:
                        # Look good
                        user = User.objects.create_user(
                            username=username, 
                            password=password,
                            email=email, 
                            first_name=first_name, 
                            last_name=last_name)
                        # Login after register
                        # auth.login(request, user)
                        # messages.success(request, 'You are now logged in')
                        # return redirect('index')
                        user.save()
                        messages.success(request, 'Vous etes inscrit. Vous pouvez vous connecter maintenant')
                        return redirect('login')
        else:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')    
                    


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Vous etes connecter maintenant')
            return redirect('dashboard')
        else:
            messages.error(request, 'Informations non valides')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def dashboard(request):
  user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

  context = {
    'contacts': user_contacts
  }
  return render(request, 'accounts/dashboard.html', context)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Vous etes deconnecter maintenant')
        return redirect('index')