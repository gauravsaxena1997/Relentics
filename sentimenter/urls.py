from django.conf.urls import url
from . import views

from .views import userinput
urlpatterns=[
    url(r'^$index/',views.index,name='index'),
    url(r'^$',views.login,name='login'),
    url(r'^analyze/$',views.analyze,name='analyze'),
    url(r'^postsignin/$',views.postsignin,name='postsignin'),
    url(r'^logout/',views.logout,name="logout"),
    url(r'^signup/',views.signup,name="signup"),
    url(r'^postsignup/',views.postsignup,name="postsignup"),
    url(r'^contact/',views.contact,name="contact"),
    url(r'^postfeedback/',views.postfeedback,name="postfeedback"),
    url(r'^check/',views.check,name="check")

]
app_name='sentimenter'
