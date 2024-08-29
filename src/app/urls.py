"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

import app.views as app_views
import user_session.views as user_session_views


urlpatterns = [
    # core app
    path('health', app_views.health),
    path('shealth', app_views.shealth),
    path('login', app_views.login),
    path('lobby', user_session_views.UserSessionView.as_view()),
    path('game/requests', user_session_views.GameRequestView.as_view())
]
