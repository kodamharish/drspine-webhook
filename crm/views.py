from django.shortcuts import render

# Create your views here.




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import *
from django.shortcuts import get_object_or_404

import requests
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

def send_message(phone_number, template, media_id=None, media_type=None, variables=None):
    url = "https://graph.facebook.com/v21.0/446402058564779/messages"
    headers = {
        "Authorization": "Bearer EAAGDQdUOFfUBO5H24wotZAqmZBswF2McQ4epf65lHpsZBx4IxtIAufOvUfZAObQjnWEaYOFMK85UmHySZCbKwdHRQm6AZBaM1WQ13nTmka2pqpwPlWvQufb0xoYVAWtQhlORnGsQsDwznPcB6ZA3RXJVPwkZBHEixuwhZBEd9NKwvJuQJvqxqJAhmQxhSW3wMorsQriDTxefz64XPWzMUjknCQk9iIHNniunZAkZAcqNAGm",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": template.name,
            "language": {
                "code": "en_US"
            },
            "components": []
        }
    }

    # Adding media if provided
    if media_id and media_type:
        data['template']['components'].append({
            "type": "header",
            "parameters": [
                {
                    "type": media_type,
                    media_type: {"id": media_id}
                }
            ]
        })
    
    # Adding variables if provided
    if variables:
        data['template']['components'].append({
            "type": "body",
            "parameters": [{"type": "text", "text": var} for var in variables]
        })

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json() 
    response_status = "Sent" if response.status_code == 200 else "Failed"
    
    if response.status_code == 200:
        print(f"Message sent successfully to {phone_number}!")
    else:
        print(f"Failed to send message to {phone_number}. Response:", response_data)

    # Logging the message attempt
    MessageLog.objects.create(
        template_name=template.name,
        mobile_number=phone_number,
        status=response_status,
    )

    return response


def Media_Id_Generator(media_file):
    url = "https://graph.facebook.com/v21.0/446402058564779/media"
    headers = {
        "Authorization": "Bearer EAAGDQdUOFfUBO5H24wotZAqmZBswF2McQ4epf65lHpsZBx4IxtIAufOvUfZAObQjnWEaYOFMK85UmHySZCbKwdHRQm6AZBaM1WQ13nTmka2pqpwPlWvQufb0xoYVAWtQhlORnGsQsDwznPcB6ZA3RXJVPwkZBHEixuwhZBEd9NKwvJuQJvqxqJAhmQxhSW3wMorsQriDTxefz64XPWzMUjknCQk9iIHNniunZAkZAcqNAGm"
    }
    files = {
        'file': (media_file.name, media_file, media_file.content_type),
        'type': (None, 'image' if 'image/' in media_file.content_type else 'video'),
        'messaging_product': (None, 'whatsapp')
    }
    response = requests.post(url, headers=headers, files=files)
    return response.json().get("id") if response.status_code == 200 else None


def user_Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        Super_admin = SuperAdmin.objects.filter(sa_username=username).first()
        user = User.objects.filter(username=username).first()

        if Super_admin:
            if check_password(password, Super_admin.sa_password):
                request.session['username'] = Super_admin.sa_username
                # request.session['company_id'] = None  # SuperAdmin doesn't have a company
                messages.success(request, 'Login Successful!')
                return redirect('SA_Dashboard')
            else:
                messages.error(request, 'Invalid Username or Password!')
        elif user:
            if check_password(password, user.password):
                request.session['username'] = user.username
                request.session['company_id'] = user.company_id

                if user.user_role == "Admin":
                    messages.success(request, 'Login Successful!')
                    return redirect('admin_dashboard')
                # else:
                #     messages.success(request, 'Login Successful!')
                #     return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid Username or Password!')
        else:
            messages.error(request, 'User does not exists!')
        
        return render(request, 'app_template/login.html')
    else:
        return render(request, 'app_template/login.html')


