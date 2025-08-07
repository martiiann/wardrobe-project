# Wardrobe 🛍️

![Wardrobe Preview](README_IMAGES/laptophome.png)

**Wardrobe** is a fully responsive, full-stack e-commerce platform built with Django, Bootstrap, and Stripe.  
It enables secure online shopping, real-time cart updates, and streamlined order tracking via a custom admin dashboard.

🔗 **Live Site:** https://wardrobe-project-2025-a1e1d4253e40.herokuapp.com/  
💻 **GitHub:** https://github.com/martiiann/wardrobe-project

---

## 📱 Responsive Overview

| Mobile View | Tablet View | Desktop View |
|-------------|-------------|--------------|
| ![Mobile Home](README_IMAGES/mobilehome.png) | ![Tablet Shop](README_IMAGES/tabletshop.png) | ![Laptop Shop](README_IMAGES/laptopshop.png) |
| ![Mobile Checkout](README_IMAGES/mobilecheckout.png) | ![Tablet Cart](README_IMAGES/tabletcart.png) | ![Laptop Home](README_IMAGES/laptophome.png) |

---

## 🧭 Page Overviews
### 🏠 Home Page
![Home](README_IMAGES/laptophome.png)

### 🛍️ Shop Page
![Shop](README_IMAGES/laptopshop.png)

### 🛒 Cart Page
![Cart](README_IMAGES/cartwf.PNG)

### 💳 Checkout Page
![Checkout](README_IMAGES/checkoutwf.PNG)

### 📦 Order History
![Order History](README_IMAGES/ordersviewstest.png)

### 👤 Profile Page
![Profile](README_IMAGES/profilehtmltest.png)

### ⚙️ Admin Dashboard
![Admin View](README_IMAGES/adminviewstest.png)

---

## 🧩 Wireframes
| Page              | Wireframe |
|-------------------|-----------|
| Home              | ![Home WF](README_IMAGES/homewf.PNG) |
| Shop (Product Detail) | ![Product Detail WF](README_IMAGES/productdetailwf.PNG) |
| Cart              | ![Cart WF](README_IMAGES/cartwf.PNG) |
| Checkout          | ![Checkout WF](README_IMAGES/checkoutwf.PNG) |

---

## 🗃️ Database Design (ERD)
![ERD](README_IMAGES/erddiagram.png)

---

## 🔄 User Flow Diagram
![User Flow](README_IMAGES/userflowdiagram.png)

---

## ✨ Features
- 🔐 **Authenticate** — Secure registration, login, and logout
- 🛍️ **Browse** — Shop by gender and category with responsive product cards
- 📄 **Product Details** — View product descriptions, prices, availability, and select sizes
- 🛒 **Live Cart Updates** — Add, update, and remove items with instant cart count updates
- 💳 **Checkout Securely** — Stripe integration for safe, fast transactions
- 📦 **Track Orders** — Order history and tracking number display
- 🖥 **Custom Admin Panel** — Manage products, orders, and tracking in a tailored dashboard
- 📱 **Responsive by Design** — Optimized for mobile, tablet, and desktop

---

## 🛠 Technical Stack
**Frontend:** HTML5, CSS3, JavaScript (ES6), Bootstrap  
**Backend:** Python 3, Django 5  
**Database:** PostgreSQL  
**Payments:** Stripe API  
**Hosting & Storage:** Heroku, Cloudinary  
**Version Control:** Git, GitHub

---

## 🧮 Functionality Overview
| Feature              | Description                                              |
|----------------------|----------------------------------------------------------|
| Add to Cart          | Add from product page or shop view                       |
| Update Quantity      | Adjust quantity in cart using + / −                      |
| Remove from Cart     | Remove individual items                                  |
| Checkout with Stripe | Secure payment via Stripe API                            |
| Order History        | View all past orders with details                        |
| Tracking Number      | Admin adds tracking; user sees it instantly              |
| Live Cart Updates    | Cart count updates instantly                             |
| Admin Panel          | Full product & order management                          |

---

## ✅ Manual Testing

<details>
<summary>📋 Click to view Manual Testing Table</summary>

