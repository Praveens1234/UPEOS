#!/usr/bin/env python3
"""
Full Sync Script for UPEOS System
Parallel processing implementation for fast, complete data synchronization
"""

import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("FullSync")

class FullSyncEngine:
    def __init__(self, max_workers=8, detail_workers_per_centre=3):
        self.max_workers = max_workers
        self.detail_workers_per_centre = detail_workers_per_centre
        self.rate_limiter = RateLimiter()
        # Use thread-local storage for database connections
        self.local = threading.local()
        
    @property
    def db(self):
        """Thread-local database connection"""
        if not hasattr(self.local, 'db'):
            from upeos.db.connection import DatabaseConnection
            self.local.db = DatabaseConnection()
        return self.local.db
    
    @property
    def sync_engine(self):
        """Thread-local sync engine"""
        if not hasattr(self.local, 'sync_engine'):
            from upeos.sync.engine import SyncEngine
            self.local.sync_engine = SyncEngine(self.db)
        return self.local.sync_engine
    
    @property
    def centre_repo(self):
        """Thread-local centre repository"""
        if not hasattr(self.local, 'centre_repo'):
            from upeos.db.repositories.centre_repo import CentreRepository
            self.local.centre_repo = CentreRepository(self.db)
        return self.local.centre_repo
    
    @property
    def summary_repo(self):
        """Thread-local summary repository"""
        if not hasattr(self.local, 'summary_repo'):
            from upeos.db.repositories.summary_repo import SummaryRepository
            self.local.summary_repo = SummaryRepository(self.db)
        return self.local.summary_repo
    
    def run_full_sync(self):
        """Main entry point for full synchronization"""
        logger.info("Starting full synchronization...")
        start_time = time.time()
        
        try:
            # Phase 1: Discover all centres (in main thread)
            logger.info("Phase 1: Discovering all centres...")
            from upeos.sync.engine import SyncEngine
            from upeos.db.connection import DatabaseConnection
            
            # Create a new connection for the main thread
            main_db = DatabaseConnection()
            main_sync_engine = SyncEngine(main_db)
            centre_count = main_sync_engine.sync_all_centres()
            main_sync_engine.close()
            main_db.close()
            logger.info(f"Discovered {centre_count} centres")
            
            # Phase 2: Get all centres from DB
            main_db = DatabaseConnection()
            from upeos.db.repositories.centre_repo import CentreRepository
            main_centre_repo = CentreRepository(main_db)
            centres = main_centre_repo.get_all_centres()
            main_db.close()
            logger.info(f"Retrieved {len(centres)} centres from database")
            
            # Phase 3: Process all centres in parallel
            logger.info("Phase 3: Processing centres in parallel...")
            self.process_centres_parallel(centres)
            
            # Phase 4: Process farmer details for all dates
            logger.info("Phase 4: Processing farmer details...")
            self.process_all_farmer_details(centres)
            
            end_time = time.time()
            logger.info(f"Full synchronization completed in {end_time - start_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Error during full sync: {e}")
            raise
    
    def process_centres_parallel(self, centres):
        """Process all centres in parallel to fetch date-wise summaries"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all centre processing tasks
            future_to_centre = {
                executor.submit(self.process_centre_summaries, centre): centre 
                for centre in centres
            }
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(future_to_centre):
                centre = future_to_centre[future]
                try:
                    count = future.result()
                    completed += 1
                    logger.info(f"Completed {centre['name']}: {count} date entries")
                    logger.info(f"Progress: {completed}/{len(centres)} centres")
                except Exception as e:
                    logger.error(f"Error processing centre {centre['name']}: {e}")
    
    def process_centre_summaries(self, centre):
        """Process a single centre to fetch all date-wise summaries"""
        # Rate limiting
        self.rate_limiter.wait_if_needed("eproc.up.gov.in")
        
        # Fetch and save date-wise summaries
        count = self.sync_engine.sync_centre_datewise_data(centre['name'])
        return count
    
    def process_all_farmer_details(self, centres):
        """Process farmer details for all centres and dates"""
        # Get all dates for all centres
        total_dates = 0
        
        # Get summaries using main thread connection
        from upeos.db.connection import DatabaseConnection
        from upeos.db.repositories.summary_repo import SummaryRepository
        main_db = DatabaseConnection()
        main_summary_repo = SummaryRepository(main_db)
        
        all_tasks = []
        for centre in centres:
            summaries = main_summary_repo.get_summaries_by_centre(centre['id'])
            total_dates += len(summaries)
            for summary in summaries:
                all_tasks.append((centre['name'], summary['date']))
        
        main_db.close()
        
        logger.info(f"Processing farmer details for {total_dates} dates across {len(centres)} centres")
        
        # Process in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {
                executor.submit(self.process_date_farmer_details, centre_name, date): (centre_name, date)
                for centre_name, date in all_tasks
            }
            
            # Collect results
            processed_dates = 0
            for future in as_completed(future_to_task):
                centre_name, date = future_to_task[future]
                try:
                    count = future.result()
                    processed_dates += 1
                    logger.info(f"Completed farmer details for {centre_name} on {date}: {count} transactions")
                    logger.info(f"Farmer details progress: {processed_dates}/{total_dates} dates")
                except Exception as e:
                    logger.error(f"Error processing farmer details for {centre_name} on {date}: {e}")
    
    def process_date_farmer_details(self, centre_name, date):
        """Process farmer details for a specific centre and date"""
        # Rate limiting
        self.rate_limiter.wait_if_needed("eproc.up.gov.in")
        
        # Fetch and save farmer details
        count = self.sync_engine.sync_farmer_details(centre_name, date)
        return count
    
    def cleanup(self):
        """Cleanup resources"""
        # Clean up thread-local resources
        if hasattr(self.local, 'sync_engine'):
            self.local.sync_engine.close()
        if hasattr(self.local, 'db'):
            self.local.db.close()
        logger.info("Cleanup completed")

class RateLimiter:
    def __init__(self):
        self.domain_last_request = {}
        self.min_delay = 1.0  # seconds
        self.lock = threading.Lock()
    
    def wait_if_needed(self, domain):
        with self.lock:
            last_req = self.domain_last_request.get(domain, 0)
            elapsed = time.time() - last_req
            if elapsed < self.min_delay:
                time.sleep(self.min_delay - elapsed)
            self.domain_last_request[domain] = time.time()

def main():
    """Main function to run full sync"""
    logger.info("Initializing full sync engine...")
    sync_engine = FullSyncEngine(max_workers=8, detail_workers_per_centre=3)
    
    try:
        sync_engine.run_full_sync()
        logger.info("Full sync completed successfully!")
    except Exception as e:
        logger.error(f"Full sync failed: {e}")
        raise
    finally:
        sync_engine.cleanup()

if __name__ == "__main__":
    main()