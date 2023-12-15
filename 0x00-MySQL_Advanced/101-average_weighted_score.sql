-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students

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



DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE user_id INT;
  DECLARE cur CURSOR FOR SELECT id FROM users;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;


  OPEN cur;

  read_loop: LOOP
    FETCH cur INTO user_id;

	IF done THEN
	  LEAVE read_loop;
	END IF;

	CALL ComputeAverageWeightedScoreForUser(user_id);
  END LOOP;

  CLOSE cur;

END //
DELIMITER ;

