from django.shortcuts import render, redirect
from django.contrib import messages
# from django.core.mail import send_mail
from .models import Contact

def contact(request):
  if request.method == 'POST':
    listing_id = request.POST['listing_id']
    listing = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    user_id = request.POST['user_id']
    realtor_email = request.POST['realtor_email']

    #  Check if user has made inquiry already
    if request.user.is_authenticated:
      user_id = request.user.id
      has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
      if has_contacted:
        messages.error(request, 'Vous avez deja fait une demande pour cette annonce')
        return redirect('/listings/'+listing_id)

    contact = Contact(
        listing=listing, 
        listing_id=listing_id, 
        name=name, 
        email=email, 
        phone=phone, 
        message=message, 
        user_id=user_id )
    contact.save()
    
    messages.success(request, 'Votre requete a ete soumis, un agent immobilier vous contactera bientot')
    return redirect('/listings/'+listing_id)
    
    '''# Send email
    send_mail(
        'Property Listing Inquiry',
        'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
        'frenchacting.aac@gmail.com',
        [realtor_email, 'daniel.ach@hotmail.com'],
        fail_silently=False
    )
    '''
    

    

