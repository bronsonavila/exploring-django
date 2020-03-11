from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

import misaka

MEMBERSHIP_CHOICES = (
    (0, "banned"),
    (1, "member"),
    (2, "moderator"),
    (3, "admin")
)


class Community(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through="CommunityMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("communities:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "communities"


class CommunityMember(models.Model):
    community = models.ForeignKey(Community, related_name="memberships")
    user = models.ForeignKey(User, related_name="communities")
    role = models.IntegerField(choices=MEMBERSHIP_CHOICES, default=1)

    def __str__(self):
        return "{} is {} in {}".format(
            self.user.username,
            self.role,
            self.community.name
        )

    class Meta:
        unique_together = ("community", "user")
