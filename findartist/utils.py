from rq.job import Job
def job_is_successful(job: Job, uri_prefix: str):
    """
    Checks if the job result starts with a certain prefix
    @param job: the job object
    @param uri_prefix: the prefix to check for
    @return: Boolean representing if the job result starts with the prefix
    """
    return type(job.result) == str and job.result.startswith(uri_prefix)
