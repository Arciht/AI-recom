import reflex as rx
from backend.recommender import get_recommendations
from .user_state import UserState


class RecommendationState(rx.State):
    """Handles loading personalized recommendations"""

    recommendations: list[dict] = []
    is_loading: bool = False

    def load_recommendations(self):
        """Load recommendations based on current user state"""
        self.is_loading = True

        try:
            if not UserState.logged_in:
                # Guest / Not logged in → Show popular products
                print("👤 Guest user → Loading top rated products")
                self.recommendations = get_recommendations(
                    user_id=None,
                    user_type="new",
                    top_n=12
                )
            else:
                # Logged in user
                print(f"👤 Logged in user (ID: {UserState.user_id}, Type: {UserState.user_type})")
                
                self.recommendations = get_recommendations(
                    user_id=UserState.user_id,      # This is the mapped integer ID
                    user_type=UserState.user_type,
                    top_n=12
                )

        except Exception as e:
            print(f"❌ Error loading recommendations: {e}")
            self.recommendations = []

        finally:
            self.is_loading = False

    def refresh_recommendations(self):
        """Force refresh recommendations"""
        self.recommendations = []
        self.load_recommendations()