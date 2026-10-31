from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import ConsructionSite, SiteImage
from .forms import ConsructionSiteForm, SiteImageForm


# Only staff accounts can reach add/edit/delete and the internal
# dashboard — everyone else is bounced to the login page. Public
# visitors only ever see site_list -> public_home / site_detail.
staff_required = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='login')


def _site_stats(sites):
    total_sites = sites.count()
    ongoing = sum(1 for s in sites if s.status == 'Ongoing')
    completed = sum(1 for s in sites if s.status == 'Completed')
    planned = sum(1 for s in sites if s.status == 'Planned')
    total_budget = sites.aggregate(total=Sum('budget'))['total'] or 0
    return {
        'total_sites': total_sites,
        'ongoing': ongoing,
        'completed': completed,
        'planned': planned,
        'total_budget': total_budget,
    }


def public_home(request):
    """
    Public landing page: shows off ongoing/completed work with a
    photo carousel and animated stat counters. No CRUD controls,
    no budget figures — just what a visitor should see.
    """
    sites = ConsructionSite.objects.all().order_by('-start_date')
    carousel_images = SiteImage.objects.select_related('site').order_by('-uploaded_at')[:8]

    context = {'sites': sites, 'carousel_images': carousel_images}
    context.update(_site_stats(sites))
    return render(request, 'sites/public_home.html', context)


@staff_required
def site_list(request):
    """
    Staff dashboard view: lists all construction sites with full
    CRUD controls and a handful of summary stats.
    """
    sites = ConsructionSite.objects.all().order_by('-start_date')
    context = {'sites': sites}
    context.update(_site_stats(sites))
    return render(request, 'sites/site_list.html', context)


def site_detail(request, site_id):
    """
    View to display details of a specific construction site.
    Public visitors can view this page too; edit/delete controls
    and the budget figure are only shown to staff (enforced in the
    template, and the underlying edit/delete views are staff-only).
    """
    try:
        site = ConsructionSite.objects.get(id=site_id)
    except ConsructionSite.DoesNotExist:
        return render(request, 'sites/site_not_found.html', {'site_id': site_id})

    return render(request, 'sites/detail_site.html', {'site': site})


@staff_required
def add_site(request):
    """
    View to add a new construction site.
    """
    if request.method == 'POST':
        form = ConsructionSiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_sites')
    else:
        form = ConsructionSiteForm()

    return render(request, 'sites/site_add.html', {'form': form})


@staff_required
def edit_site(request, site_id):
    """
    View to edit an existing construction site.
    """
    try:
        site = ConsructionSite.objects.get(id=site_id)
    except ConsructionSite.DoesNotExist:
        return render(request, 'sites/site_not_found.html', {'site_id': site_id})

    if request.method == 'POST':
        form = ConsructionSiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            return redirect('list_sites')
    else:
        form = ConsructionSiteForm(instance=site)
    return render(request, 'sites/site_edit.html', {'form': form, 'site': site})


@staff_required
def delete_site(request, site_id):
    """
    Simple delete view with confirmation.
    """
    site = get_object_or_404(ConsructionSite, id=site_id)

    if request.method == 'POST':
        site.delete()
        return redirect('list_sites')

    return render(request, 'sites/site_confirm_delete.html', {'site': site})


@staff_required
def add_site_image(request, site_id):
    """
    Upload a photo for a site — feeds the public homepage carousel
    and the photo gallery on the site's detail page.
    """
    site = get_object_or_404(ConsructionSite, id=site_id)

    if request.method == 'POST':
        form = SiteImageForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.site = site
            photo.save()
            return redirect('site_detail', site_id=site.id)
    else:
        form = SiteImageForm()

    return render(request, 'sites/site_image_add.html', {'form': form, 'site': site})


@staff_required
def delete_site_image(request, image_id):
    """
    Remove a photo from a site's gallery.
    """
    image = get_object_or_404(SiteImage, id=image_id)
    site_id = image.site_id

    if request.method == 'POST':
        image.delete()

    return redirect('site_detail', site_id=site_id)