def user_Logout(request):
    request.session.flush()
    messages.success(request, 'Logout Successful!')
    return redirect('Login')

# Super Admin Views
def sa_Dashboard(request):
    return render(request, 'SA/sa_dashboard.html')

def sa_Register_SuperAdmin(request):
    if request.method == 'POST':
        full_name = request.POST.get('sa_full_name')
        email = request.POST.get('sa_email')
        username = request.POST.get('sa_username')
        password = request.POST.get('sa_password')
        
        SuperAdmin.objects.create(

            sa_full_name = full_name,
            sa_email = email,
            sa_username = username,
            sa_password = password
            )
        
        return redirect('manage_SuperAdmin')  # Redirect to a suitable page after registration

    return render(request, 'SA/sa_Register_SuperAdmin.html')

def sa_Register_Company(request):
    return render(request, 'SA/sa_Register_Company.html')

def sa_Register_User(request):
    return render(request, 'SA/sa_Register_User.html')

def manage_SuperAdmin(request):
    sa = SuperAdmin.objects.all()
    context = {
        'superAdmins': sa,
    }
    return render(request, 'SA/sa_Manage_SuperAdmin.html', context)

def manage_Company(request):
    companies = Company.objects.all()
    context = {
        'companies': companies,
    }
    return render(request, 'SA/sa_Manage_Company.html', context)

def manage_User(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'SA/sa_Manage_User.html', context)

# User Views
def admin_profiles(request):

    return render(request, 'compose/dashboard.html')



#Template Section


def CreateTemplate(request):
    company_username = request.session.get('username')
    user = User.objects.get(username=company_username)
    if request.method == 'POST':
        name = request.POST.get('name')
        language = request.POST.get('language')
        category = request.POST.get('category')
        template_type = request.POST.get('template_type')
        message = request.POST.get('message')
        
        Template.objects.create(
            company=user.company,
            name=name,
            language=language,
            category=category,
            template_type=template_type,
            message=message
        )
        return redirect('ManageTemplate')

    templates = Template.objects.filter(company=user.company)

    return render(request, 'Templates/CreateTemplate.html', {'templates': templates})

def ManageTemplate(request):
    company_id = request.session.get('company_id')
    data = Template.objects.filter(company_id=company_id)
    print(data)
    return render(request, 'Templates/ManageTemplate.html', {'data': data})

def DeleteTemplate(request, id):
    temp = get_object_or_404(Template, id=id)
    temp.delete()
    return redirect('ManageTemplate')

# Contacts and Groups Section

# Group whatsapp

def CreateGroup(request):
    company_id = request.session.get('username')
    g_id = User.objects.get(username=company_id)
    if request.method == 'POST':
        g_name = request.POST.get('name')
        g_description = request.POST.get('description')

        WhatsApp_Group.objects.create(
            company=g_id.company,
            group_name=g_name,
            group_description=g_description
        )
        return redirect('ManageGroup')

    groups = WhatsApp_Group.objects.filter(company_id=company_id)
    return render(request, 'GroupWhatsApp/CreateGroup.html', {'group': groups})

def ManageGroup(request):
    company_id = request.session.get('company_id')
    groups = WhatsApp_Group.objects.filter(company_id=company_id)
    return render(request, 'GroupWhatsApp/ManageGroup.html', {'group': groups})

def DeleteGroup(request,id):
    group=WhatsApp_Group.objects.get(id=id)
    group.delete()
    return redirect('ManageGroup')

def GroupContacts(request):
    return render(request,'GroupWhatsApp/AddContacts.html')

