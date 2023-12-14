-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student
DROP PROCEDURE ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
  DECLARE avg_score DECIMAL(5,2);



  -- compute the average score
  SELECT AVG(score) INTO avg_score FROM corrections WHERE user_id = user_id;

  -- store the computed score
  UPDATE users SET average_score = avg_score WHERE id = user_id;

END //
DELIMITER ;
