from src.dao.MongodbDAO import MongodbDAO
from src.tool.Logger import Logger

import uuid

class CarOfferDAO(MongodbDAO):
    
    def __init__(self):
        super().__init__()
        self.collection = self.mongodb_connection['car_offers']  # Access the specific collection

    def insert_many(self, dto_collection):
        logger = Logger.get_logger(__name__)
        inserted_ids = []
        for dto_object in dto_collection:
            car_offer = {
                'gear_type': dto_object.gear_type,
                'id': str(uuid.uuid4()),
                'internal_ref': dto_object.internal_ref,
                'mileage': dto_object.mileage,
                'motorisation': dto_object.motorisation,
                'origin': dto_object.origin,
                'price': dto_object.price,
                'production_date': dto_object.production_date,
                'scraping_time': dto_object.scraping_time,
                'subtitle': dto_object.subtitle,
                'title': dto_object.title,
                'type': dto_object.type,
                'url': dto_object.url
            }
            result = self.collection.insert_one(car_offer)
            inserted_ids.append(result.inserted_id)
        logger.info(f"Inserted {len(inserted_ids)} car offers with IDs: {inserted_ids}")
        return inserted_ids