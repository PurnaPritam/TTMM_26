from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

User = get_user_model()

REQUIRED_BIDDING_AMOUNT = 35

def upload_image(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s-%s.%s" % (instance.__class__.__name__, instance.id, ext)
    return "/".join([filename])

def upload_ppt(instance, filename):
    ext = filename.split(".")[-1]
    filename = "acco-%s.%s" % (instance.id, ext)
    return "/".join([filename])

class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="ttmm_investor")
    name = models.CharField(max_length=300)
    image = models.FileField(upload_to=upload_image, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def total_funding(self):
        total = self.fundings.aggregate(Sum("amount"))["amount__sum"]
        return total if total else 0

day_choices = ((1, "Day 1"), (2, "Day 2"))

class Startup(models.Model):
    name = models.CharField(max_length=300)
    day = models.IntegerField(choices=day_choices)
    image = models.FileField(upload_to=upload_image, blank=True)
    ppt = models.FileField(upload_to=upload_ppt, blank=True)
    bid_overview = models.TextField(blank=True, max_length=512)

    @property
    def total_bid(self):
        total = Funding.objects.filter(startup=self).aggregate(Sum("funding"))["funding__sum"]
        return total if total else 0

    @property
    def is_funded(self):
        return self.total_bid >= REQUIRED_BIDDING_AMOUNT

    def __str__(self):
        return self.name

choices = (
    (0, "none"),
    (1, "bidding"),
    (2, "after_bidding"),
)

class PortalControlManager(models.Manager):
    _ttmm = None
    
    def get_ttmm(self):
        if self._ttmm is None:
            self._ttmm = self.get(control_name="ttmm")
        return self._ttmm

class PortalControl(models.Model):
    control_name = models.CharField(null=True, blank=True, max_length=30)
    day = models.IntegerField(choices=day_choices)
    current_scene = models.IntegerField(choices=choices)
    current_startup = models.ForeignKey(Startup, on_delete=models.RESTRICT, null=True, blank=True)
    allow_bids = models.BooleanField(default=False)
    force_reload = models.BooleanField(default=False)

    objects = PortalControlManager()

    def __str__(self):
        return self.control_name or "Portal Control"

@receiver(pre_save, sender=PortalControl, dispatch_uid="portal_control_pre_save")
def pre_save_portal_control(sender, instance, **kwargs):
    if instance.control_name == "ttmm":
        if instance.current_scene != 1:
            instance.allow_bids = True

@receiver(post_save, sender=PortalControl, dispatch_uid="portal_control_changed")
def portal_control_changed(sender, instance, created, **kwargs):
    if not created:
        if instance.control_name == "ttmm":
            sender.objects._ttmm = instance

class FundingManager(models.Manager):
    _funded_investors = None

    def get_funded_investors(self):
        if self._funded_investors is None:
            portal_control = PortalControl.objects.get_ttmm()
            if portal_control.current_startup is not None:
                fundings = self.filter(startup=portal_control.current_startup)
                self._funded_investors = fundings.values_list("investor", flat=True)
        return self._funded_investors

class Funding(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    funding = models.IntegerField(blank=True, default=0)
    final_submit = models.BooleanField(blank=True, default=False)

    objects = FundingManager()

    def __str__(self):
        return f"{self.investor.name} -> {self.startup.name}"