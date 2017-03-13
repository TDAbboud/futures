# Futures

> ETL pipeline built on Amazon EMR for futures ticker data

## Setup

1. Create an Amazon S3 bucket with the following structure

    ```
    tickerdata
    ├── bootstrap
    ├── cleaned
    └── raw
    ```

2. Upload all ticker data as `.csv` files to the raw bucket
3. Upload all bootstrap scripts to the bootstrap directory

## Running
1. Install the [AWS CLI](https://aws.amazon.com/cli/)
2. Start an EMR cluster via `start_emr.sh` or through the EMR web UI
    - If jupyter is needed, then create a bootstrap action to run the `install_jupyter.sh` file in the bootstrap directory
3. Transfer the desired scripts to the master node
4. ssh into the master node *(forwarding the jupyter port if needed)*
    -  ` ssh -L 8888:localhost:8888 -i <aws-ssh-key> hadoop@<master-node>`
5. Set the SPARK_HOME environment variable
    - `export SPARK_HOME=/usr/lib/spark`
6. submit a spark application and run the desired scripts
    - `spark-submit --deploy-mode cluster --master yarn <script>`

