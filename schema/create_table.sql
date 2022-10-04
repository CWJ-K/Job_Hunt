
USE job

CREATE TABLE jobs (
    job_id VARCHAR(7) NOT NULL,
    job_title VARCHAR(50) NOT NULL,
    company_name VARCHAR(50) NOT NULL,
    company_addr VARCHAR(10),
    job_url VARCHAR(2083) NOT NULL,
    period VARCHAR(10),
    appear_date DATE NOT NULL,
    updated_date DATE
);