def ManualContactUpload(request):
    company_id = request.session.get('company_id')
    if request.method == 'POST':
        group_id =request.POST.get('group')
        group = get_object_or_404(WhatsApp_Group,id=group_id)
        number = request.POST.get('numbers')
        name = request.POST.get('name')
        email = request.POST.get('email')
        cname = request.POST.get('cname')


        # Split the input into individual numbers (assuming they are comma-separated)
        numbers_list = number.split(',')

        any_existing_number = False

        for number in numbers_list:
            number = number.strip()  # Remove any extra whitespace
            # Validate number format (e.g., length and digits only)
            if len(number) == 10 and number.isdigit():
                #check if the number alredy exists in the group
                if not Group_Contacts.objects.filter(group=group,number=number).exists():
                    Group_Contacts.objects.create(
                        group=group,
                        number=number,
                        name=name,
                        email = email,
                        company_name = cname,
                        )
                else:
                    messages.error(request, f"The Number {number} already exists in the group {group.group_name}")
                    any_existing_number = True
            else:
                messages.error(request, f"Invalid number format: {number}")
                any_existing_number = True
        if any_existing_number:
            return redirect ('SingleContactUpload')
        else:
            return redirect ('ManageGroup')
    groups = WhatsApp_Group.objects.filter(company_id=company_id)
    return render(request, 'GroupWhatsApp/UploadManual.html', {'group': groups})

import pandas as pd


def upload_excel(request):
    if request.method == 'POST':
        group_id = request.POST.get('group')
        group = WhatsApp_Group.objects.get(pk=group_id)

        # Handle file upload
        excel_file = request.FILES['file']
        print(excel_file)

        if excel_file.name.endswith('.xlsx'):
            df = pd.read_excel(excel_file)

            total_uploaded = 0  # Initialize counter for uploaded contacts

            # Assuming phone numbers are in the first column (index 0), names in the second (index 1), and emails in the third (index 2)
            for _, row in df.iterrows():
                # Handle potential empty cells beyond the expected columns
                number = str(row.iloc[0]) if not pd.isnull(row.iloc[0]) else None
                name = str(row.iloc[1]) if len(row) > 1 and not pd.isnull(row.iloc[1]) else None
                email = str(row.iloc[2]) if len(row) > 2 and not pd.isnull(row.iloc[2]) else None
                cname = str(row.iloc[3]) if len(row) > 3 and not pd.isnull(row.iloc[3]) else None

                # Check if number already exists for the group to avoid duplicates
                if number and not Group_Contacts.objects.filter(group=group, number=number).exists():
                    Group_Contacts.objects.create(group=group, number=number, name=name, email=email, company_name=cname)
                    total_uploaded += 1  # Increment counter for each new contact uploaded
                else:
                    print(f"Skipping duplicate or invalid contact: {number}, {name}, {email}")

            # Display success message using Django messages framework
            messages.success(request, f'{total_uploaded} contacts uploaded successfully to group "{group.group_name}"')
            print(total_uploaded)
            return redirect('ContactExcelUpload')  # Redirect to success page or another view

    # If GET request or form is not valid, render the upload form
    groups = WhatsApp_Group.objects.all()
    return render(request, 'GroupWhatsApp/UploadExcel.html', {'groups': groups})


def ManageGroupContacts(request, group_id):
    group = get_object_or_404(WhatsApp_Group, pk=group_id)
    return render(request, 'GroupWhatsApp/ManageGroupContacts.html', {'group': group})

def DeleteGroupContacts(request, contact_id):
    contact = get_object_or_404(Group_Contacts, id=contact_id)
    group_id = contact.group.id  # Get the group ID before deleting the contact
    contact.delete()
    return redirect('ManageGroupContacts', group_id=group_id)

def SingleMessage(request):
    if request.method == 'POST':
        phone_number = request.POST.get('mobile_number')
        template_id = request.POST.get('template')
        template_variable = request.POST.get('template_variable')
        media_file = request.FILES.get('uploadFile') if 'uploadFile' in request.FILES else None

        try:
            template = Template.objects.get(pk=template_id)
            media_id = None
            media_type = None

            # Generate media ID if a file is uploaded
            if media_file:
                media_id = Media_Id_Generator(media_file)
                media_type = 'image' if media_file.content_type.startswith('image/') else 'video' if media_file.content_type.startswith('video/') else 'document'

            variables = [template_variable] if template_variable else None
            
            send_message(phone_number, template, media_id, media_type, variables)
            return redirect('SingleMessage')
        except ObjectDoesNotExist:
            return redirect('TemplateNotFound')

    templates = Template.objects.all()
    return render(request, 'compose/message.html', {'templates': templates})


























