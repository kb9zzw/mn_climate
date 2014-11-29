CREATE OR REPLACE VIEW zip_count AS
(SELECT 
zip.gid,zip.zip_code,zip.geom,
  CAST(SUM(CASE WHEN ST_Contains(zip.geom,impact.geom) THEN 1 ELSE 0 END) AS integer) AS count
FROM
 zip, impact
GROUP BY
zip.gid
);
