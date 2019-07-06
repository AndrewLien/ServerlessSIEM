# ServerlessSIEM
An open source project that will dive through how to configure an end to end SIEM solution all through google cloud platform's serverless technologies.

## How to run
First, ensure you have a service account credentials file, and set that in the variables.tf

Then, you can simply run:

```
terraform init
terraform plan
terraform apply
```

There's a nifty script in the `scripts` directory that you can use to test your dataflow pipeline. 

```
cd scripts
pip install -r requirements.txt
python evtx_dump.py <location_of_evtx_file> <pubsub_topic> <gcp_project_id>
python evtx_dump.py %SystemRoot%\System32\Winevt\Logs\Security.evtx windows-eventstream serverless-siem
```

