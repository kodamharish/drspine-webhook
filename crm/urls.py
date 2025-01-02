from django.urls import path
from .views import *

urlpatterns = [
    path('',user_Login, name='Login'),
    path('Logout/', user_Logout, name='Logout'),


    #Super admin
    path('SA_Dashboard/', sa_Dashboard, name='SA_Dashboard'),
    path('register/superAdmin/', sa_Register_SuperAdmin, name='SA_register_superAdmin'),
    path('register/company/', sa_Register_Company, name='SA_register_company'),
    path('register/user/', sa_Register_User, name='SA_register_user'),
    path('manage_SuperAdmin/', manage_SuperAdmin, name='manage_SuperAdmin'),
    path('manage_Company/', manage_Company, name='manage_Company'),
    path('manage_User/', manage_User, name='manage_User'),


    
    path('admin_dashboard/', admin_profiles, name='admin_dashboard'),
    #path('user_dashboard/',user_dashboard,name='dashboard'),

    # Template Section
    path('CreateTemplate/', CreateTemplate, name='CreateTemplate'),
    path('ManageTemplate/', ManageTemplate, name='ManageTemplate'),
    path('DeleteTemplate/<int:id>/', DeleteTemplate, name='DeleteTemplate'),

    # Contacts and Groups Section
    path('CreateGroup/',CreateGroup,name='CreateGroup'),
    path('GroupContacts/',GroupContacts,name='GroupContacts'),

    path('SingleContactUpload/',ManualContactUpload, name='SingleContactUpload'),
    path('ContactExcelUpload/', upload_excel, name='ContactExcelUpload'),
    
    path('ManageGroup/',ManageGroup,name='ManageGroup'),
    
    path('DeleteGroup/<int:id>',DeleteGroup,name='DeleteGroup'),

    path('ManageGroupContacts/<int:group_id>/',ManageGroupContacts,name='ManageGroupContacts'),
    path('DeleteGroupContact/<int:contact_id>/', DeleteGroupContacts, name='DeleteGroupContact'),

    # path('CheckNumber/',CheckNumber,name='CheckNumber'),
    # path('Check/',NumberCheck,name='Check'),
    
    #Compose Section
    path('Dashboard/', Dashboard, name='Dashboard'),
    path('SingleMessage/',SingleMessage,name='SingleMessage'),
    path('GroupMessage/',GroupMessage,name='GroupMessage'),

    #APIs
    path('api/single-message/', SingleMessageAPI.as_view(), name='single-message-api'),
    path('api/single-message-with-variable/', SingleMessageWithVariableAPI.as_view(), name='single-message-with-variable'),
    path('api/single-message-with-multiple-variable/', SingleMessageWithListVariablesAPI.as_view(), name='single-message-with-variable'),



    # Message Los
    path('MessageLogs/', Message_logs, name='MessageLogs'),





    path('base/',base, name='base'),
    path('home/',home, name='home'),
    path('pushsms/',pushsms, name='pushsms'),
    path('pushvoicesms/',pushvoicesms, name='pushvoicesms'),
    path('bussiness/',bussiness, name='bussiness'),
    path('vr/',vr, name='vr'),
    path('pullsms/',pullsms, name='pullsms'),
    path('reports/',reports, name='reports'),
    path('profile/',profile, name='profile'),
    path('complaintbox/',complaintbox, name='complaintbox'),


    path('dynamic/',dynamic,name='dynamic'),
    path('dynamic/message/<int:id>',dynamicmessage,name='dynamicmessage'),


    path('retargeting/',retargeting,name='retargeting'),
    path('retargeting/message/',retargetingmessage,name='retargetingmessage'),

    path('dynamicpdf/',dynamicpdf,name='dynamicpdf'),
    path('dynamicpdf/message/<int:id>',dynamicpdfmessage,name='dynamicpdfmessage'),

    path('singlecatalog/',singlecatalog,name='singlecatalog'),
    path('singlecatalog/message/<int:id>',singlecatalogmessage,name='singlecatalogmessage'),



    #live chart
    path('livechat/startchat/',startchat,name='startchat'),
    path('livechat/new/',livechatnew,name='livechatnew'),
    path('livechat/addagent/',addagent,name='addagent'),
    path('livechat/manageagent/',manageagent,name='manageagent'),


    
    
    # bot autoresponder
    path('add_bout/',add_bout,name='add_bout'),
    path('managebotautoresponder/',managebotautoresponder,name='managebotautoresponder'),
    path('addcatalogresponder/',addcatalogresponder,name='addcatalogresponder'),
    path('managecatalogresponder/',managecatalogresponder,name='managecatalogresponder'),

    # WA Flow
    path('addflow/',addflow,name='addflow'),
    path('manageflow/',manageflow,name='manageflow'),
    path('addKeywordToFlow/',addKeywordToFlow,name='addKeywordToFlow'),
    path('WAFlowReports/',WAFlowReports,name='WAFlowReports'),


    # drip campaigns
    path('createDripCampaign/',createDripCampaign,name='createDripCampaign'),
    path('manageDripCampaign/',manageDripCampaign,name='manageDripCampaign'),
    path('manageDripCampaign/edit/',manageDripCampaignedit,name='manageDripCampaignedit'),
    path('addnumbertodrip/',addnumbertodrip,name='addnumbertodrip'),
    path('addbrtodrip/',addbrtodrip,name='addbrtodrip'),
    






    path('incomingreplay/',incomingreplay,name='incomingreplay'),
    path('repliesexcel/',repliesexcel,name='repliesexcel'),
    path('sendreports/',sendreports,name='sentreports'),
    path('sendexcelreports/',sendexcelreports,name='sentexcelreports'),
    
    
]