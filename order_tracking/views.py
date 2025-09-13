from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse
from .models import Order
import asyncio
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from .utils import connect_sse, push_event


def menu(request):
    return render(request, "menu.html")


@login_required
def order_view(request, id=None):
    if request.method == "POST":
        user = request.user
        order = Order.objects.create(customer=user, status="Confirmed")
        connect_sse(order.id)
        async_to_sync(push_event)(order.id, "Confirmed")
        return render(request, "SSE.html", {"order_id": order.id})
    if request.method == "GET":
        if id:
            order = get_object_or_404(Order, id=id)
            return render(request, "SSE.html", {"order_id": order.id})


# track the order
# the pattern is SSE over each client
# listen change in status using signal -> put new change in queue
# each order has queue
# {order_id: <queue of status>}
# then check our queue in sse stream


async def sse_stream(request, order_id):
    q = connect_sse(order_id)

    async def event_stream():
        start_time = asyncio.get_event_loop().time()  # monotonic clock point
        while True:
            try:
                if asyncio.get_event_loop().time() - start_time > 30 * 60:
                    break
                status = await asyncio.wait_for(q.get(), timeout=3)
                yield f"data: {status}\n\n"
                if status.lower() == "delivered":
                    break
            except asyncio.TimeoutError:
                yield "alive\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
