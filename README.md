
# TrackerAutoLogin

Github URL: https://github.com/mastiffmushroom/TrackerAutoLogin

Dockerhub URL: https://hub.docker.com/r/mastiffmushroom/trackerautologin

This is a docker file to automate the logging in of torrent trackers every few hours so your account can stay active and you can still have access to downloading your Linux install files.

**DISCLAIMER**: This software doesn't download any illegal files, it simply logs in with pre-given credentials. I do not condone using this software to illegally obtain items.

## Currently supported sites

* Aither (Aither.cc)
* AlphaRatio (AlphaRatio.cc)
* ExtremeBits (Extremebits.net)
* Gay-Torrents (Gay-Torrents.org)
* HappyFappy (HappyFappy.org)
* HD-Space [mostly working] (HD-Space.org)
* MyAnonmouse (MyAnonamouse.net)
* Pornbay (Pornbay.org)
* PussyTorrents (PussyTorrents.org)
* TorrentLeech (TorrentLeech.org)
* TV Vault (TV-Vault.me)

## Configuration

This software uses Docker, so please look into how to install it on Docker. As I run linux, I will only be able to tell you how to run it on linux.

The configuration files are loaded under `config/`. On the github page, it has an example of each one, and on the first runtime it will download these directly from the github and put them in the corresponding `config/` folder. If you mount your host path to the container, you can edit these from the container and maintain persistance with updates.

The code lookds for `user_config.json` while `config/` only has `user_config_sample.json` to give you an idea on how to fill it out. You only need to put in information for websites that you have login details for -- otherwise the login will fail.

`LogLevel` is the level you want to write logs to. All logs are written inside the docker container to `/app/Logfile/TrackerLogin.log`. `LogLevel` takes 3 values [`debug`, `warning`, `error`].

`Hours_Rerun` in the config file is the maximum number of hours to to wait before each run. What this software does, is it chooses a random range between `Hours_Rerun/2` and `Hours_Rerun` before attempting the next rerun. The reason for this is if some sites have bot login detection, it will be much harder to detect if you're not logging in the same time every day.

`CheckConnectionURL` is a configurable parameter. What you feed in here is a URL that you want to check against to make sure you're connected to the internet. It will try to load this webpage each time to make sure that you have an internet connection before trying to log into the trackers. If the connection to this URL fails, it will skip trying the trackers.

## How to Run

You can run this 3 different ways

### Directly on your machine

```bash
cd /path/to/TrackerAutoLogin/
docker build . -t trackerautologin
docker run -v /path/on/your/system/:/app/config/ -it trackerautologin
```
After running this, stop the run, navigate to `/path/on/your/system/` and update the `user_config.json` with your login instructions for each of the trackers that you have access to.

### Through dockerhub

```bash
docker pull mastiffmushroom/trackerautologin
```

Then you can simply run it using the same command as above

```bash
docker run -v /path/on/your/system/:/app/config/ -it mastiffmushroom/trackerautologin
```

#### Note about running locally

To view the log file, you first need to run `docker ps` and get the phrase in the format of `word1_word2` under the `NAME` column. For the example below, replace `WORD1_WORD2` with what you found in the `NAME` column.

```bash
docker exec -it WORD1_WORD2 bash
cd /app/config/logs/
more trackerautologin.log
```

### Unraid Community Applications

This app is now located on the Unraid Community Applications and can be ran as a typical app there as well.


## Future work

One thing I would like to add to this is for it to take a screenshot of your profile stats with every successful login, with it keeping the most recent 5 photos. The benefit of this is that you will always have your stats on how much data you shared when you downloaded your Linux isos. 
