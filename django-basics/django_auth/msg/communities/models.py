from django.conf import settings
from django.urls import reverse
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
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="CommunityMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("communities:single", kwargs={"slug": self.slug})

    # NOTE: The instructor stated that these three properties could (and
    # probably should) be done as methods on a custom model manager.
    @property
    def admins(self):
        # Return list of IDs of the users who are admins.
        return self.memberships.filter(role=3).values_list('user', flat=True)

    @property
    def moderators(self):
        return self.memberships.filter(role=2).values_list('user', flat=True)

    @property
    def good_members(self):
        return self.memberships.exclude(role=0)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "communities"


class CommunityMember(models.Model):
    community = models.ForeignKey(
        Community,
        related_name="memberships",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="communities",
        on_delete=models.CASCADE,
    )
    role = models.IntegerField(choices=MEMBERSHIP_CHOICES, default=1)

    def __str__(self):
        return "{} is {} in {}".format(
            self.user.username,
            self.role,
            self.community.name
        )

    class Meta:
        # When you add a new permission, you are adding it to the
        # `permissions` table, which requires a new migration.
        permissions = (
            # The second item is displayed in the admin menu.
            ('ban member', 'Can ban members'),
        )
        unique_together = ("community", "user")
