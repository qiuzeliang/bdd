@Business
Feature: 业务管理
  Only blog owners can post to a blog, except administrators,
  who can post to all blogs.

  Background: Login
    Given a global administrator named "Greg"
    And a blog named "Greg's anti-tax rants"
    And a customer named "Dr. Bill"
    And a blog named "Expensive Therapy" owned by "Dr. Bill"

  @HappyPath @Business
  Scenario: 新增业务类型
    Given I am logged in as Dr. Bill
    When I try to post to "Expensive Therapy"
    Then I should see "Your article was published."

  Scenario: B
    Given I am logged in as Dr. Bill
    When I try to post to "Greg's anti-tax rants"
    Then I should see "Hey! That's not your blog!"

  Scenario: C
    Given I am logged in as Greg
    When I try to post to "Expensive Therapy"
    Then I should see "Your article was published."

  Scenario Outline: D
    Given I am logged in as Greg
    When I try to post to "Expensive Therapy"
    Then I should see "Your article was published."
    Examples: parameter
      | 1 | 2 | 3 |
      | 2 | 3 | 4 |

  Scenario Outline: E
    Given I am logged in as Greg
    When I try to post to "Expensive Therapy"
    Then I should see "Your article was published."
    Examples: parameter
      | 1 | 2 | 3 |
      | 2 | 3 | 4 |
