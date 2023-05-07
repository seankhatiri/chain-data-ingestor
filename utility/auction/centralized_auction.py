from logic.controller.adsrecommender_controller import AdsRecommender
from connector.mongo_helper import MongoHelper
from configuration.configs import Configs

class CentralizedAuction:
    def __init__(self):
        self.ads_recommender = AdsRecommender()
        self.mongo_helper = MongoHelper(Configs.mongo_url_cloud)
        
    def calculate_age_factor(self, days_since_launch):
        return 1 / (1 + days_since_launch)
        
    def calculate_ads_impression(self, clicks, impressions, age_factor):
        return (clicks / impressions) * (1 + age_factor)
        
    def calculate_quality_score(self, ads_similarity, ads_impression):
        return ads_similarity * ads_impression
        
    def calculate_overall_score(self, quality_score, max_bid):
        return quality_score * max_bid
        
    def update_ad_impression(self, ad_id, winning_status):
        #TODO: Implement function to update ad impression after each winning status
        
    def fetch_ads(self, fixed_criteria):
        #TODO: Implement function to retrieve ads based on fixed criteria here, now it retrieves all ads inside adsrecommender_controller
        
    def get_highest_score_ad(self, pk):
        ranked_ads = self.ads_recommender.rank_ads(pk)
        #TODO: Calculate ads_impression, quality_score ,and overall_score,
        # for ad in ranked_ads:
            # age_factor = self.calculate_age_factor(ad['days_since_launch'])
            # ads_impression = self.calculate_ads_impression(ad['clicks'], ad['impressions'], age_factor)
            # quality_score = self.calculate_quality_score(ads_similarity, ads_impression)
            # overall_score = self.calculate_overall_score(quality_score, ad['budget']/ad['timeRemaining'])
        
        return self.mongo_helper.find_one('campaigns', {'description': ranked_ads[0]['description']})
        