| Feature                    | Test Description                         | Expected Outcome                              | Status |
|---------------------------|-------------------------------------------|-----------------------------------------------|--------|
| Register User             | Create account                            | Success message, redirect                     | ✅ Pass |
| Invalid Registration      | Submit empty/invalid form                 | Errors displayed, no account created          | ✅ Pass |
| Login                     | Enter valid credentials                   | Logged in, redirect to shop                   | ✅ Pass |
| Invalid Login             | Enter wrong password                      | Error message, no login                       | ✅ Pass |
| Add to Cart               | Add from shop and product detail          | Item appears in cart, toast shown             | ✅ Pass |
| Update Quantity           | Use + / - on cart page                    | Quantity updates, totals recalculated         | ✅ Pass |
| Remove from Cart          | Remove an item                            | Item removed, totals recalculated             | ✅ Pass |
| Empty Cart Checkout       | Attempt checkout with no items            | Prevented with warning                        | ✅ Pass |
| Stripe Success            | Pay with valid test card                  | Payment success, order created, email sent    | ✅ Pass |
| Stripe Failure            | Use failing test card                     | Payment fails, no order created               | ✅ Pass |
| Out-of-Stock Product      | Add unavailable size                      | Disabled button / alert shown                 | ✅ Pass |
| Order History             | View order list                           | Orders render with correct fields             | ✅ Pass |
| Tracking Number Visibility| Admin adds tracking                       | Tracking shown on user order detail           | ✅ Pass |
| Auth-Protected Views      | Visit profile/history while logged out    | Redirect to login                             | ✅ Pass |
| Responsive Layout         | iPhone / iPad / Desktop                   | Layout adapts without overflow                | ✅ Pass |

</details>

---

## 🧪 Validator & Automated Testing

<details>
<summary>💻 Click to view Validation & Automated Testing Screenshots</summary>

### HTML Validation
![HTML Validation](README_IMAGES/homebasehtmltest.png)  
![Profile HTML Test](README_IMAGES/profilehtmltest.png)  
![Shop HTML Test](README_IMAGES/shophtmltest.png)  
![Checkout HTML Test](README_IMAGES/checkouthtmltest.png)

### CSS Validation
![CSS Validation](README_IMAGES/csstest.png)

### JavaScript Validation
![JSHint Validation](README_IMAGES/jshintvalidtest.png)

### Python Validation  
All Python code validated with the Code Institute Python Linter — no errors.

**Admin Tests**  
![Admin Forms Test](README_IMAGES/adminformstest.png)  
![Admin URL Test](README_IMAGES/adminurlstest.png)  
![Admin Views Test](README_IMAGES/adminviewstest.png)  

**Cart Tests**  
![Cart HTML Test](README_IMAGES/carthtmltest.png)  
![Cart Pytest Test](README_IMAGES/cartpytesttest.png)  
![Cart Views Test](README_IMAGES/cartviewstest.png)  

**Orders Tests**  
![Orders Forms Test](README_IMAGES/ordersformstest.png)  
![Orders Model Test](README_IMAGES/ordersmodeltest.png)  
![Orders URL Test](README_IMAGES/ordersurlstest.png)  
![Orders Views Test](README_IMAGES/ordersviewstest.png)  

**Products Tests**  
![Products Admin Test](README_IMAGES/productsadmintest.png)  
![Products Model Test](README_IMAGES/productsmodeltest.png)  
![Products View Test](README_IMAGES/productsviewtest.png)  

**Wardrobe App Tests**  
![Wardrobe URL Test](README_IMAGES/wardrobeurlstest.png)  
![Wardrobe App Forms Test](README_IMAGES/wardrobeappformstest.png)  
![Wardrobe App Models Test](README_IMAGES/wardrobeappmodelstest.png)  
![Wardrobe App URL Test](README_IMAGES/wardrobeappurlstest.png)  
![Wardrobe App Views Test](README_IMAGES/wardrobeappviewstest.png)  

</details>

---

## 🚀 Performance
![Lighthouse Test](README_IMAGES/lighthousetest.png)

- **Performance:** 95%  
- **Accessibility:** 90%  
- **Best Practices:** 94%  
- **SEO:** 92%  

---

## 💡 Future Features
- Wishlist  
- Product reviews & ratings  
- Discount codes  
- Advanced search  

---

## 🛠️ Deployment
The project was deployed on **Heroku** with:
- PostgreSQL for database  
- Cloudinary for media storage  
- Stripe for payments  
- GitHub for version control

---
