Feature: Check SCIENCE or METADATA files in a granule
  Scenario Outline:
    Given a JSON message for a granule
      """
      {
          "submission_id": 123,
          "files": [
              {
                  "id": "tests/data/test_binary_file",
                  "checksum": {
                      "type": "MD5",
                      "hash": "bacfc108148ce83e4c05d4c5b4f969e2"
                  },
                  "stored": false,
                  "type": "SCIENCE"
              },
              {
                  "id": "tests/data/test_text_file.txt",
                  "checksum": {
                      "type": "MD5",
                      "hash": "675c9d875973335dcdbb51bedd6e5ef5"
                  },
                  "stored": false,
                  "type": "METADATA"
              }
          ]
      }
      """
    When we validate the <file_type> files in the granule against their checksums
    Then the granule validation will return a status of True
    And a message for <file> of "Success"
    Examples:
      | file_type | file                          |
      | SCIENCE   | tests/data/test_binary_file   |
      | METADATA  | tests/data/test_text_file.txt |
