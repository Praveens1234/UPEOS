# Catbox upload via curl

import os
import json
import subprocess
from ..config.settings import Settings

class ReportUploader:
    """
    Uploads generated reports to Catbox.moe using curl.
    """
    
    def __init__(self):
        self.settings = Settings()
    
    def upload_report(self, file_path):
        """
        Uploads a report file to Catbox.moe.
        
        Args:
            file_path (str): Path to the file to upload
            
        Returns:
            dict: Upload result with URL and status
        """
        if not os.path.exists(file_path):
            return {
                'status': 'error',
                'message': f'File not found: {file_path}'
            }
        
        if not self.settings.enable_cloud_upload:
            return {
                'status': 'skipped',
                'message': 'Cloud upload is disabled in settings'
            }
        
        try:
            # Use curl to upload the file to Catbox.moe
            # Catbox.moe API endpoint for file uploads
            url = "https://catbox.moe/user/api.php"
            
            # Prepare the curl command
            cmd = [
                "curl",
                "-X", "POST",
                "-F", f"reqtype=fileupload",
                "-F", f"userhash=",
                "-F", f"fileToUpload=@{file_path}",
                url
            ]
            
            # Execute the curl command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Successful upload
                upload_url = result.stdout.strip()
                
                # Verify that we got a valid URL
                if upload_url.startswith("http"):
                    return {
                        'status': 'success',
                        'url': upload_url,
                        'message': 'File uploaded successfully'
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f'Upload failed: Invalid response from server: {upload_url}'
                    }
            else:
                # Upload failed
                return {
                    'status': 'error',
                    'message': f'Upload failed: {result.stderr}'
                }
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'message': 'Upload timed out'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Upload failed: {str(e)}'
            }
    
    def upload_and_register_report(self, file_path):
        """
        Uploads a report and registers the upload URL.
        
        Args:
            file_path (str): Path to the file to upload
            
        Returns:
            dict: Upload result with URL and status
        """
        # First, perform the upload
        upload_result = self.upload_report(file_path)
        
        # If upload was successful, update the report registry
        if upload_result['status'] == 'success':
            # Read existing reports
            if os.path.exists(self.settings.creport_registry):
                with open(self.settings.creport_registry, 'r') as f:
                    reports = json.load(f)
            else:
                reports = []
            
            # Find the report and update it with the upload URL
            for report in reports:
                if report.get('file_path') == file_path:
                    report['upload_url'] = upload_result['url']
                    break
            
            # Write back to file
            with open(self.settings.creport_registry, 'w') as f:
                json.dump(reports, f, indent=2)
        
        return upload_result