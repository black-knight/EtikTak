Feature: User creation

Scenario: I can create a user
    Given I apply for a new user with mobile number "12345678" and password "Test1234"
    And I simulate an SMS with pincode "ABC123"
    Then I can register the user
    And I can login

Scenario: I cannot create a user with an existing mobile number
    Given there is already a user with mobile number "12345678"
    Then I cannot apply for a new user with that mobile number
