from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, permissions
from . import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChangeRoleSerializer, DojoMemberSerializer, DojoMemberActiveUpdateSerializer, DojoMemberRoleUpdateSerializer, DojoMemberListSerializer
from dojos.models import DojoMembership
from rest_framework.permissions import BasePermission
from dojos.choices import DojoRole
from rest_framework.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from dojos.models import Dojo, DojoMembership
from django.views import View
from django.contrib import messages
from django.http import HttpResponseForbidden



class DojoListView(LoginRequiredMixin, ListView):
    model = models.Dojo
    template_name = 'dojo_list.html'
    context_object_name ='dojos'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        tradename = self.request.GET.get('tradename')
        
        if tradename:
            queryset = queryset.filter(tradename__icontains=tradename)
        return queryset
    
class DojoCreateView(LoginRequiredMixin, CreateView):
    model = models.Dojo
    template_name = 'dojo_create.html'
    form_class = forms.DojoForm
    success_url = reverse_lazy('dojo_list')

class DojoDetailView(LoginRequiredMixin, DeleteView):
    model = models.Dojo
    template_name = 'dojo_detail.html'

class DojoUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Dojo
    template_name = 'dojo_update.html'
    form_class = forms.DojoForm
    success_url = reverse_lazy('dojo_list')

class DojoDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Dojo
    template_name = 'dojo_delete.html'
    success_url = reverse_lazy('dojo_list')
 
# 🔹 Lista todos os Dojos
class DojoListAPI(generics.ListAPIView):
    queryset = models.Dojo.objects.all()
    serializer_class = serializers.DojoSerializer
    ermission_classes = [permissions.AllowAny]  # ✅ Permite acesso público 


#view par definição de Role
class ChangeRoleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangeRoleSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        membership = serializer.validated_data["target_membership"]
        membership.role = serializer.validated_data["role"]
        membership.save()

        return Response(
            {"detail": "Role atualizada com sucesso"},
            status=status.HTTP_200_OK
        )
    
class DojoMembersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dojo_id):
        try:
            membership = DojoMembership.objects.get(
                user=request.user,
                dojo_id=dojo_id
            )
        except DojoMembership.DoesNotExist:
            return Response({"detail": "Acesso negado"}, status=403)

        if membership.role not in ["OWNER", "ADMIN"]:
            return Response({"detail": "Permissão negada"}, status=403)

        members = DojoMembership.objects.filter(dojo_id=dojo_id)
        serializer = DojoMemberSerializer(members, many=True)

        return Response(serializer.data)    
    
# dojos/permissions.py
class IsDojoOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        dojo_id = view.kwargs.get("dojo_id")
        if not dojo_id:
            return False

        try:
            membership = DojoMembership.objects.get(
                user=request.user,
                dojo_id=dojo_id,
                active=True
            )
        except DojoMembership.DoesNotExist:
            return False

        return membership.role in [DojoRole.OWNER, DojoRole.ADMIN]
    

