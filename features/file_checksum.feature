Feature: Check a file against a checksum
  Scenario Outline: Check a file against a checksum
    Given a file with path <file_path>
    And a checksum <checksum> of type <checksum_type>
    When we validate the contents of the file against the checksum
    Then the validation will return <status>
    And a message matching "<status_message_re>"

  Examples: MD5 Successes
    | file_path                     | checksum_type | status | status_message_re  | checksum                         |
    | tests/data/test_text_file.txt | md5           | True   | Success            | 675c9d875973335dcdbb51bedd6e5ef5 |
    | tests/data/test_binary_file   | md5           | True   | Success            | bacfc108148ce83e4c05d4c5b4f969e2 |

  Examples: SHA256 Successes
    | file_path                     | checksum_type | status | status_message_re  | checksum                                                         |
    | tests/data/test_text_file.txt | sha256        | True   | Success            | c364b31ba54903fb2c9ae4ab4ed3d9941b49b4185f6579c5a5959bbd77ddbde6 |
    | tests/data/test_binary_file   | sha256        | True   | Success            | 71f9ebf3b491fb844934350e203ba31cd64d86a3dffdbe3aa5444df0d0b6d5a0 |

  Examples: MD5 Failures
    | file_path                     | checksum_type | status | status_message_re                                     | checksum                         |
    | tests/data/test_text_file.txt | md5           | False  | Computed checksum .*? does not match .*? for file .*? | aaa9d875973335dcdbb51bedd6e5ef5  |
    | tests/data/test_binary_file   | md5           | False  | Computed checksum .*? does not match .*? for file .*? | aaafc108148ce83e4c05d4c5b4f969e2 |
