    # Wardrobe 🛍️

    ![Wardrobe Preview](README_IMAGES/wardrobe-overview.png)

    Wardrobe is a full-stack e-commerce application built with Django, Bootstrap, and Stripe.  
    It allows users to browse men's and women's clothing, filter by category and size, add products to a shopping cart, checkout securely, and track their orders with a custom admin dashboard.

    🔗 [Live Site (Coming Soon)](https://your-heroku-app.herokuapp.com)  
    💻 [GitHub Repository](https://github.com/yourusername/wardrobe-project)

    ---

    ## 📚 Table of Contents
    - [Responsive Overview](#-responsive-overview)
    - [Page Overviews](#-page-overviews)
    - [Wireframes](#-wireframes)
    - [Database Design (ERD)](#️-database-design-erd)
    - [Features](#-features)
    - [Functionality Overview](#-functionality-overview)
    - [Manual Testing Table](#-manual-testing-table)
    - [First-Time Visitor Goals](#-first-time-visitor-goals)
    - [Returning Visitor Goals](#-returning-visitor-goals)
    - [Design](#-design)
    - [Validator Testing](#-validator-testing)
    - [Performance](#-performance)
    - [Devices Tested](#-devices-tested)
    - [Browser Compatibility](#-browser-compatibility)
    - [Future Features](#-future-features)
    - [Deployment](#-deployment)
    - [Debugging & Problem Solving](#-debugging--problem-solving)
    - [Lessons Learned](#-lessons-learned)
    - [Acknowledgments](#-acknowledgments)

    ---

    ## 📱 Responsive Overview
    Mobile, tablet, and desktop views tested manually.

    | Mobile View | Tablet View | Desktop View |
    |-------------|-------------|--------------|
    | ![Mobile](README_IMAGES/mobile.png) | ![Tablet](README_IMAGES/tablet.png) | ![Desktop](README_IMAGES/desktop.png) |

    ---

    ## 🧭 Page Overviews
    ### 🏠 Home Page
    ![Home](README_IMAGES/homepage.png)

    ### 🛍️ Shop Page
    ![Shop](README_IMAGES/shopoverview.png)

    ### 🛒 Cart Page
    ![Cart](README_IMAGES/cartoverview.png)

    ### 💳 Checkout Page
    ![Checkout](README_IMAGES/checkoutoverview.png)

    ### 📦 Order History
    ![Orders](README_IMAGES/orderhistory.png)

    ### 👤 Profile Page
    ![Profile](README_IMAGES/profile.png)

    ### ⚙️ Admin Dashboard
    ![Admin](README_IMAGES/adminpanel.png)

    ---

    ## 🧩 Wireframes
    Initial wireframes created during planning (desktop, tablet, mobile).  
    Some adjustments made during development to improve UX.

    | Page         | Wireframe |
    |--------------|-----------|
    | Home         | ![Home WF](README_IMAGES/wf_home.png) |
    | Shop         | ![Shop WF](README_IMAGES/wf_shop.png) |
    | Cart         | ![Cart WF](README_IMAGES/wf_cart.png) |
    | Checkout     | ![Checkout WF](README_IMAGES/wf_checkout.png) |
    | Profile      | ![Profile WF](README_IMAGES/wf_profile.png) |
    | Admin Panel  | ![Admin WF](README_IMAGES/wf_admin.png) |

    ---

    ## 🗃️ Database Design (ERD)
    Entity Relationship Diagram showing all models and relationships:
    - User ↔ Profile (1:1)
    - Category ↔ Product (1:M)
    - Product ↔ Sizes (M:M)
    - Product ↔ ProductImages (1:M)
    - Order ↔ OrderItems (1:M)
    - User ↔ Order (1:M)

    ![ERD](README_IMAGES/erd.png)

    ---

    ## ✨ Features
    - **User Authentication**: Register, login, logout  
    - **Shop by Category & Gender**: Men’s and women’s sections with filters  
    - **Product Details**: Multiple images, size selection, availability status  
    - **Cart**: Add, update, remove items (with live updates)  
    - **Checkout**: Stripe integration for secure payments  
    - **Order Tracking**: Order history with tracking numbers  
    - **Custom Admin Dashboard**: Manage products, orders, and tracking numbers  
    - **Responsive Design**: Mobile-first with Bootstrap  

    ---

    ## 🧮 Functionality Overview
    | Feature                        | Description                                                                |
    |--------------------------------|----------------------------------------------------------------------------|
    | Add to Cart                    | Add from product page or shop view                                         |
    | Update Quantity                | Adjust quantity in cart using + / -                                        |
    | Remove from Cart               | Remove individual items                                                    |
    | Checkout with Stripe           | Secure payment via Stripe API                                              |
    | Order History                  | View all past orders with details                                          |
    | Tracking Number                | Admin can add tracking; user sees it                                       |
    | Live Cart Updates              | Cart count updates instantly                                               |
    | Admin Panel                    | Full product & order management                                            |

    ---

    ## ✅ Manual Testing Table
    | Feature                       | Test Description                          | Expected Outcome                  | Status |
    |-------------------------------|-------------------------------------------|-----------------------------------|--------|
    | Register User                 | Create account                           | Success message, redirect               | ✅ Pass |
    | Login                         | Enter valid credentials                  | Logged in, redirect to shop                | ✅ Pass |
    | Add to Cart                   | Add product                              | Item in cart, toast alert                     | ✅ Pass |
    | Remove from Cart              | Remove product                           | Item removed, alert shown                     | ✅ Pass |
    | Checkout                      | Pay with Stripe test card                | Payment success, order created          | ✅ Pass |
    | Order History                 | Check history                            | Orders appear correctly                       | ✅ Pass |
    | Tracking Number               | Admin updates tracking                   | User sees tracking in order detail.       | ✅ Pass |
    | Responsive Layout             | Test on iPhone / iPad / Desktop          | Layout works well on all sizes               | ✅ Pass |

    ---

    ## 🎯 First-Time Visitor Goals
    - Browse categories and products  
    - View detailed product pages with sizes and prices  
    - Easily add products to cart and checkout  

    ---

    ## 🔁 Returning Visitor Goals
    - Log in to view orders  
    - Manage saved shipping details  
    - Track order status  

    ---

    ## 🎨 Design
    - **Font**: Bootstrap default (modern, clean)  
    - **Color Theme**: Dark theme with white text for e-commerce look  
    - **Buttons & Cards**: Consistent Bootstrap styling  
    - **Responsiveness**: Verified across devices  

    ---

    ## 🧪 Validator Testing
    ### ✅ HTML Validation
    ![HTML Test](README_IMAGES/htmltest.png)  

    ### ✅ CSS Validation
    ![CSS Test](README_IMAGES/csstest.png)  

    ### ✅ JavaScript Validation
    ![JS Test](README_IMAGES/jstest.png)  

    ### ✅ Python Validation
    ![Python Test](README_IMAGES/pythontest.png)  

    ---

    ## 🚀 Performance
    Tested with Lighthouse:  
    ![Performance](README_IMAGES/lighthouse.png)  

    - **Performance**: 95%  
    - **Accessibility**: 90%  
    - **Best Practices**: 94%  
    - **SEO**: 92%  

    ---

    ## 📱 Devices Tested
    - Mobile: iPhone 15, Samsung S23 Ultra  
    - Tablet: iPad Air  
    - Desktop: MacBook Pro, Windows 1080p  
    ✅ Works as expected on all  

    ---

    ## 🌐 Browser Compatibility
    - Chrome  
    - Firefox  
    - Safari  
    - Edge  
    ✅ All major browsers work perfectly  

    ---

    ## 💡 Future Features
    - Wishlist  
    - Product reviews & ratings  
    - Discount codes  
    - Advanced search  

    ---

    ## 🛠️ Deployment
    Will be deployed on **Heroku** with:
    - PostgreSQL for database  
    - Cloudinary for media storage  
    - Stripe for payments  

    ---

    ## 🐞 Debugging & Problem Solving
    - **Cart count not updating** → Fixed via AJAX refresh  
    - **Image thumbnails not switching** → Added JavaScript event listeners  
    - **Stripe test mode errors** → Corrected API keys & webhook secret  

    ---

    ## 🧠 Lessons Learned
    - Django model relationships  
    - Stripe integration  
    - Custom admin panels  
    - Improving UX in e-commerce  

    ---

    ## 🙏 Acknowledgments
    - Code Institute  
    - Bootstrap & Django docs  
    - Stripe API docs