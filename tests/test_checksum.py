from checksum import check_file
import pytest


@pytest.mark.parametrize(
    "file_path,checksum_type,checksum_to_check,expected_result", [
        # md5 success
        ("tests/data/test_text_file.txt", "md5", "675c9d875973335dcdbb51bedd6e5ef5", (True, "Success")),
        ("tests/data/test_binary_file", "md5", "bacfc108148ce83e4c05d4c5b4f969e2", (True, "Success")),

        # MD5
        ("tests/data/test_text_file.txt", "MD5", "675c9d875973335dcdbb51bedd6e5ef5", (True, "Success")),
        ("tests/data/test_binary_file", "MD5", "bacfc108148ce83e4c05d4c5b4f969e2", (True, "Success")),

        # md5 value uppercase
        ("tests/data/test_text_file.txt", "md5", "675C9D875973335DCDBB51BEDD6E5EF5", (True, "Success")),
        ("tests/data/test_binary_file", "md5", "BACFC108148CE83E4C05D4C5B4F969E2", (True, "Success")),

        # sha256
        ("tests/data/test_text_file.txt", "sha256", "c364b31ba54903fb2c9ae4ab4ed3d9941b49b4185f6579c5a5959bbd77ddbde6",
            (True, "Success")),
        ("tests/data/test_binary_file", "sha256", "71f9ebf3b491fb844934350e203ba31cd64d86a3dffdbe3aa5444df0d0b6d5a0",
            (True, "Success")),

        # SHA256
        ("tests/data/test_text_file.txt", "SHA256", "c364b31ba54903fb2c9ae4ab4ed3d9941b49b4185f6579c5a5959bbd77ddbde6",
            (True, "Success")),
        ("tests/data/test_binary_file", "SHA256", "71f9ebf3b491fb844934350e203ba31cd64d86a3dffdbe3aa5444df0d0b6d5a0",
            (True, "Success")),

        # sha256 value uppercase
        ("tests/data/test_text_file.txt", "sha256", "C364B31BA54903FB2C9AE4AB4ED3D9941B49B4185F6579C5A5959BBD77DDBDE6",
            (True, "Success")),
        ("tests/data/test_binary_file", "sha256", "71F9EBF3B491FB844934350E203BA31CD64D86A3DFFDBE3AA5444DF0D0B6D5A0",
            (True, "Success")),

        # input md5 is incorrect
        ("tests/data/test_text_file.txt", "md5", "775c9d875973335dcdbb51bedd6e5ef5",
            (False, "Computed checksum 675c9d875973335dcdbb51bedd6e5ef5 does not match 775c9d875973335dcdbb51bedd6e5ef5"
                    " for file tests/data/test_text_file.txt")),
        ("tests/data/test_binary_file", "md5", "3acfc108148ce83e4c05d4c5b4f969e2",
            (False, "Computed checksum bacfc108148ce83e4c05d4c5b4f969e2 does not match 3acfc108148ce83e4c05d4c5b4f969e2"
                    " for file tests/data/test_binary_file",)),

        # input sha256 is incorrect
        ("tests/data/test_text_file.txt", "sha256", "0364b31ba54903fb2c9ae4ab4ed3d9941b49b4185f6579c5a5959bbd77ddbde6",
            (False, "Computed checksum c364b31ba54903fb2c9ae4ab4ed3d9941b49b4185f6579c5a5959bbd77ddbde6 does not "
                    "match 0364b31ba54903fb2c9ae4ab4ed3d9941b49b4185f6579c5a5959bbd77ddbde6 for file "
                    "tests/data/test_text_file.txt")),
        ("tests/data/test_binary_file", "sha256", "01f9ebf3b491fb844934350e203ba31cd64d86a3dffdbe3aa5444df0d0b6d5a0",
            (False, "Computed checksum 71f9ebf3b491fb844934350e203ba31cd64d86a3dffdbe3aa5444df0d0b6d5a0 does not "
                    "match 01f9ebf3b491fb844934350e203ba31cd64d86a3dffdbe3aa5444df0d0b6d5a0 for file "
                    "tests/data/test_binary_file")),

        # missing file
        ("tests/data/doesnotexist", "md5", "775c9d875973335dcdbb51bedd6e5ef5",
            (False, "File tests/data/doesnotexist not found")),

        # incorrect algorithm
        ("tests/data/test_text_file.txt", "bad_algorithm", "675c9d875973335dcdbb51bedd6e5ef5",
         ( False, "Checksum algorithm bad_algorithm not available")),
    ]
)
def test_check_md5(file_path, checksum_type, checksum_to_check, expected_result):
    assert check_file(file_path, checksum_type, checksum_to_check) == expected_result


def test_large_file(tmp_path):
    file = tmp_path / "large_file"
    file.write_text('a' * (2 * 1024 * 1024 + 1))
    assert check_file(file, 'md5', 'f0a5d0aa0b425bf89a75a696a7c80347') == (True, 'Success')

