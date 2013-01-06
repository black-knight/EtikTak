Feature: User verification

Scenario: I can verify a user
    Given I apply for a new user with mobile number "20000000" and password "Test1234"
    And I check that a challenge has been created in the database
    And I simulate that an SMS has been successfully sent
    Then I can verify the user

Scenario: I cannot contribute to the crowd database if not verified
    Given I apply for a new user with mobile number "20000001" and password "Test1234"
    And I check that a challenge has been created in the database
    And I simulate that an SMS has been successfully sent
    Then I cannot contribute to the crowd database on an existing product

Scenario: I cannot contribute to the crowd database with non-existant user
    I cannot contribute to the crowd database on an existing product with non-existant user
