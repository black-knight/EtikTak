Feature: Product scan clustering

Scenario: Product scans will be clustered correctly
    Given I simulate that a user scans "100" times in a radius of "100" meters
    And I run the clustering algorithm
    Then the product scans have been clustered correctly
