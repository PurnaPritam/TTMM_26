from django.shortcuts import render, get_object_or_404
from .models import Investor, Startup, PortalControl, Funding
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers
from django.core.exceptions import ObjectDoesNotExist

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bidding(request):
    data = request.data
    try:
        admin = Investor.objects.get(user__id=request.user.id)
        startup = Startup.objects.get(pk=data["startup"])
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, safe=False)

    try:
        portal_control = PortalControl.objects.get(control_name="ttmm")
    except ObjectDoesNotExist:
        return JsonResponse({"success": False, "message": "Portal Config Missing"}, status=500)

    # OLD LOGIC: Check global Portal Control settings
    if (portal_control.current_startup != startup
        or not portal_control.allow_bids
        or portal_control.current_scene != 1):
        return JsonResponse({"success": False, "message": "Bid denied"}, status=400, safe=False)

    fund_amount = data["bid"]
    previous_funding = Funding.objects.filter(investor=admin, startup=startup)
    
    if not previous_funding.exists():
        funding = Funding(investor=admin, startup=startup, funding=fund_amount)
        funding.save()
    else:
        prev_fund = previous_funding.first()
        prev_fund.funding = fund_amount
        prev_fund.save()

    startup.refresh_from_db()
    return JsonResponse({"success": True, "total_bid": startup.total_bid}, safe=False)

@api_view(["GET"])
def portal_control(request):
    try:
        portal = PortalControl.objects.get(control_name="ttmm")
        portal_ser = serializers.PortalControlSerializer(portal, many=False)
        resp_data = portal_ser.data
        
        # Manually attach total_bid and startup_name
        if portal.current_startup:
            resp_data["total_bid"] = portal.current_startup.total_bid
            resp_data["startup_name"] = portal.current_startup.name
        else:
            resp_data["total_bid"] = 0
            resp_data["startup_name"] = None

        return JsonResponse(resp_data, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Portal Control not initialized"}, status=404)

@api_view(["GET"])
def investor_fetch(request):
    investor = Investor.objects.all()
    investor_ser = serializers.InvestorSerializer(investor, many=True)
    return Response(investor_ser.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_investor_profile(request):
    try:
        investor = Investor.objects.get(user=request.user)
        investor_ser = serializers.InvestorProfileSerializer(investor)
        return Response(investor_ser.data)
    except ObjectDoesNotExist:
        return Response({"success": False, "message": "Investor profile not found"})

@api_view(["GET"])
def startup_fetch(request):
    startup = Startup.objects.all()
    start_ser = serializers.StartupFetchSerializer(startup, many=True)
    return Response(start_ser.data)

@api_view(["GET"])
def get_funded_investors(request):
    try:
        portal_control = PortalControl.objects.get(control_name="ttmm")
        if portal_control.current_startup is None:
            return Response({"success": False})
        fundings = Funding.objects.filter(startup=portal_control.current_startup)
        funded_investors = fundings.values_list("investor", flat=True)
        return JsonResponse(list(funded_investors), safe=False)
    except ObjectDoesNotExist:
        return Response({"success": False})

@api_view(["GET"])
def funding_fetch(request):
    try:
        control = PortalControl.objects.get(control_name="ttmm")
        if not control.current_startup:
             return Response([])
        startup = Startup.objects.filter(pk=control.current_startup.pk)
        start_ser = serializers.StartupFetchSerializer(startup, many=True)
        return Response(start_ser.data)
    except:
        return Response([])

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_own_funding(request):
    try:
        control = PortalControl.objects.get(control_name="ttmm")
        if not control.current_startup:
             return Response({"success": True, "has_bid": False})
        
        funding = Funding.objects.get(
            startup=control.current_startup, investor__user__id=request.user.id
        )
        return Response({"success": True, "has_bid": True, "bid": funding.funding})
    except ObjectDoesNotExist:
        return Response({"success": True, "has_bid": False})
    except Exception:
        return Response({"success": False})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_investor_funded_startups(request):
    try:
        funding = Funding.objects.filter(investor__user__id=request.user.id)
        funding_ser = serializers.InvestorFundingsSerializer(
            funding, many=True, context={"request": request}
        )
        return Response(funding_ser.data)
    except Exception as err:
        print(err)
        return Response([])

@api_view(["GET"])
def get_startup_investors(request):
    try:
        portal_control = PortalControl.objects.get(control_name="ttmm")
        if portal_control.current_startup is None:
            return Response({"success": False})
        fundings = Funding.objects.filter(startup=portal_control.current_startup)
        funded_investors = fundings.values_list("investor", flat=True)
        return Response({
            "investors": funded_investors,
            "total_bid": portal_control.current_startup.total_bid,
            "startup_name": portal_control.current_startup.name,
        })
    except Exception as err:
        print(err)
        return Response({"success": False})