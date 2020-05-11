from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^dashboard/2$', views.dashboard2, name='dashboard2'),
    url(r'^import/form$', views.import_form2, name='import_form'),

    # url(r'^vazao/delete/(?P<vazao_id>\d+)$', views.vazao_delete, name='vazao_delete'),
    # url(r'^vazao/edit/(?P<vazao_id>\d+)$', views.vazao_edit, name='vazao_edit'),
    # url(r'^vazao/new$', views.vazao_new, name='vazao_new'),
    # url(r'^vazao', views.vazao, name='vazao'),
]
