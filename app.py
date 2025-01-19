import streamlit as st
import pandas as pd
from datetime import datetime
from recommendation_system import RecommendationSystem

# Initialize recommendation system
recommender = RecommendationSystem()

# Sample product data
products = {
    'P1': {
        'name': 'Wireless Headphones',
        'category': 'electronics',
        'price': 99.99,
        'brand': 'SoundMax',
        'description': 'Premium wireless headphones with noise cancellation',
        'image_url': 'images/head_phone.jpg',
        'features': {
            'category_score': 0.8,
            'price_range': 0.6,
            'brand_rating': 0.9
        }
    },
    'P2': {
        'name': 'Smart Watch',
        'category': 'electronics',
        'price': 199.99,
        'brand': 'TechFit',
        'description': 'Fitness tracking smartwatch with heart rate monitor',
        'image_url': 'images/watch.jpg',
        'features': {
            'category_score': 0.8,
            'price_range': 0.7,
            'brand_rating': 0.85
        }
    },
    'P3': {
        'name': 'Running Shoes',
        'category': 'sports',
        'price': 79.99,
        'brand': 'SpeedRun',
        'description': 'Lightweight running shoes with cushioned sole',
        'image_url': 'images/shoves.jpeg',
        'features': {
            'category_score': 0.6,
            'price_range': 0.5,
            'brand_rating': 0.75
        }
    },
    'P4': {
        'name': 'Coffee Maker',
        'category': 'appliances',
        'price': 149.99,
        'brand': 'BrewMaster',
        'description': 'Programmable coffee maker with thermal carafe',
        'image_url': 'images/coffe_maker.jpeg',
        'features': {
            'category_score': 0.4,
            'price_range': 0.65,
            'brand_rating': 0.8
        }
    },
    'P5': {
        'name': 'Backpack',
        'category': 'accessories',
        'price': 49.99,
        'brand': 'TravelPro',
        'description': 'Water-resistant laptop backpack with multiple compartments',
        'image_url': 'images/bag.jpeg',
        'features': {
            'category_score': 0.5,
            'price_range': 0.4,
            'brand_rating': 0.7
        }
    },
    'P6': {
        'name': 'speaker',
        'category': 'electronics',
        'price': 49.99,
        'brand': 'BassBoom',
        'description': 'Portable Bluetooth speaker with deep bass and long battery life',
        'image_url': 'images/speaker.webp',
        'features': {
            'category_score': 0.8,
            'price_range': 0.5,
            'brand_rating': 0.8
        }
    },
    'P7': {
        'name': 'Gaming Mouse',
        'category': 'electronics',
        'price': 29.99,
        'brand': 'GamePro',
        'description': 'Ergonomic gaming mouse with customizable buttons and RGB lighting',
        'image_url': 'images/mouse.jpeg',
        'features': {
            'category_score': 0.9,
            'price_range': 0.4,
            'brand_rating': 0.85
        }
    },
    'P8': {
        'name': '4K Smart TV',
        'category': 'electronics',
        'price': 499.99,
        'brand': 'VisionTech',
        'description': '55-inch 4K UHD Smart TV with streaming apps and voice control',
        'image_url': 'images/tv.jpg',
        'features': {
            'category_score': 0.9,
            'price_range': 0.8,
            'brand_rating': 0.9
        }
    },
    'P9': {
        'name': 'Noise-Cancelling Earbuds',
        'category': 'electronics',
        'price': 79.99,
        'brand': 'SoundMax',
        'description': 'Compact wireless earbuds with active noise cancellation',
        'image_url': 'images/earbuds.jpg',
        'features': {
            'category_score': 0.8,
            'price_range': 0.6,
            'brand_rating': 0.9
        }
    },
    'P10': {
        'name': 'Fitness Tracker',
        'category': 'electronics',
        'price': 39.99,
        'brand': 'FitPro',
        'description': 'Lightweight fitness tracker with sleep monitoring and step counter',
        'image_url': 'images/fitness_tracker.jpg',
        'features': {
            'category_score': 0.8,
            'price_range': 0.5,
            'brand_rating': 0.8
        }
    },
    'P11': {
        'name': 'Laptop Backpack',
        'category': 'accessories',
        'price': 59.99,
        'brand': 'TravelMate',
        'description': 'Water-resistant laptop backpack with multiple compartments',
        'image_url': 'images/lap_bag.webp',
        'features': {
            'category_score': 0.7,
            'price_range': 0.6,
            'brand_rating': 0.85
        }
    },
    'P12': {
        'name': 'Wireless Keyboard',
        'category': 'electronics',
        'price': 49.99,
        'brand': 'KeyEase',
        'description': 'Sleek wireless keyboard with long battery life and silent keys',
        'image_url': 'images/keyboard.jpeg',
        'features': {
            'category_score': 0.8,
            'price_range': 0.5,
            'brand_rating': 0.8
        }
    },
    'P13': {
        'name': 'Action Camera',
        'category': 'electronics',
        'price': 299.99,
        'brand': 'AdventureCam',
        'description': 'Waterproof action camera with 4K recording and stabilization',
        'image_url': 'images/camera.jpeg',
        'features': {
            'category_score': 0.9,
            'price_range': 0.7,
            'brand_rating': 0.85
        }
    },
    'P14': {
        'name': 'E-Reader',
        'category': 'electronics',
        'price': 129.99,
        'brand': 'ReadOn',
        'description': 'Lightweight e-reader with adjustable backlight and large storage',
        'image_url': 'images/e_reader.jpeg',
        'features': {
            'category_score': 0.8,
            'price_range': 0.6,
            'brand_rating': 0.85
        }
    },
    'P15': {
        'name': 'Streaming Device',
        'category': 'electronics',
        'price': 39.99,
        'brand': 'StreamHub',
        'description': 'Compact streaming device with access to popular streaming services',
        'image_url': 'images/Streaming Device.jpeg',
        'features': {
            'category_score': 0.9,
            'price_range': 0.5,
            'brand_rating': 0.8
        }
    }

}

