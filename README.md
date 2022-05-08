# LE 2022

## Sources

### Full Extent Boundaries

-   [Dec 2017](https://geoportal.statistics.gov.uk/datasets/ons::wards-december-2017-full-extent-boundaries-in-uk-wgs84/about)
-   [Dec 2018](https://geoportal.statistics.gov.uk/datasets/ons::wards-december-2018-full-extent-boundaries-gb/about)
-   [May 2022](https://osdatahub.os.uk/downloads/open/BoundaryLine)

### Results

Many Thanks to UK Election Maps, Britain Elects, Andrew Teale and Ballot Box.

-   [Eng + Wal + Sco 2022](https://docs.google.com/spreadsheets/d/1RmvhrMUb8-zxqipiz8RDTzMmhRnl-KEUiZXHILMxEQA/edit#gid=494045480)
-   [Eng 2018](https://docs.google.com/spreadsheets/d/1ZaAenyQkbwcxdl4GiPUj73rpi2oocpG3PmwAnypAQZA/edit#gid=635729702)
-   [Wal 2017](https://www.andrewteale.me.uk/leap/councils/2017/#area59) + [Spreadsheet](https://docs.google.com/spreadsheets/d/1KFklLbaAHSq6Tlxf-LUpKCpj2JCCyvUfoBPGsazKyBc/edit?usp=sharing)
-   [Sco 2017](https://ballotbox.scot/councils/2017-elections)

## Process

-   Merge 2022 wards Boundaries

-   Now we are going to find the minimum area that encompasses both the old and new maps

    1. Make four regions (Wales, Scotland, England, London) - make sure to include the Highlands (use join)
    2. Intersect regions with 2017/18 (as they are difference source)

-   Now we intersect with wards and export

    1. Pairwise intersect wards with the regions to produce wards_eng_2022, wards_wal_2022, wards_lon_2022, wards_sco_2022
    2. Pairwise intersect wards with the regions to produce wards_eng_2018, wards_wal_2017, wards_lon_2018, wards_sco_2017
    3. Export to Geojson

-   Cd into scripts and run boundary_changes.py

-   Remove extra attributes, simplify (.1km for LDN + WAL, .5km for ENG)