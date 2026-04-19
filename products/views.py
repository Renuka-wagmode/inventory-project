import os
import uuid

from bson.errors import InvalidId
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .forms import ProductForm
from .models import Product


def _get_product_or_404(product_id: str) -> Product:
    from bson import ObjectId

    try:
        oid = ObjectId(product_id)
    except InvalidId as exc:
        raise Http404("Invalid product id") from exc
    product = Product.objects(id=oid).first()
    if not product:
        raise Http404("Product not found")
    return product


def _save_uploaded_image(uploaded_file) -> str:
    ext = os.path.splitext(uploaded_file.name)[1].lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        ext = ".jpg"
    name = f"{uuid.uuid4().hex}{ext}"
    subdir = "products"
    dest_dir = settings.MEDIA_ROOT / subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / name
    with open(path, "wb+") as out:
        for chunk in uploaded_file.chunks():
            out.write(chunk)
    return f"{subdir}/{name}"


def _delete_image_file(relative_path: str | None) -> None:
    if not relative_path:
        return
    full = settings.MEDIA_ROOT / relative_path
    try:
        if full.is_file():
            full.unlink()
    except OSError:
        pass


@require_http_methods(["GET"])
def product_list(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects
    if q:
        products = products.filter(name__icontains=q)
    products = products.order_by("-created_at")
    return render(
        request,
        "products/list.html",
        {"products": products, "search_query": q},
    )


@require_http_methods(["GET", "POST"])
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            image_path = ""
            if form.cleaned_data.get("image"):
                image_path = _save_uploaded_image(form.cleaned_data["image"])
            Product(
                name=form.cleaned_data["name"].strip(),
                price=float(form.cleaned_data["price"]),
                quantity=int(form.cleaned_data["quantity"]),
                image=image_path or None,
            ).save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "products/form.html", {"form": form, "title": "Add product", "edit": False})


@require_http_methods(["GET", "POST"])
def product_edit(request, product_id: str):
    product = _get_product_or_404(product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.cleaned_data.get("image")
            if new_image:
                _delete_image_file(product.image)
                product.image = _save_uploaded_image(new_image)
            product.name = form.cleaned_data["name"].strip()
            product.price = float(form.cleaned_data["price"])
            product.quantity = int(form.cleaned_data["quantity"])
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm(
            initial={
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
            }
        )
    return render(
        request,
        "products/form.html",
        {
            "form": form,
            "title": "Edit product",
            "edit": True,
            "product": product,
        },
    )


@require_http_methods(["GET", "POST"])
def product_delete(request, product_id: str):
    product = _get_product_or_404(product_id)
    if request.method == "POST":
        _delete_image_file(product.image)
        product.delete()
        return redirect("product_list")
    return render(request, "products/delete_confirm.html", {"product": product})
