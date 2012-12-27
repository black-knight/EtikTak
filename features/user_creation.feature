Feature: User creation

Scenario: I can create a user
    Given I apply for a new user with mobile number "12345678" and password "Test1234"
    And I check that a challenge has been created in the database
    Then I can verify the user
    And I can login

Scenario: I cannot create a user with an existing mobile number
    Given there is already a user with mobile number "87654321"
    Then I cannot apply for a new user with that mobile number
