from typing import Dict, List, Optional, Union
from decimal import Decimal
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from rest_framework import viewsets
from .serializers import OrderSerializer
from .models import Order


def order_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        # Получаем данные из формы
        table_number: str = request.POST.get('table_number', '')
        # Ожидаем список блюд в формате JSON
        items: List[str] = request.POST.getlist('items[]')
        item_prices: List[str] = request.POST.getlist(
            'prices[]')  # Цены на блюда

        # Преобразуем данные в формат JSON
        formatted_items: List[Dict[str, Union[str, float]]] = [
            {'name': name, 'price': float(price)}
            for name, price in zip(items, item_prices)
        ]

        # Создаем заказ
        order: Order = Order.objects.create(
            table_number=int(table_number),
            items=formatted_items
        )
        order.calculate_total()  # Рассчитываем общую стоимость заказа

        return redirect('order_list')

    return render(request, 'orders/order_create.html')


def order_delete(request: HttpRequest, order_id: int) -> HttpResponse:
    order: Order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')


def order_update(request: HttpRequest, order_id: int) -> HttpResponse:
    order: Order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Обновляем данные заказа
        table_number: str = request.POST.get('table_number', '')
        items: List[str] = request.POST.getlist('items[]')
        item_prices: List[str] = request.POST.getlist('prices[]')

        # Преобразуем данные в формат JSON
        formatted_items: List[Dict[str, Union[str, float]]] = [
            {'name': name, 'price': float(price)}
            for name, price in zip(items, item_prices)
        ]
        order.table_number = int(table_number)
        order.items = formatted_items
        order.calculate_total()  # Пересчитываем общую стоимость
        order.status = request.POST.get('status', 'pending')
        order.save()

        return redirect('order_list')

    return render(request, 'orders/order_update.html', {'order': order})


def calculate_revenue(request: HttpRequest) -> HttpResponse:
    # Суммируем total_price для всех оплаченных заказов
    total_revenue: Optional[Decimal] = Order.objects.filter(status='paid').aggregate(
        total=Sum('total_price'))['total'] or Decimal('0')

    return render(request, 'orders/revenue.html', {'total_revenue': total_revenue})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # Все заказы
    serializer_class = OrderSerializer  # Используем созданный сериализатор


def order_list(request: HttpRequest) -> HttpResponse:
    search_query = request.GET.get('search', '')  # Получаем поисковый запрос
    orders = Order.objects.all()  # Все заказы

    # Если есть поисковый запрос
    if search_query:
        try:
            # Пытаемся преобразовать в число (поиск по столу)
            table_number = int(search_query)
            orders = orders.filter(table_number=table_number)
        except ValueError:
            # Если не число → поиск по статусу (например, "готово")
            orders = orders.filter(status__icontains=search_query.lower())

    return render(request, 'orders/order_list.html', {'orders': orders})
