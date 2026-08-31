from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .models import Project, ThemeSettings
from django.db.models import Q
from pages.views import get_base_context

def project_index(request):
    projects = Project.objects.all()
    context = get_base_context(request)
    context.update({
        'projects': projects
    })
    return render(request, 'projects/project_index.html', context)

def project_detail(request, slug):
    try:
        project = Project.objects.get(slug=slug)
        context = get_base_context(request)
        context.update({
            'project': project
        })
        return render(request, 'projects/project_detail.html', context)
    except Project.DoesNotExist:
        from django.http import Http404
        raise Http404("Project does not exist")

def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Project.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(technology__icontains=query)
        ).distinct()
    
    context = get_base_context(request)
    context.update({
        'query': query,
        'results': results,
    })
    return render(request, 'projects/search_results.html', context)

@staff_member_required
@require_POST
def activate_theme(request, theme_id):
    ThemeSettings.objects.all().update(is_active=False)
    theme = get_object_or_404(ThemeSettings, id=theme_id)
    theme.is_active = True
    theme.save()

    referer = request.POST.get('next') or request.META.get('HTTP_REFERER', '')
    host = request.get_host()
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={host}, require_https=False):
        return redirect(referer)
    return redirect('home')
