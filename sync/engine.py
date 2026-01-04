# Sync orchestration logic

from ..fetcher.client import HTTPClient
from ..parser.detector import detect_page_type
from ..parser.centre_parser import parse_centre_list
from ..parser.datewise_parser import parse_datewise_summary
from ..parser.farmer_parser import parse_farmer_details
from ..db.repositories.centre_repo import CentreRepository
from ..db.repositories.summary_repo import SummaryRepository
from ..db.repositories.farmer_repo import FarmerRepository
from ..utils.hashing import compute_html_hash
from ..core.constants import BASE_URL
from ..config.settings import Settings
import time

class SyncEngine:
    """
    Orchestration engine for synchronizing data from the government website.
    """
    
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.centre_repo = CentreRepository(db_connection)
        self.summary_repo = SummaryRepository(db_connection)
        self.farmer_repo = FarmerRepository(db_connection)
        self.http_client = HTTPClient()
        self.settings = Settings()
    
    def sync_all_centres(self):
        """
        Synchronizes all centres from the government website.
        """
        print("Starting sync of all centres...")
        
        # Fetch the main centre list page
        response = self.http_client.get(BASE_URL)
        html_content = response.text
        html_hash = compute_html_hash(html_content)
        
        # Parse the centre list
        centres = parse_centre_list(html_content, BASE_URL)
        
        # Save centres to database
        for centre in centres:
            self.centre_repo.create_or_update_centre(
                name=centre['name'],
                url=centre['url']
            )
        
        print(f"Synced {len(centres)} centres")
        return len(centres)
    
    def sync_centre_datewise_data(self, centre_name):
        """
        Synchronizes date-wise data for a specific centre.
        """
        print(f"Starting sync of date-wise data for centre: {centre_name}")
        
        # Get centre from database
        centre = self.centre_repo.get_centre_by_name(centre_name)
        if not centre:
            print(f"Centre not found: {centre_name}")
            return 0
        
        # Fetch the date-wise summary page
        response = self.http_client.get(centre['url'])
        html_content = response.text
        html_hash = compute_html_hash(html_content)
        
        # Parse the date-wise summary
        datewise_data = parse_datewise_summary(html_content, centre['url'])
        
        # Save date-wise summaries to database
        count = 0
        for date_entry in datewise_data['dates']:
            self.summary_repo.create_or_update_summary(
                centre_id=centre['id'],
                date=date_entry['date'],
                farmer_count=date_entry['farmer_count'],
                quantity=date_entry['quantity'],
                amount=date_entry['amount'],
                details_url=date_entry['details_url'],
                html_hash=html_hash
            )
            count += 1
        
        print(f"Synced {count} date-wise entries for centre: {centre_name}")
        return count
    
    def sync_farmer_details(self, centre_name, date):
        """
        Synchronizes farmer details for a specific centre and date.
        """
        print(f"Starting sync of farmer details for centre: {centre_name}, date: {date}")
        
        # Get centre from database
        centre = self.centre_repo.get_centre_by_name(centre_name)
        if not centre:
            print(f"Centre not found: {centre_name}")
            return 0
        
        # Get date-wise summary to get the details URL
        summary = self.summary_repo.get_summary_by_centre_and_date(centre['id'], date)
        if not summary or not summary['details_url']:
            print(f"No details URL found for centre: {centre_name}, date: {date}")
            return 0
        
        # Fetch the farmer details page
        response = self.http_client.get(summary['details_url'])
        html_content = response.text
        html_hash = compute_html_hash(html_content)
        
        # Parse the farmer details
        farmer_data = parse_farmer_details(html_content)
        
        # Delete existing transactions for this centre and date to avoid duplicates
        self.farmer_repo.delete_transactions_by_centre_and_date(centre['id'], date)
        
        # Save farmer transactions to database
        count = 0
        for transaction in farmer_data['transactions']:
            self.farmer_repo.create_or_update_transaction(
                centre_id=centre['id'],
                date=date,
                farmer_id=transaction['farmer_id'],
                farmer_name=transaction['farmer_name'],
                village=transaction['village'],
                quantity=transaction['quantity'],
                amount=transaction['amount'],
                transaction_time=transaction['transaction_time']
            )
            count += 1
        
        print(f"Synced {count} farmer transactions for centre: {centre_name}, date: {date}")
        return count
    
    def close(self):
        """
        Closes the HTTP client.
        """
        self.http_client.close()