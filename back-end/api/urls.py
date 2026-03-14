from django.urls import path
from . import views

urlpatterns = [
    path("user/register/", views.CreateUserView.as_view(), name="register"),
    path("user/me/", views.CurrentUserView.as_view(), name="current-user"),
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("batiments/", views.BatimentListCreate.as_view(), name="batiment-list"),
    path("batiments/<int:pk>/", views.BatimentDetail.as_view(), name="batiment-detail"),
    path("salles/", views.SalleListCreate.as_view(), name="salle-list"),
    path("salles/<int:pk>/", views.SalleDetail.as_view(), name="salle-detail"),
    path("affectations/", views.AffectationSalleListCreate.as_view(), name="affectation-list"),
    path("affectations/<int:pk>/", views.AffectationSalleDetail.as_view(), name="affectation-detail"),
    path("infos/", views.InfosEssentiellesListCreate.as_view(), name="infos-list"),
    path("infos/<int:pk>/", views.InfosEssentiellesDetail.as_view(), name="infos-detail"),
    path("documents/", views.DocumentListCreate.as_view(), name="document-list"),
    path("documents/<int:pk>/", views.DocumentDetail.as_view(), name="document-detail"),
    path("dashboard/stats/", views.DashboardStatsView.as_view(), name="dashboard-stats"),
    path("users/<int:pk>/role/", views.UserRoleUpdateView.as_view(), name="user-role-update"),
]