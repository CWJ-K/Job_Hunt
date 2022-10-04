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

5. unit testing:

6. Packages
   * loguru
   * sqlalchemy
   * pytest_check
   * pytest-assume
   * pymysql

# Progress
- [x] structure of the project
- [x] create a data schema in mysql
- [ ] deal with company tags(type: list) become two rows
- [ ] clear advertisement data
- [ ] make sure datatype


# Run
```bash
  python src/main.py

```