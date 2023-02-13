# socialblock-data-processor
The data-engine for the SocialBlock platform.
We used Python to design the main pipelines and processors. After logging in to the dashboard you can see the processors. Each processor can be selected individually or with others. You need to add a string of transaction hashes which are separated with a comma like tx1,tx2,..,txn, then select your desire processors and hit the run pipeline button. 
![Alt text](public/processors.png)
Note: If you don't enter any transaction hashes it will start to get 100 first transactions of your MongoDB instance to start the processors.
