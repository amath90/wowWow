Feature: My first behave feature

  Scenario: Find wowair.us page
    Given I have google.pl displayed in Google Chrome
    When I type wowair in search bar
    Then I have search results displayed and clicked link