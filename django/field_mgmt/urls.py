from django.urls import path

from field_mgmt import views

urlpatterns = [
	path('farms/', views.FarmList.as_view(), name = 'farm_list'),
    path('fields/', views.Index.as_view(), name = 'all_fields'),
    path('fields/<int:pk>/', views.FieldRecord.as_view(), name = 'single_field'),
    path('import/', views.ImportData.as_view(), name = 'import'),
]
