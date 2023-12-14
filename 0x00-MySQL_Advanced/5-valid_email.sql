-- SQL script that creates a trigger that resets the attribute valid_email only when the email has been changed

DELIMITER //
CREATE TRIGGER email_change_reset
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
  -- if new email is not equal to old email then reset the attribute valid_email
  IF NEW.email <> OLD.email THEN
    SET NEW.valid_email = 0;
  END IF;
END; //
DELIMITER ;
