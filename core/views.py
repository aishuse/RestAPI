from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from core.models import Currency, Category, Transaction
from core.serializers import CurrencySerializer, CategorySerializer, ReadTransactionSerializer, \
    WriteTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryModelViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TransactionModelViewset(viewsets.ModelViewSet):
    # queryset = Transaction.objects.select_related("currency", "category", 'user')
    permission_classes = (IsAuthenticated,)
    # serializer_class = TransactionSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        else:
            return WriteTransactionSerializer

    def get_queryset(self):
        return Transaction.objects.select_related("currency", "category", 'user').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)