# Add products to recommendation system
for product_id, product_data in products.items():
    recommender.add_product(product_id, product_data['features'])

# Streamlit UI
st.title('E-commerce Recommendation System')

# Session state for user ID
if 'user_id' not in st.session_state:
    st.session_state.user_id = 'user1'
if 'viewed_products' not in st.session_state:
    st.session_state.viewed_products = set()
if 'purchased_products' not in st.session_state:
    st.session_state.purchased_products = set()

# Sidebar for user information
st.sidebar.title('User Information')
user_id = st.sidebar.text_input('User ID', st.session_state.user_id)

# Display all products
st.header('Available Products')
cols = st.columns(3)
col_idx = 0

for product_id, product_data in products.items():
    with cols[col_idx]:
        st.image(product_data['image_url'], caption=product_data['name'])
        st.write(f"**{product_data['name']}**")
        st.write(f"Price: ${product_data['price']}")
        st.write(f"Brand: {product_data['brand']}")
        st.write(product_data['description'])
        
        # View and Purchase buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f'View ', key=f'view_{product_id}'):
                recommender.record_interaction(user_id, product_id, 'view')
                st.session_state.viewed_products.add(product_id)
                st.success(f"Viewed {product_data['name']}")
        
        with col2:
            if st.button(f'Buy ', key=f'buy_{product_id}'):
                recommender.record_interaction(user_id, product_id, 'purchase')
                st.session_state.purchased_products.add(product_id)
                st.success(f"Purchased {product_data['name']}")
        
        # Show interaction status
        if product_id in st.session_state.viewed_products:
            st.info('Viewed ✓')
        if product_id in st.session_state.purchased_products:
            st.success('Purchased ✓')
        
        col_idx = (col_idx + 1) % 3

# Get and display recommendations
if st.session_state.viewed_products or st.session_state.purchased_products:
    st.header('Recommended Products')
    recommendations = recommender.get_recommendations(user_id, n_recommendations=3)
    
    if recommendations:
        rec_cols = st.columns(3)
        for idx, rec_id in enumerate(recommendations):
            if rec_id in products:
                product_data = products[rec_id]
                with rec_cols[idx]:
                    st.image(product_data['image_url'], caption=product_data['name'])
                    st.write(f"**{product_data['name']}**")
                    st.write(f"Price: ${product_data['price']}")
                    st.write(f"Brand: {product_data['brand']}")
    else:
        st.info('Interact with more products to get personalized recommendations!')

# Reset button
