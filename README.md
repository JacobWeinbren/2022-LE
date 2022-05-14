# LE 2022

## Sources

With many thanks to Election Maps UK, Britain Elects, Andrew Teale, Ballot Box, Electoral Calculus, The Ordnance Survey and The Boundary Commission 

### Full Extent Boundaries

-   [Dec 2017](https://geoportal.statistics.gov.uk/datasets/ons::wards-december-2017-full-extent-boundaries-in-uk-wgs84/about)
-   [Dec 2018](https://geoportal.statistics.gov.uk/datasets/ons::wards-december-2018-full-extent-boundaries-gb/about)
-   [Electoral Calculus](https://www.electoralcalculus.co.uk/geoserver/)
-   OS Unitary Electoral Division

### Results

-   [Eng + Wal + Sco 2022](https://docs.google.com/spreadsheets/d/1RmvhrMUb8-zxqipiz8RDTzMmhRnl-KEUiZXHILMxEQA/edit#gid=494045480)
-   [Eng 2018](https://docs.google.com/spreadsheets/d/1ZaAenyQkbwcxdl4GiPUj73rpi2oocpG3PmwAnypAQZA/edit#gid=635729702)
-   [Wal 2017](https://www.andrewteale.me.uk/leap/councils/2017/#area59) + [Spreadsheet](https://docs.google.com/spreadsheets/d/1KFklLbaAHSq6Tlxf-LUpKCpj2JCCyvUfoBPGsazKyBc/edit?usp=sharing)
-   [Sco 2017](https://ballotbox.scot/councils/2017-elections)

## Process

-   python3 -m venv env
-   source env/bin/activate

-   Merge 2022 wards Boundaries
-   Parwise Clip wards with 2017/18 (as they are difference source)
-   Spatial join with districts

-   Now we are going to find the minimum area that encompasses both the old and new maps

    1. Make four regions (Wales, Scotland, England, London) from country region
    3. Remove attributes

-   Now we intersect with wards and export

    1. Pairwise intersect wards with the regions to produce wards_eng_2022, wards_wal_2022, wards_lon_2022, wards_sco_2022
    2. Pairwise intersect wards with the regions to produce wards_eng_2018, wards_wal_2017, wards_lon_2018, wards_sco_2017
    3. Export to Geojson

-   Cd into scripts and run boundary_changes.py

-   Remove extra attributes, simplify (use mapshaper ~1mb topojson)