class DojoMemberListView(LoginRequiredMixin, ListView):
    model = DojoMembership
    template_name = "members/DojoMemberList.html"
    context_object_name = "members"

    def get_queryset(self):
        dojo_id = self.kwargs["dojo_id"]

        # 🔒 só quem pertence ao dojo pode acessar
        DojoMembership.objects.get(
            user=self.request.user,
            dojo_id=dojo_id
        )

        return DojoMembership.objects.filter(
            dojo_id=dojo_id,
            is_active=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dojo_id = self.kwargs["dojo_id"]

        membership = DojoMembership.objects.get(
            user=self.request.user,
            dojo_id=dojo_id
        )

        # 🔴 AJUSTE ESSENCIAL (não quebra nada)
        dojo = get_object_or_404(Dojo, id=dojo_id)

        context["requester_role"] = membership.role
        context["dojo_id"] = dojo_id
        context["dojo"] = dojo  # ← necessário para {% url ... dojo.id %}

        return context    
 
class DojoMemberRoleUpdateView(generics.UpdateAPIView):
    queryset = DojoMembership.objects.all()
    serializer_class = DojoMemberRoleUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        requester = DojoMembership.objects.get(
            user=self.request.user,
            dojo=serializer.instance.dojo
        )

        # ❌ Admin não pode alterar OWNER
        if serializer.instance.role == DojoRole.OWNER:
            raise PermissionDenied("Não é permitido alterar o OWNER.")

        # ❌ Student nunca altera role
        if requester.role == DojoRole.STUDENT:
            raise PermissionDenied("Você não tem permissão para alterar roles.")
        
        # ❌ admin não promove para OWNER
        if (
            requester.role == DojoRole.ADMIN
            and serializer.validated_data["role"] == DojoRole.OWNER
        ):
            raise PermissionDenied("Admin não pode criar OWNER.")
        
        # ❌ Admin não pode alterar outro ADMIN
        if (
            requester.role == DojoRole.ADMIN
            and serializer.instance.role == DojoRole.ADMIN
        ):
            raise PermissionDenied("Admin não pode alterar outro Admin.")

        serializer.save()
    
class DojoMemberActiveUpdateView(generics.UpdateAPIView):
    queryset = DojoMembership.objects.all()
    serializer_class = DojoMemberActiveUpdateSerializer
    permission_classes = [IsAuthenticated, IsDojoOwnerOrAdmin]

class DojoMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = DojoMembership
    template_name = "DojoMemberConfirmDelete.html"

    def dispatch(self, request, *args, **kwargs):
        membership = self.get_object()

        requester = DojoMembership.objects.get(
            user=request.user,
            dojo=membership.dojo,
            active=True
        )

        # 🔒 Somente OWNER remove membros
        if requester.role != DojoRole.OWNER:
            raise PermissionDenied("Somente o OWNER pode remover membros.")

        # 🔒 OWNER não pode remover a si mesmo
        if membership.user == request.user:
            raise PermissionDenied("Você não pode remover a si mesmo.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            "dojo_member_list",
            args=[self.object.dojo.id]
        )

class DojoMemberUpdateRoleView(LoginRequiredMixin, UpdateView):
    model = DojoMembership
    fields = ["role"]
    template_name = "members/UpdateRole.html"

    def get_success_url(self):
        return reverse("dojo_member_list", args=[self.object.dojo.id])


class DojoMemberDeactivateView(LoginRequiredMixin, UpdateView):
    model = DojoMembership
    fields = []  # não renderiza form
    template_name = "members/DojoMemberConfirmDelete.html"

    def dispatch(self, request, *args, **kwargs):
        membership = self.get_object()

        requester = DojoMembership.objects.get(
            user=request.user,
            dojo=membership.dojo,
            is_active=True
        )

        if requester.role != DojoRole.OWNER:
            raise PermissionDenied("Somente o OWNER pode remover membros.")

        if membership.user == request.user:
            raise PermissionDenied("Você não pode remover a si mesmo.")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        membership = self.get_object()
        membership.is_active = False
        membership.save()

        return redirect("dojo_member_list", membership.dojo.id)

class DojoMemberInactiveListView(LoginRequiredMixin, ListView):
    model = DojoMembership
    template_name = "members/DojoMemberInactiveList.html"
    context_object_name = "members"

    def get_queryset(self):
        dojo = get_object_or_404(Dojo, id=self.kwargs["dojo_id"])
        return (
            DojoMembership.objects
            .filter(dojo=dojo, is_active=False)
            .select_related("user")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dojo"] = get_object_or_404(Dojo, id=self.kwargs["dojo_id"])
        return context

class DojoMemberReactivateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        membership = get_object_or_404(DojoMembership, pk=pk)

        # Apenas OWNER pode reativar
        requester = get_object_or_404(
            DojoMembership,
            dojo=membership.dojo,
            user=request.user,
            is_active=True
        )

        if requester.role != "OWNER":
            return HttpResponseForbidden()

        membership.is_active = True
        membership.save(update_fields=["is_active"])

        messages.success(request, "Membro reativado com sucesso.")

        return redirect(
            "dojo_member_inactive_list",
            dojo_id=membership.dojo.id
        )