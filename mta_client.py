import datetime
from nyct_gtfs import NYCTFeed

class MTAClient:
    """
    Handles fetching and parsing real-time MTA data.
    Hardware-independent core logic.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key

    def get_next_arrivals(self, stop_id, line='L', max_results=3, max_minutes=60):
        """
        Fetches next arrivals for a specific stop_id (e.g. L11N) on a given line.
        Returns a list of minutes: [4, 12, 18]
        """
        arrivals = []
        now = datetime.datetime.now(datetime.timezone.utc)

        try:
            # NYCTFeed handles the feed URL and parsing
            feed = NYCTFeed(line, api_key=self.api_key)
            # nyct-gtfs 1.3.2 uses filter_trips and headed_for_stop_id
            trips = feed.filter_trips(headed_for_stop_id=stop_id)
            
            for trip in trips:
                for update in trip.stop_time_updates:
                    # Match exact stop_id (with N/S suffix)
                    if update.stop_id == stop_id:
                        arrival_time = update.arrival
                        if arrival_time:
                            # Handle timezone differences
                            if arrival_time.tzinfo is None:
                                arrival_time = arrival_time.replace(tzinfo=datetime.timezone.utc)
                            
                            diff = (arrival_time - now).total_seconds()
                            minutes = int(diff / 60)
                            
                            # Clamp values: ignore negative or too far in the future
                            if 0 <= minutes <= max_minutes:
                                arrivals.append(minutes)
                                break # only first match per trip for this stop
        except Exception as e:
            print(f"Error fetching MTA data for line {line}: {e}")
            raise e # Let the caller handle retries

        # Sort and limit
        arrivals.sort()
        return arrivals[:max_results]

if __name__ == "__main__":
    # Test (Bedford Av Northbound)
    client = MTAClient()
    try:
        results = client.get_next_arrivals("L11N", "L")
        print(f"Next L trains at Bedford Av (N): {results}")
    except Exception as e:
        print(f"Could not fetch data: {e}")
