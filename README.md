# scraper_dominios

Exploring Github Actions to scrape data from argentina internet domain registrations.

The data is found [here](https://github.com/lbellomo/scraper_dominios/tree/master/data), it is named in the form Year Month Day .csv and is updated every night when there is new data in the [official bulletin](https://www.boletinoficial.gob.ar/seccion/cuarta).

The fun part is that the data is updated via a Github Action ([found here](https://github.com/lbellomo/scraper_dominios/blob/master/.github/workflows/main.yml) that runs every night with a cron and commits the new data to the repo if there is any.

## Limitations of using Github Actions as scrapers

The biggest limitation is that there is a [maximum](https://help.github.com/en/github/setting-up-and-managing-billing-and-payments-on-github/about-billing-for-github-actions#about-billing-for-github-actions) of 2000 minutes to run jobs in the actions per account. So it is not useful for scrapers that run for a long time or very often but a good option for small scrapers.

The [minimum cron](https://help.github.com/en/actions/configuring-and-managing-workflows/configuring-a-workflow#triggering-a-workflow-with-events) interval is 5 minutes (maybe you can overcome this by putting more crons).

You have to install the dependencies every time you run the action (which can be time consuming for large projects), but you can [cache the dependencies](https://help.github.com/en/actions/configuring-and-managing-workflows/caching-dependencies-to-speed-up-workflows) to save time.

The [maximum size](https://help.github.com/en/github/managing-large-files/what-is-my-disk-quota#file-and-repository-size-limitations) of the repo (with the whole story) is 100 GB and a file is 100 MB.

## TODO
- [ ]: Scrape old domains.

