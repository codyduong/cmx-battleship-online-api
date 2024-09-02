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

import core.views as core_views
import user_session.views as user_session_views
import lobby.views as lobby_views


urlpatterns = [
    # core app
    path('health', core_views.health),
    path('shealth', core_views.shealth),
    # user session
    path('info', user_session_views.get_online_player_count),
    path('login', user_session_views.create_session_login),
    path('logout', user_session_views.destory_session_logout),
    # lobby
    path('game/requests', lobby_views.GameRequestView.as_view())
]
