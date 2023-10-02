@Channel
Feature: 渠道管理
  作为一个管理员
  我要新增渠道成功
  以便于创建渠道

  Background: Login Success
    Given 登录成功

  @HappyPath
  Scenario Outline: 新增渠道
    Given 参数{'channel': cib}
    When 新增Channel时
    Then 新增成功
    Examples:
      | 1 | 2 | 3 |
      | 2 | 3 | 4 |

  Scenario: 新增Channel失败
    Given 参数{'channel': cib}
    When 新增Channel时
    Then 新增成功
