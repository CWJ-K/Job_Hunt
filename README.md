# Introduction 

The product can crawl previous 7 days' job information from the 104 website every day. If there are new jobs, you will receive a mail


# Requirements
1. Data Source
    * crawl previous 7 days' data
    * Use .yml:
      * location: Taipei
      * content of jobs: e.g. Python
      * mail 
    * data includes:
      *  the index of the page to check duplicated data
      *  date of the information => start_date
      *  company name
      *  job title
      *  work experience
      *  location
      *  content of jobs
      *  link
      *  update_date: after the start date, companies update their jobs again
2. Data Storage
   * delete the previous one month's data 
   * if data is duplicated, do not store it, just skip, but update the update_date
3. Mail 
   * if new job appear (start_date, not in the db before), send mails
     * with the information of updated jobs

4.  environment:
    * local => free cloud


# Progress
- [x] structure of the project
- [ ] create a excel file and check if it exists
  - [ ] for the first time create an excel file, set a empty file, but with a header
    - [ ] apped data, only the first time, header is kept
- [ ] deal with company tags(type: list) become two rows
- [ ] clear advertisement data