import reflex as rx
from ..backend.recommender import get_recommendations
from .user_state import UserState


class RecommendationState(rx.State):
    recommendations: list[dict] = []
    content_based_recs: list[dict] = []
    collaborative_recs: list[dict] = []
    is_loading: bool = False

    async def load_recommendations(self):
        """Load recommendations based on current user state"""
        self.is_loading = True

        try:
            # Get user state for runtime values
            user_state = await self.get_state(UserState)
            uid = user_state.user_id if user_state.logged_in else None
            utype = user_state.user_type
            
            # Note: the import from backend might need to be adjusted based on sys.path
            # In ai_ecom.py, the root_dir is added to sys.path
            raw_recs = get_recommendations(
                user_id=uid,
                user_type=utype,
                top_n=8
            )
            
            # Map columns and clean up
            mapped_recs = []
            for r in raw_recs:
                # The raw_recs might already have mapped columns or original ones
                # We normalize them here for the frontend
                item = {
                    "product_id": str(r.get("product_id", r.get("ProdID", ""))),
                    "product_name": str(r.get("product_name", r.get("Name", ""))),
                    "image_url": str(r.get("image_url", r.get("ImageURL", ""))).split(" | ")[0] if r.get("image_url", r.get("ImageURL")) else "https://via.placeholder.com/400",
                    "rating": float(r.get("rating", r.get("Rating", 0.0))),
                    "rating_count": int(r.get("rating_count", r.get("Review Count", 0))),
                    "category": str(r.get("category", r.get("Category", ""))),
                    "description": str(r.get("description", r.get("Description", ""))),
                    "tags": str(r.get("tags", r.get("Tags", ""))),
                    "price": float(r.get("price", round((hash(str(r.get("product_id", r.get("ProdID", "")))) % 10000) / 100 + 499, 2)))
                }
                mapped_recs.append(item)
                
            self.recommendations = mapped_recs[:20]
            
            # For Recommendation Page specific tabs
            # Note: In a real app we might call specific methods, but here we reuse get_recommendations
            self.content_based_recs = self.recommendations[:8]
            self.collaborative_recs = self.recommendations[8:16]

        except Exception as e:
            print(f"❌ Error loading recommendations: {e}")
            self.recommendations = []
        finally:
            self.is_loading = False

    async def trigger_recommendations(self):
        await self.load_recommendations()
        return rx.redirect("/recommendations")

    async def refresh_recommendations(self):
        """Force refresh recommendations"""
        self.recommendations = []
        await self.load_recommendations()
        return rx.toast("Recommendations refreshed!")
