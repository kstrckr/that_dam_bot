# That DAM Bot

Gilt.com was ending it's contract with a 3rd party digital asset management service (Evolphin). The only way to retrieve all assets for local backup was to manually download directories through Evolphin's command line tool. 17 Terabytes of images were spread across hundreds of directories and manually downloading them all efficiently would have been a major time sink.

Additionally, the DAM server was taken offline every night for it's own checkpoint creation, so any downloads would be terminated and many hours of download time would be lost before the next workday began.

This Python program allowed us to generate a list of directories to track and download automatically through a local sqlite database. Any unexpected download interuptions would be detected and the process would restart where it left off. Additionally it would detect the overnight server downtime and log it's self back in as soon as the server was back online. 

With this level of set-it-and-forget-it functionality the entire archive was copied to local storage with only minutes of work required every few days.