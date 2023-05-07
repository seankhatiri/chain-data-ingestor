from connector.mongo_helper import MongoHelper
from recommender import Recommender

class CentralizedAuction:
    def __init__(self):
        self.recommender = Recommender()
        
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
        #TODO: Implement function to retrieve ads based on fixed criteria, now it retrieves all ads

        
    def get_highest_score_ad(self, ads_list):
        max_score = 0
        highest_score_ad = None
        
        for ad in ads_list:
            # Calculate ads_similarity using the recommender
            ads_similarity = self.recommender.get_ads_similarity(ad, fixed_criteria)
            
            # Calculate ads_impression
            age_factor = self.calculate_age_factor(ad['days_since_launch'])
            ads_impression = self.calculate_ads_impression(ad['clicks'], ad['impressions'], age_factor)
            
            # Calculate quality_score and overall_score
            quality_score = self.calculate_quality_score(ads_similarity, ads_impression)
            overall_score = self.calculate_overall_score(quality_score, ad['max_bid'])
            
            # Update highest_score_ad if overall_score is higher than max_score
            if overall_score > max_score:
                max_score = overall_score
                highest_score_ad = ad
                
        return highest_score_ad

# Initialize the CentralizedAuction class
auction = CentralizedAuction()

# Add code to interact with the auction system, e.g., create accounts, campaigns, fetch ads, etc.
