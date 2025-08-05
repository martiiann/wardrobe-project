// ================== CART DETAIL ==================
document.addEventListener('DOMContentLoaded', function () {
    function showEmptyCart() {
        document.querySelector('.cart-container').innerHTML = `
            <div class="container d-flex justify-content-center align-items-center py-5">
              <div class="card bg-dark text-white shadow-lg text-center p-4" style="max-width: 500px; width: 100%;">
                <div class="card-body">
                  <i class="bi bi-cart-x fs-1 text-secondary mb-3"></i>
                  <h4 class="mb-3">Your Cart is Empty</h4>
                  <p class="text-muted mb-4">Looks like you haven’t added anything yet.</p>
                  <a href="/products/" class="btn btn-success w-100">Browse Products</a>
                </div>
              </div>
            </div>`;
    }

    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', function () {
            const url = this.dataset.url;
            const row = this.closest('tr');
            fetch(url, {
                method: 'POST',
                headers: { 
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    row.remove();
                    document.getElementById('cart-items').textContent = data.cart_total_items;
                    const subtotalEl = document.querySelector('#cart-subtotal');
                    if (subtotalEl) subtotalEl.textContent = `€${parseFloat(data.cart_total_price).toFixed(2)}`;
                    const deliverySpan = document.querySelector('#cart-delivery');
                    if (deliverySpan) deliverySpan.textContent = data.cart_delivery_fee === 0 ? 'Free (Orders over €50)' : `€${parseFloat(data.cart_delivery_fee).toFixed(2)}`;
                    const totalEl = document.querySelector('#cart-total');
                    if (totalEl) totalEl.textContent = `€${parseFloat(data.cart_total_with_delivery).toFixed(2)}`;
                    const cartCountEl = document.getElementById('cart-count');
                    if (cartCountEl) cartCountEl.textContent = data.cart_count;
                    if (data.cart_total_items === 0) showEmptyCart();
                }
            });
        });
    });

    document.querySelectorAll('.quantity-form').forEach(form => {
        form.querySelectorAll('button[type="submit"]').forEach(button => {
            button.addEventListener('click', function (e) {
                e.preventDefault();
                const formData = new FormData(form);
                formData.set('quantity', this.value);

                fetch(form.action, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('cart-items').textContent = data.cart_total_items;
                    const subtotalEl = document.querySelector('#cart-subtotal');
                    if (subtotalEl) subtotalEl.textContent = `€${parseFloat(data.cart_total_price).toFixed(2)}`;
                    const deliverySpan = document.querySelector('#cart-delivery');
                    if (deliverySpan) deliverySpan.textContent = data.cart_delivery_fee === 0 ? 'Free (Orders over €50)' : `€${parseFloat(data.cart_delivery_fee).toFixed(2)}`;
                    const totalEl = document.querySelector('#cart-total');
                    if (totalEl) totalEl.textContent = `€${parseFloat(data.cart_total_with_delivery).toFixed(2)}`;
                    const cartCountEl = document.getElementById('cart-count');
                    if (cartCountEl) cartCountEl.textContent = data.cart_count;
                    const itemRow = form.closest('tr');
                    if (data.item_quantity === 0) {
                        if (itemRow) itemRow.remove();
                    } else {
                        const quantitySpan = form.querySelector('.quantity-display');
                        quantitySpan.textContent = data.item_quantity;
                        if (itemRow && data.item_total_price !== undefined) {
                            itemRow.querySelector('.item-total').textContent = `€${parseFloat(data.item_total_price).toFixed(2)}`;
                        }
                    }
                    if (data.cart_total_items === 0) showEmptyCart();
                });
            });
        });
    });
});

// ================== CHECKOUT ==================
const stripe = Stripe("{{ STRIPE_PUBLIC_KEY }}");
document.getElementById("checkout-button").addEventListener("click", function () {
    const data = {
        full_name: document.getElementById("id_full_name").value,
        email: document.getElementById("id_email").value,
        address: document.getElementById("id_address").value,
        city: document.getElementById("id_city").value,
        postal_code: document.getElementById("id_postal_code").value,
        country: document.getElementById("id_country").value,
        payment_method: document.getElementById("id_payment_method").value
    };
    fetch("/orders/create_checkout_session/", {
        method: "POST",
        headers: { "X-CSRFToken": "{{ csrf_token }}", "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            stripe.redirectToCheckout({ sessionId: data.id });
        } else {
            alert("Something went wrong: " + (data.error || "Unknown error"));
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong.");
    });
});

// ================== ORDER DETAIL + HISTORY ==================
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);
    });
});

