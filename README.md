
# TrackerAutoLogin

Github URL: https://github.com/mastiffmushroom/TrackerAutoLogin
Dockerhub URL: https://hub.docker.com/repository/registry-1.docker.io/mastiffmushroom/trackerautologin/general

This is a docker file to automate the logging in of torrent trackers every few hours so your account can stay active and you can still have access to downloading your Linux install files.

**DISCLAIMER**: This software doesn't download any illegal files, it simply logs in with pre-given credentials. I do not condone using this software to illegally obtain items.

## Currently supported sites

* AlphaRatio
* TorrentLeech
* Aither

## Configuration

This software uses Docker, so please look into how to install it on Docker. As I run linux, I will only be able to tell you how to run it on linux.

Once the files are downloaded, rename `user_config_sample.json` to `user_config.json`. From there, open up `user_config.json` and delete all of the sites that you don't have login details for. For each individual site, you can put in your appropriate username and password.

`LogLevel` is the level you want to write logs to. All logs are written inside the docker container to `/app/Logfile/TrackerLogin.log`. `LogLevel` takes 3 values [`debug`, `warning`, `error`].

`Hours_Rerun` in the config file is the maximum number of hours to to wait before each run. What this software does, is it chooses a random range between `Hours_Rerun/2` and `Hours_Rerun` before attempting the next rerun. The reason for this is if some sites have bot login detection, it will be much harder to detect if you're not logging in the same time every day.

`CheckConnectionURL` is a configurable parameter. What you feed in here is a URL that you want to check against to make sure you're connected to the internet. It will try to load this webpage each time to make sure that you have an internet connection before trying to log into the trackers. If the connection to this URL fails, it will skip trying the trackers.

## How to Run

I will be moving this to DockerHub as well as try to get it uploaded on the Unraid Community Apps, however this will take some time. 

In the meantime, on linux you can run it with the following commands

```bash
cd /path/to/TrackerAutoLogin/
sudo docker build . -t trackerautologin
sudo docker run -it trackerautologin
```

To view the log file, you first need to run `docker ps` and get the phrase in the format of `word1_word2` under the `NAME` column. For the example below, replace `WORD1_WORD2` with what you found in the `NAME` column.

```bash
docker exec -it WORD1_WORD2 bash
cd /app/Logfile/
more TrackerLogfile.log
```

## Future work

One thing I would like to add to this is for it to take a screenshot of your profile stats with every successful login, with it keeping the most recent 5 photos. The benefit of this is that you will always have your stats on how much data you shared when you downloaded your Linux isos. 
