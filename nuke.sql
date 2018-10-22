

select *
from "headlineScraper_headlinerevision"
where title='Min overgriper var ikke et monster. Han var et menneske.';

select *
from "articleScraper_revision"
where article_id=7065;

UPDATE "articleScraper_revision"
  set timestamp='2017-01-01'
where article_id=7065;

/* NUKE */
DELETE FROM "submission_limit";
DELETE FROM "submission_headlinesummary";
DELETE FROM "submission_userreport";
DELETE FROM "submission_report";
DELETE FROM "submission_reportcategory";
DELETE FROM "headlineScraper_rank";
DELETE from "headlineScraper_headlinerevision";
DELETE from "articleScraper_articleimage_photographers";
DELETE from "articleScraper_revision_images";
DELETE from "articleScraper_articleimage";
DELETE from "articleScraper_photographer";
DELETE from "articleScraper_revision_journalists";
DELETE from "articleScraper_journalist";
DELETE FROM "articleScraper_revision";
DELETE FROM "articleScraper_article";
DELETE from "headlineScraper_headline";


/* Articles only */
TRUNCATE "headlineScraper_headline"CASCADE;