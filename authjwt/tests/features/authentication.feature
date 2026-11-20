@backend
Feature: JWT authentication integration

  Scenario: Enabling the plugin activates JWT support in the REST API
    Then Django REST Framework accepts JWT bearer authentication
    And CORS middleware is enabled
