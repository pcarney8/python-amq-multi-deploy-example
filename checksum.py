import hashlib


def check_granule_files_of_type(granule: dict, file_type: str):
    granule_status = True
    file_status = {}
    for file in [f for f in granule['files'] if f['type'] == file_type]:
        status = check_file(file['id'], file['checksum']['type'], file['checksum']['hash'])
        file_status[file['id']] = status
        if not status[0]:
            granule_status = False
    return granule_status, file_status


def check_file(file_path: str, checksum_type: str, checksum_to_check: str) -> (bool, str):
    """
    Computes the checksum of a given file and checks it against the given value file_path

    :param file_path: The path to the file to be checked
    :param checksum_type: The checksum algorithm (MD5, SHA256, etc).  Must be an algorithm available in hashlib
    :param checksum_to_check: The given checksum value to check against
    :return: (True, "Success") if the checksum of the value validates against the given checksum,
    (False, error_message) if checksum doesn't match, or
     checksum_type is invalid, or if file does not exist,
    with an error message describing the problem
    """
    try:
        algorithm = getattr(hashlib, checksum_type.lower())
        computed_hash = algorithm()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b''):
                computed_hash.update(chunk)

        if computed_hash.hexdigest().lower() == checksum_to_check.lower():
            return True, "Success"
        else:
            return False, "Computed checksum {} does not match {} for file {}".format(
                computed_hash.hexdigest().lower(),
                checksum_to_check.lower(),
                file_path
            )
    except AttributeError:
        return False, "Checksum algorithm {} not available".format(checksum_type)
    except FileNotFoundError:
        return False, "File {} not found".format(file_path)
