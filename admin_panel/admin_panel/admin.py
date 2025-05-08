from django.contrib import admin


class BallsdexAdminSite(admin.AdminSite):
    site_header = "IconDex administration"
    site_title = "IconDex admin panel"
    site_url = None  # type: ignore
    final_catch_all_view = False
