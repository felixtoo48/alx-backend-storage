-- script that creates a stored procedure AddBonus
-- that adds a new correction for a student.

DELIMITER //

CREATE PROCEDURE AddBonus(
    IN in_user_id INT,
    IN in_project_name VARCHAR(255),
    IN in_score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if the project exists, create it if not
    SELECT id INTO project_id FROM projects WHERE name = in_project_name;

    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (in_project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Add the correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (in_user_id, project_id, in_score);

    -- Update the user's average_score
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE user_id = in_user_id
    )
    WHERE id = in_user_id;
END;
//

DELIMITER ;

