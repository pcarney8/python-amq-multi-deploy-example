from behave import given, when, then
from checksum import check_granule_files_of_type
import json

@given("a JSON message for a granule")
def step_impl(context):
    context.granule = json.loads(context.text)


@when("we validate the {file_type} files in the granule against their checksums")
def step_impl(context, file_type):
    context.granule_status, context.file_statuses = check_granule_files_of_type(context.granule, file_type)


@then("the granule validation will return a status of True")
def step_impl(context):
    assert context.granule_status


@then('a message for {file} of "Success"')
def step_impl(context, file):
    assert file in context.file_statuses
    assert context.file_statuses[file] == (True, "Success")