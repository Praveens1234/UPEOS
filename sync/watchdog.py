# Stuck-job detection

import time
import threading
from datetime import datetime

class SyncWatchdog:
    """
    Monitors synchronization jobs for timeouts and stuck processes.
    """
    
    def __init__(self, timeout_seconds=300):  # 5 minutes default timeout
        self.timeout_seconds = timeout_seconds
        self.active_jobs = {}
        self.monitor_thread = None
        self.monitoring = False
    
    def start_monitoring(self):
        """
        Starts the monitoring thread.
        """
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """
        Stops the monitoring thread.
        """
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def register_job(self, job_id):
        """
        Registers a new job for monitoring.
        
        Args:
            job_id (str): Unique identifier for the job
        """
        self.active_jobs[job_id] = {
            'start_time': time.time(),
            'last_checkin': time.time(),
            'timed_out': False
        }
    
    def checkin_job(self, job_id):
        """
        Updates the last check-in time for a job.
        
        Args:
            job_id (str): Unique identifier for the job
        """
        if job_id in self.active_jobs:
            self.active_jobs[job_id]['last_checkin'] = time.time()
    
    def unregister_job(self, job_id):
        """
        Unregisters a job from monitoring.
        
        Args:
            job_id (str): Unique identifier for the job
        """
        if job_id in self.active_jobs:
            del self.active_jobs[job_id]
    
    def is_job_stuck(self, job_id):
        """
        Checks if a job is stuck (timed out).
        
        Args:
            job_id (str): Unique identifier for the job
            
        Returns:
            bool: True if job is stuck, False otherwise
        """
        if job_id not in self.active_jobs:
            return False
        
        job_info = self.active_jobs[job_id]
        if job_info['timed_out']:
            return True
        
        elapsed = time.time() - job_info['last_checkin']
        return elapsed > self.timeout_seconds
    
    def _monitor_loop(self):
        """
        Main monitoring loop that runs in a separate thread.
        """
        while self.monitoring:
            current_time = time.time()
            for job_id, job_info in list(self.active_jobs.items()):
                elapsed = current_time - job_info['last_checkin']
                if elapsed > self.timeout_seconds and not job_info['timed_out']:
                    # Mark job as timed out
                    self.active_jobs[job_id]['timed_out'] = True
                    print(f"WARNING: Job {job_id} has timed out after {elapsed} seconds")
            
            # Sleep for a short interval before checking again
            time.sleep(10)  # Check every 10 seconds