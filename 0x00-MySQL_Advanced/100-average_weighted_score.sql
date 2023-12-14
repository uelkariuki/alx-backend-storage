-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DROP PROCEDURE ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
  DECLARE total_weight FLOAT;
  DECLARE weighted_sum_score FLOAT;

  SELECT SUM(projects.weight) INTO total_weight
  FROM corrections
  JOIN projects ON corrections.project_id = projects.id
  WHERE corrections.user_id = user_id;

  SELECT SUM(corrections.score * projects.weight) INTO weighted_sum_score
  FROM corrections
  JOIN projects ON corrections.project_id = projects.id
  WHERE corrections.user_id = user_id;

  UPDATE users
  SET average_score = weighted_sum_score / total_weight
  WHERE id = user_id;

END //
DELIMITER ;
