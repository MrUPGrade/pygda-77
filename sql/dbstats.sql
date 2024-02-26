-- Kill all connections beside mine
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE
  -- don't kill my own connection!
    pid <> pg_backend_pid()
  AND datname = 'db';


-- Postgres settings
select *
from pg_settings
where name like '%';

-- DB size
SELECT relname                                                                 as "Table",
       pg_size_pretty(pg_total_relation_size(relid))                           As "Total size",
       pg_size_pretty(pg_relation_size(relid))                                 as "Table only size",
       pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as "External size"
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;