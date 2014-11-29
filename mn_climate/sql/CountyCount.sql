CREATE OR REPLACE VIEW county_count AS
(SELECT 
county.gid,county.countyname,county.geom,
  CAST(SUM(CASE WHEN ST_Contains(county.geom,impact.geom) THEN 1 ELSE 0 END) AS integer ) as count
FROM
 county, impact
GROUP BY
county.gid
);