from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class SingleMessageAPI(APIView):
    def post(self, request):
        # Extract and validate the required fields
        mobile_number = request.data.get('mobile_number')
        template_name = request.data.get('template_name')

        if not mobile_number or not template_name:
            return Response(
                {"error": "Both 'mobile_number' and 'template_name' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Retrieve the template by name
            template = Template.objects.get(name=template_name)

            # Call the send_message function
            response = send_message(mobile_number, template)

            if response.status_code == 200:
                return Response({"message": "Message sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Failed to send message.", "details": response.json()},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ObjectDoesNotExist:
            return Response(
                {"error": f"Template with name '{template_name}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SingleMessageWithVariableAPI(APIView):
    def post(self, request):
        # Extract and validate the required fields
        mobile_number = request.data.get('mobile_number')
        template_name = request.data.get('template_name')
        template_variable = request.data.get('template_variable')

        if not mobile_number or not template_name or not template_variable:
            return Response(
                {"error": "All fields 'mobile_number', 'template_name', and 'template_variable' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Retrieve the template by name
            template = Template.objects.get(name=template_name)

            # Call the send_message function
            variables = [template_variable]  # Pass variables as a list
            response = send_message(mobile_number, template, variables=variables)

            if response.status_code == 200:
                return Response({"message": "Message sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Failed to send message.", "details": response.json()},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ObjectDoesNotExist:
            return Response(
                {"error": f"Template with name '{template_name}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class SingleMessageWithListVariablesAPI(APIView):
    def post(self, request):
        # Extract required fields from the request
        mobile_number = request.data.get('mobile_number')
        template_name = request.data.get('template_name')
        template_variables = request.data.get('template_variable', [])

        # Validate fields
        if not mobile_number or not template_name:
            return Response(
                {"error": "Fields 'mobile_number' and 'template_name' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(template_variables, list):
            return Response(
                {"error": "'template_variable' must be a list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Retrieve the template by name
            template = Template.objects.get(name=template_name)

            # Call the send_message function
            response = send_message(mobile_number, template, variables=template_variables)

            if response.status_code == 200:
                return Response({"message": "Message sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Failed to send message.", "details": response.json()},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ObjectDoesNotExist:
            return Response(
                {"error": f"Template with name '{template_name}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def GroupMessage(request):
    if request.method == 'POST':
        group_id = request.POST.get('businessNumber')
        template_id = request.POST.get('template')
        media_file = request.FILES.get('uploadFile') if 'uploadFile' in request.FILES else None

        try:
            group = WhatsApp_Group.objects.get(pk=group_id)
            template = Template.objects.get(pk=template_id)
            media_id = None
            media_type = None

            # Generate media ID and determine the media type if a file is uploaded
            if media_file:
                media_id = Media_Id_Generator(media_file)
                media_type = 'image' if 'image/' in media_file.content_type else 'video' if 'video/' in media_file.content_type else 'document'

            # Send messages to all contacts in the group using the related name 'numbers'
            for contact in group.numbers.all():
                # Check if the template expects variables
                variables = [contact.name] if contact.name and "{{1}}" in template.message else None
                
                send_message(contact.number, template, media_id, media_type, variables)
            
            return redirect('GroupMessage')
        except ObjectDoesNotExist:
            return redirect('GroupOrTemplateNotFound')

    groups = WhatsApp_Group.objects.all()
    templates = Template.objects.all()
    return render(request, 'compose/groupmessage.html', {'templates': templates, 'groups': groups})



def dynamic(request):
    templates = Template.objects.all()
    return render(request,'compose/dynamic.html',{'templates': templates})

def dynamicmessage(request,id):
    temp=Template.objects.get(id=id)
    return render(request,'compose/dynamicmessage.html',{'temp':temp})

def retargeting(request):
    return render(request,'compose/retargeting.html')

def retargetingmessage(request):
    return render(request,'compose/retargetingmessage.html')

def dynamicpdf(request):
    templates = Template.objects.all()
    return render(request,'compose/dynamicpdf.html',{'templates': templates})

def dynamicpdfmessage(request,id):
    temp=Template.objects.get(id=id)
    return render(request,'compose/dynamicpdfmessage.html',{'temp':temp})

def singlecatalog(request):
    templates = Template.objects.all()
    return render(request,'compose/singlecatlog.html',{'templates': templates})

def singlecatalogmessage(request,id):
    temp=Template.objects.get(id=id)
    return render(request,'compose/singlecatalogmessage.html',{'temp':temp})

def Dashboard(request):
    return render (request, 'compose/dashboard.html')


def base(request):
    username=request.session.get('username')

    context = {'username':username}
    return render(request,'base/base.html', context)

def home(request):
    return render(request,'app_template/home.html')

def pushsms(request):
    return render(request,'app_template/pushsms.html')

def pushvoicesms(request):
    return render(request,'app_template/pushvoicesms.html')

def bussiness(request):
    return render(request,'app_template/bussiness.html')

def vr(request):
    return render(request,'app_template/vr.html')

def pullsms(request):
    return render(request,'app_template/pullsms.html')

def reports(request):
    return render(request,'app_template/reports.html')

def profile(request):
    return render(request,'app_template/profile.html')

def complaintbox(request):
    return render(request,'app_template/complaintbox.html')


# livechat
def startchat(request):
    return render(request,'livechat/startchat.html')

def livechatnew(request):
    return render(request,'livechat/whatsappchat.html')

def addagent(request):
    return render(request,'livechat/addagent.html')

def manageagent(request):
    return render(request,'livechat/manageagent.html')








# bot autoresponder
def add_bout(request):
    return render(request,'botautoresponder/add_bout.html')

def managebotautoresponder(request):
    return render(request,'botautoresponder/managebotautoresponder.html')

def addcatalogresponder(request):
    return render(request,'botautoresponder/addcatalogresponder.html')

def managecatalogresponder(request):
    return render(request,'botautoresponder/managecatalogresponder.html')

# WA Flow
def addflow(request):
    return render(request,'waflow/addflow.html')

def manageflow(request):
    return render(request,'waflow/manageflow.html')

def addKeywordToFlow(request):
    return render(request,'waflow/addKeywordToFlow.html')

def WAFlowReports(request):
    return render(request,'waflow/WAFlowReports.html')


## drip campaigns ##
def createDripCampaign(request):
    return render(request,'dripcampaign/createDripCampaign.html')

def manageDripCampaign(request):
    return render(request,'dripcampaign/manageDripCampaign.html')

def manageDripCampaignedit(request):
    campaign_name = "Campaign 10"
    return render(request,'dripcampaign/manageDripCampaignedit.html',{'campaign_name': campaign_name})

def addnumbertodrip(request):
    return render(request,'dripcampaign/addnumbertodrip.html')

def addbrtodrip(request):
    return render(request,'dripcampaign/addbrtodrip.html')



##WA Report##
def incomingreplay(request):
    return render(request,'wareports/IncomingReports.html')

def repliesexcel(request):
    return render(request,'wareports/repliesexcel.html')

def sendreports(request):
    return render(request,'wareports/sentReports.html')

def sendexcelreports(request):
    return render(request,'wareports/sentExcelReports.html')

def Message_logs(request): 

    logs = MessageLog.objects.all().order_by('-timestamp')  # Most recent logs first
    context = {
        'logs': logs,
        'custom_user': request.user
    }
    return render(request, 'Message_Logs/Message_logs.html', context)




