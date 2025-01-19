from collections import defaultdict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import pandas as pd

class RecommendationSystem:
    def __init__(self):
        # Store user interactions (browsing and purchase history)
        self.user_interactions = defaultdict(lambda: {
            'views': defaultdict(lambda: []),
            'purchases': defaultdict(lambda: [])
        })
        
        # Store product features for content-based filtering
        self.product_features = {}
        
        # Store user-product interaction matrix for collaborative filtering
        self.interaction_matrix = defaultdict(lambda: defaultdict(float))
        
        # Cache for recommendations
        self.recommendation_cache = {}
        self.cache_duration = timedelta(hours=1)
    
    def add_product(self, product_id, features):
        """
        Add or update product features for content-based filtering
        
        Args:
            product_id: unique identifier for the product
            features: dict of product features (e.g., category, brand, price_range)
        """
        self.product_features[product_id] = features
    
    def record_interaction(self, user_id, product_id, interaction_type, timestamp=None):
        """
        Record user interaction with a product
        
        Args:
            user_id: unique identifier for the user
            product_id: unique identifier for the product
            interaction_type: 'view' or 'purchase'
            timestamp: datetime of interaction (defaults to current time)
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        if interaction_type == 'view':
            self.user_interactions[user_id]['views'][product_id].append(timestamp)
            self.interaction_matrix[user_id][product_id] += 0.5
        elif interaction_type == 'purchase':
            self.user_interactions[user_id]['purchases'][product_id].append(timestamp)
            self.interaction_matrix[user_id][product_id] += 2.0
        
        # Invalidate cache for this user
        if user_id in self.recommendation_cache:
            del self.recommendation_cache[user_id]
    
    def _get_content_based_recommendations(self, user_id, n_recommendations=5):
        """
        Generate content-based recommendations based on user's recent interactions
        """
        if not self.user_interactions[user_id]['views'] and not self.user_interactions[user_id]['purchases']:
            return []
        
        # Get user's recent interactions
        recent_products = set()
        for product_id in self.user_interactions[user_id]['views'].keys():
            recent_products.add(product_id)
        for product_id in self.user_interactions[user_id]['purchases'].keys():
            recent_products.add(product_id)
        
        # Calculate average feature vector for user's interests
        user_profile = defaultdict(float)
        for product_id in recent_products:
            if product_id in self.product_features:
                for feature, value in self.product_features[product_id].items():
                    user_profile[feature] += float(value)
        
        # Normalize user profile
        total_interactions = len(recent_products)
        if total_interactions > 0:
            for feature in user_profile:
                user_profile[feature] /= total_interactions
        
        # Calculate similarity with all products
        product_scores = []
        for product_id, features in self.product_features.items():
            if product_id not in recent_products:  # Don't recommend already interacted products
                similarity = self._calculate_feature_similarity(user_profile, features)
                product_scores.append((product_id, similarity))
        
        # Sort and return top N recommendations
        product_scores.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in product_scores[:n_recommendations]]
    
    def _get_collaborative_recommendations(self, user_id, n_recommendations=5):
        """
        Generate collaborative filtering recommendations based on user-item interaction matrix
        """
        if user_id not in self.interaction_matrix:
            return []
        
        # Convert interaction matrix to numpy array for efficient computation
        users = list(self.interaction_matrix.keys())
        products = set()
        for user_interactions in self.interaction_matrix.values():
            products.update(user_interactions.keys())
        products = list(products)
        
        # Create user-item matrix
        matrix = np.zeros((len(users), len(products)))
        user_idx = {user: idx for idx, user in enumerate(users)}
        product_idx = {product: idx for idx, product in enumerate(products)}
        
        for user, interactions in self.interaction_matrix.items():
            for product, score in interactions.items():
                matrix[user_idx[user]][product_idx[product]] = score
        
        # Calculate user similarity
        user_similarity = cosine_similarity(matrix)
        
        # Get similar users
        similar_users = []
        user_index = user_idx[user_id]
        for i, similarity in enumerate(user_similarity[user_index]):
            if i != user_index:
                similar_users.append((users[i], similarity))
        
        similar_users.sort(key=lambda x: x[1], reverse=True)
        similar_users = similar_users[:10]  # Top 10 similar users
        
        # Get recommendations from similar users
        recommendations = defaultdict(float)
        for similar_user, similarity in similar_users:
            for product, score in self.interaction_matrix[similar_user].items():
                if product not in self.interaction_matrix[user_id]:
                    recommendations[product] += similarity * score
        
        # Sort and return top N recommendations
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [p[0] for p in sorted_recommendations[:n_recommendations]]
    
    def _calculate_feature_similarity(self, user_profile, product_features):
        """
        Calculate similarity between user profile and product features
        """
        similarity = 0.0
        common_features = set(user_profile.keys()) & set(product_features.keys())
        
        for feature in common_features:
            similarity += abs(float(user_profile[feature]) - float(product_features[feature]))
        
        return 1.0 / (1.0 + similarity)  # Convert distance to similarity
    
    def get_recommendations(self, user_id, n_recommendations=5):
        """
        Get hybrid recommendations combining collaborative and content-based filtering
        
        Args:
            user_id: unique identifier for the user
            n_recommendations: number of recommendations to return
            
        Returns:
            list of recommended product IDs
        """
        # Check cache
        cache_key = (user_id, n_recommendations)
        if cache_key in self.recommendation_cache:
            cache_time, recommendations = self.recommendation_cache[cache_key]
            if datetime.now() - cache_time < self.cache_duration:
                return recommendations
        
        # Get recommendations from both approaches
        content_based = self._get_content_based_recommendations(user_id, n_recommendations)
        collaborative = self._get_collaborative_recommendations(user_id, n_recommendations)
        
        # Combine recommendations (simple averaging approach)
        recommendations = []
        seen_products = set()
        
        # Alternate between both approaches
        for i in range(max(len(content_based), len(collaborative))):
            if i < len(content_based) and content_based[i] not in seen_products:
                recommendations.append(content_based[i])
                seen_products.add(content_based[i])
            
            if i < len(collaborative) and collaborative[i] not in seen_products:
                recommendations.append(collaborative[i])
                seen_products.add(collaborative[i])
            
            if len(recommendations) >= n_recommendations:
                break
        
        # Cache results
        self.recommendation_cache[cache_key] = (datetime.now(), recommendations[:n_recommendations])
        
        return recommendations[:n_recommendations]