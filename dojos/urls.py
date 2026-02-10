from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import DojoMemberUpdateRoleView

urlpatterns = [
    path('dojos/list/', views.DojoListView.as_view(), name='dojo_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('dojos/create/', views.DojoCreateView.as_view(), name='dojo_create'),
    path('dojos/<int:pk>/detail/', views.DojoDetailView.as_view(), name='dojo_detail'),
    path('dojos/<int:pk>/update/', views.DojoUpdateView.as_view(), name='dojo_update'),
    path('dojos/<int:pk>/delete/', views.DojoDeleteView.as_view(), name='dojo_delete'),
    # endpoint a ser usado pelo flutter
    path('api/v1/dojos/', views.DojoListAPI.as_view(), name='api_genres'),
    path("api/v1/dojos/memberships/change-role/", views.ChangeRoleAPIView.as_view(), name="change_role"),
    path("api/v1/dojos/<int:dojo_id>/members/", views.DojoMembersAPIView.as_view(), name="dojo_member"),
    path("dojos/members/<int:pk>/delete/", views.DojoMemberDeleteView.as_view(), name="dojo_member_delete"),
    path("dojos/<int:dojo_id>/members/", views.DojoMemberListView.as_view(), name="dojo_member_list"), #lista 
    path("dojos/members/<int:pk>/edit-role/", views.DojoMemberUpdateRoleView.as_view(), name="dojo_member_edit_role"),
    path("dojos/members/<int:pk>/role/", views.DojoMemberRoleUpdateView.as_view(), name="dojo_member_update_role"),    
    path("dojos/members/<int:pk>/deactivate/", views.DojoMemberDeactivateView.as_view(), name="dojo_member_deactivate"),
    path("dojos/<int:dojo_id>/members/inactive/", views.DojoMemberInactiveListView.as_view(), name="dojo_member_inactive_list"),
    path("dojos/members/<int:pk>/reactivate/", views.DojoMemberReactivateView.as_view(), name="dojo_member_reactivate"),


    path("dojos/members/<int:pk>/active/", views.DojoMemberActiveUpdateView.as_view() ),
] 