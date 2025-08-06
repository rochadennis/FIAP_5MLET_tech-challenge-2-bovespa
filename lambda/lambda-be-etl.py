import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    job_name = "glue-job-etl-b3"
    
    response = glue.start_job_run(JobName=job_name)
    
    print(f"Glue Job iniciado: {response['JobRunId']}")
    return {
        'statusCode': 200,
        'body': f"Glue Job {job_name} iniciado com sucesso!"
    }
