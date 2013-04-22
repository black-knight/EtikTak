Feature: User creation

Scenario: I can create a user with password
    Given I apply for a new user with mobile number "10000000" and password "Test1234"
    And I check that a challenge has been created in the database
    And I simulate that an SMS has been successfully sent
    Then I can verify the user
    And I can contribute to the crowd database on an existing product

Scenario: I can create a user with client UID
    Given I apply for a new user with mobile number "10000001" and UID "ABCD1234"
    And I check that a challenge has been created in the database
    And I simulate that an SMS has been successfully sent
    Then I can verify the user
    And I can contribute to the crowd database on an existing product

Scenario: I cannot verify user with incorrect SMS challenge
    Given I apply for a new user with mobile number "10000002" and password "Test1234"
    And I check that a challenge has been created in the database
    And I simulate that an SMS has been successfully sent
    Then I cannot verify the user with incorrect challenge

Scenario: I cannot create a user with an existing mobile number
    Given there is already a user with mobile number "10000003"
    Then I cannot apply for a new user with that mobile number
