import os

class S3Sync:

    '''
    here folder means local folder where we are goin to save our final model.pkl whihc is final_models
    aws_bucket_url : means cloud folder in S3 bucket
    '''

    '''
    Here we are creating command which is used to sync our local folder to S3 bucket
    '''
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        command = f"aws s3 sync {folder} {aws_bucket_url}"
        os.system(command)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        command = f"aws s3 sync {aws_bucket_url} {folder}"
        os.system(command)