// ================== CATEGORY PRODUCTS ==================
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            const url = form.dataset.url;
            fetch(url, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('cart-alert-success-msg').textContent = `${data.name} added to cart!`;
                document.getElementById('cart-alert-image').src = data.image || 'https://via.placeholder.com/70';
                document.getElementById('cart-alert-name').textContent = data.name;
                document.getElementById('cart-alert-price').textContent = parseFloat(data.price).toFixed(2);
                document.getElementById('cart-alert-quantity').textContent = data.quantity;
                document.getElementById('cart-alert-size').textContent = data.size || '-';
                document.getElementById('cart-alert-total').textContent = parseFloat(data.cart_total_price).toFixed(2);
                document.getElementById('cart-alert-items').textContent = data.cart_total_items;
                const alertBox = document.getElementById('cart-alert');
                alertBox.classList.remove('d-none');
                setTimeout(() => alertBox.classList.add('show'), 10);
                setTimeout(() => { alertBox.classList.remove('show'); setTimeout(() => alertBox.classList.add('d-none'), 300); }, 6000);
                const cartCountEl = document.getElementById('cart-count');
                if (cartCountEl) cartCountEl.textContent = data.cart_count;
            })
            .catch(error => console.error('Error:', error));
        });
    });

    function equalizeCardHeights() {
        const cards = document.querySelectorAll('#product-grid .card');
        let maxHeight = 0;
        cards.forEach(card => card.style.height = 'auto');
        cards.forEach(card => { maxHeight = Math.max(maxHeight, card.offsetHeight); });
        cards.forEach(card => { card.style.height = maxHeight + 'px'; });
    }
    window.addEventListener('load', equalizeCardHeights);
    window.addEventListener('resize', equalizeCardHeights);
});

// ================== PRODUCT DETAIL ==================
document.addEventListener('DOMContentLoaded', function () {
    const mainImage = document.getElementById('main-product-image');
    const thumbnails = Array.from(document.querySelectorAll('#thumbnail-container img'));
    let currentIndex = 0;
    window.updateMainImage = function (imageUrl, index) {
        mainImage.src = imageUrl;
        currentIndex = index;
    };
    document.getElementById('next-btn').addEventListener('click', function () {
        currentIndex = (currentIndex + 1) % thumbnails.length;
        mainImage.src = thumbnails[currentIndex].src;
    });
    document.getElementById('prev-btn').addEventListener('click', function () {
        currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
        mainImage.src = thumbnails[currentIndex].src;
    });
    const form = document.getElementById('add-to-cart-form');
    const alertBox = document.getElementById('cart-alert');
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        const url = form.dataset.url;
        fetch(url, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('cart-alert-success-msg').textContent = `${data.name} added to cart!`;
            document.getElementById('cart-alert-image').src = data.image || 'https://via.placeholder.com/70';
            document.getElementById('cart-alert-name').textContent = data.name;
            document.getElementById('cart-alert-price').textContent = parseFloat(data.price).toFixed(2);
            document.getElementById('cart-alert-quantity').textContent = data.quantity;
            document.getElementById('cart-alert-size').textContent = data.size || '-';
            document.getElementById('cart-alert-total').textContent = parseFloat(data.cart_total_price).toFixed(2);
            document.getElementById('cart-alert-items').textContent = data.cart_total_items;
            alertBox.classList.remove('d-none');
            setTimeout(() => alertBox.classList.add('show'), 10);
            const cartCountEl = document.getElementById('cart-count');
            if (cartCountEl) cartCountEl.textContent = data.cart_count;
            setTimeout(() => { alertBox.classList.remove('show'); setTimeout(() => alertBox.classList.add('d-none'), 300); }, 6000);
        })
        .catch(error => console.error('Error:', error));
    });
});