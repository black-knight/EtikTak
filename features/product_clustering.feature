Feature: Product scan clustering

Scenario: Product scans will be clustered correctly
    Given I simulate that a user has scanned products in three supermarkets
    And I start the clustering algorithm
    Then the product scans have been clustered in three clusters
