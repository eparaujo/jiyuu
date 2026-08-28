from django.urls import path
from . import views

urlpatterns = [
    path("technical-programs/",  views.TechnicalProgramListView.as_view(), name="technical_program_list",),
    path("technical-programs/create/", views.TechnicalProgramCreateView.as_view(), name="technical_program_create",),
    path("technical-programs/<int:pk>/", views.TechnicalProgramDetailView.as_view(), name="technical_program_detail",),
    path("technical-programs/<int:pk>/update/", views.TechnicalProgramUpdateView.as_view(), name="technical_program_update",),
    path("technical-programs/<int:pk>/delete/", views.TechnicalProgramDeleteView.as_view(), name="technical_program_delete",),
    # -------------------------------------------------------------------------
    # TechnicalProgramItem - telas
    # -------------------------------------------------------------------------
    path("technical-program-items/", views.TechnicalProgramItemListView.as_view(), name="technical_program_item_list",),
    path("technical-program-items/create/", views.TechnicalProgramItemCreateView.as_view(),  name="technical_program_item_create",),
    path("technical-program-items/<int:pk>/", views.TechnicalProgramItemDetailView.as_view(), name="technical_program_item_detail",),
    path("technical-program-items/<int:pk>/update/", views.TechnicalProgramItemUpdateView.as_view(), name="technical_program_item_update", ),
    path("technical-program-items/<int:pk>/delete/", views.TechnicalProgramItemDeleteView.as_view(), name="technical_program_item_delete",),
    #endpoint para o app
    path("api/v1/technical-programs/", views.TechnicalProgramListAPIView.as_view(), name="technical_program_list_api",),
    path("api/v1/technical-programs/next/", views.TechnicalProgramNextAPIView.as_view(), name="technical_program_next_api",),
    path("api/v1/technical-programs/<int:pk>/", views.TechnicalProgramDetailAPIView.as_view(), name="technical_program_detail_api",),    
]