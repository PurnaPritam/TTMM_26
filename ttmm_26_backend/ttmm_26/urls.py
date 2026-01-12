from django.urls import path
from . import views

urlpatterns = [
    path("token", views.CustomTokenObtainPairView.as_view(), name="token_obtain"),
    path("bidding", views.bidding, name="bidding"),
    path("portal_control", views.portal_control, name="portal_control"),
    path("investor_fetch", views.investor_fetch, name="investor_fetch"),
    path("startup_fetch", views.startup_fetch, name="startup_fetch"),
    path("funding_fetch", views.funding_fetch, name="funding_fetch"),
    path("get_own_funding", views.get_own_funding, name="get_own_funding"),
    path("get_investor_profile", views.get_investor_profile, name="get_investor_profile"),
    path("get_startup_investors", views.get_startup_investors, name="get_startup_investors"),
    path("get_funded_investors", views.get_funded_investors, name="get_funded_investors"),
    path("get_investor_funded_startups", views.get_investor_funded_startups, name="get_investor_funded_startups"),
]