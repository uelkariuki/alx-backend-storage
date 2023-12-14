-- SQL script that creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0

DELIMITER //
CREATE FUNCTION SafeDiv(a INTEGER, b INTEGER) RETURNS FLOAT
BEGIN
   DECLARE return_value FLOAT;
   SET return_value = IF (b = 0, 0 ,a / b);
   RETURN return_value;
END //
DELIMITER ;




