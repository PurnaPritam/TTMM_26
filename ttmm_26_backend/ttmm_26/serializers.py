from rest_framework import serializers
from .models import Investor, Startup, PortalControl, Funding

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = "__all__"

class InvestorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ("name", "image")

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = "__all__"

class PortalControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalControl
        fields = "__all__"

class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = ("investor", "startup", "funding", "final_submit")

class StartupFetchSerializer(serializers.ModelSerializer):
    total_bid = serializers.SerializerMethodField(read_only=True)
    get_total_bid = lambda self, obj: obj.total_bid

    class Meta:
        model = Startup
        fields = "__all__"

class StartupMinimalSerializer(serializers.ModelSerializer):
    total_bid = serializers.SerializerMethodField(read_only=True)
    get_total_bid = lambda self, obj: obj.total_bid

    class Meta:
        model = Startup
        # REMOVED 'status'
        fields = ("id", "name", "total_bid", "day") 

class InvestorFundingsSerializer(serializers.ModelSerializer):
    startup = StartupMinimalSerializer()

    class Meta:
        model = Funding
        fields = ("startup", "funding")