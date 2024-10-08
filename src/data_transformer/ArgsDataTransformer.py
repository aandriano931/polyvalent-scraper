from src.dto.CarOfferDTO import CarOfferDTO

class ArgsDataTransformer:

    def transform_collection(self, raw_data_collection):
        transformed_data_list = []
        for raw_data in raw_data_collection:
            transformed_data = CarOfferDTO(
                raw_data.get('gear_type', 'N/A'),
                raw_data.get('internal_ref', 'N/A'),
                raw_data.get('mileage', 'N/A'),
                raw_data.get('motorisation', 'N/A'),
                raw_data.get('origin', 'N/A'),
                raw_data.get('price', 'N/A'),
                raw_data.get('production_date', 'N/A'),
                raw_data.get('scraping_time', 'N/A'),
                raw_data.get('subtitle', 'N/A'),
                raw_data.get('title', 'N/A'),
                raw_data.get('type', 'N/A'),
                raw_data.get('url', 'N/A')
            )
            transformed_data_list.append(transformed_data)
        return transformed_data_list
    