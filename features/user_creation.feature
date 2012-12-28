Feature: User creation

Scenario: I can create a user
    Given I apply for a new user with mobile number "12345678" and password "Test1234"
    And I check that a challenge has been created in the database
    Then I can verify the user
    And I can contribute to the crowd database on an existing product

Scenario: I cannot verify user with incorrect SMS challenge
    Given I apply for a new user with mobile number "22345678" and password "Test1234"
    And I check that a challenge has been created in the database
    Then I cannot verify the user with incorrect challenge

Scenario: I cannot create a user with an existing mobile number
    Given there is already a user with mobile number "87654321"
    Then I cannot apply for a new user with that mobile number

Scenario: I cannot contribute to the crowd database if not verified
    Given I apply for a new user with mobile number "32345678" and password "Test1234"
    And I check that a challenge has been created in the database
    Then I can contribute to the crowd database on an existing product
