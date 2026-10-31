# This file defines the models for the Civil Engineer Site Tracker application.

import datetime

from django.db import models

class ConsructionSite(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=30, decimal_places=10)
    engineer_incharge = models.CharField(max_length=100)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def status(self):
        """
        Derived status used purely for display — not stored in the
        database, so it needs no migration and stays in sync with
        start/end dates automatically.
        """
        today = datetime.date.today()
        if self.end_date and self.end_date < today:
            return "Completed"
        if self.start_date and self.start_date > today:
            return "Planned"
        return "Ongoing"


class SiteImage(models.Model):
    """
    A single photo attached to a construction site. A site can have
    many photos (progress shots, completion photos, etc.) — this is
    what feeds the public homepage carousel and the photo gallery on
    each site's detail page.
    """
    site = models.ForeignKey(ConsructionSite, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='site_photos/%Y/%m/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Photo of {self.site.name}"
