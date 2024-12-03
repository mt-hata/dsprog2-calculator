SELECT 
    DATE_PART('month', init_license_dt) AS month,
    business_type,
    COUNT(*) AS store_count
FROM 
    minato_restaurant
WHERE 
    DATE_PART('year', init_license_dt) = 2022
GROUP BY 
    DATE_PART('month', init_license_dt),
    business_type
ORDER BY 
    month ASC, store_count DESC;
