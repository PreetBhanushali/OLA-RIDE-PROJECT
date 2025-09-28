-- 1. Retrieve all successful bookings
SELECT o.* 
FROM ola o
JOIN booking_status b 
ON o.status_id = b.status_id
WHERE b.status = "Success"


-- 2. Find the average ride distance for each vehicle type
SELECT v.vehicle_type,ROUND(AVG(o.ride_distance),2) AS avg_distance
FROM ola o
JOIN vehicle_types v 
ON o.vehicle_type_id = v.vehicle_type_id
WHERE o.status_id = "S-S"
GROUP BY v.vehicle_type
	
	
-- 3. Get the total number of cancelled rides by customers
SELECT 
	COUNT(booking_id) AS total_customer_cancellations
FROM ola o
WHERE canceled_rides_by_customer NOT IN ("Not Applicable","Not-Applicable")
	

-- 4. List the top 5 customers who booked the highest number of rides
SELECT 
	customer_id, COUNT(booking_id) AS total_rides
FROM ola o
GROUP BY customer_id
ORDER BY total_rides DESC
LIMIT 5


-- 5. Get the number of rides cancelled by drivers due to personal and car-related issues
SELECT 
	canceled_rides_by_driver,
	COUNT(booking_id) AS total
FROM ola o 
WHERE canceled_rides_by_driver IN ("Personal & Car related issue")
GROUP BY canceled_rides_by_driver


-- 6. Find the maximum and minimum driver ratings for Prime Sedan bookings
SELECT 
	MAX(o.driver_ratings) AS max_rating,
	MIN(o.driver_ratings) AS min_rating
FROM ola o
JOIN vehicle_types v ON o.vehicle_type_id = v.vehicle_type_id
WHERE v.vehicle_type = "Prime Sedan" 
	AND o.driver_ratings != 0.0
	

-- 7. Retrieve all rides where payment was made using UPI
SELECT o.*
FROM ola o
JOIN payment_methods p ON o.payment_method_id = p.payment_method_id
WHERE p.payment_method = "UPI"



-- 8. Find the average customer rating per vehicle type
SELECT v.vehicle_type, ROUND(AVG(o.customer_rating),2) AS avg_customer_rating
FROM ola o
JOIN vehicle_types v ON o.vehicle_type_id = v.vehicle_type_id
GROUP BY v.vehicle_type


-- 9. Calculate the total booking value of rides completed successfully
SELECT 
	SUM(o.booking_value) AS total_successful_value
FROM ola o
JOIN booking_status b ON o.status_id = b.status_id
WHERE b.status = "Success"


-- 10. List all incomplete rides along with the reason
SELECT booking_id, customer_id, incomplete_rides_reason
FROM ola o 
WHERE incomplete_rides = "Yes"

