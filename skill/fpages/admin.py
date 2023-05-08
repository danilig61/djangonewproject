from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404

# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )
def page1(request):
    return render(request, 'fpages/page1.html')

def page2(request):
    if request.user.is_authenticated:
        return render(request, 'fpages/page2.html')
    else:
        return render(request, 'fpages/access_denied.html')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Администраторы').exists())
def page3(request):
    flatpage = get_object_or_404(FlatPage, url='/page3/')
    return render(request, 'fpages/page3.html', {'flatpage': flatpage})

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)