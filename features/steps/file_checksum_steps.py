from behave import given, when, then
from checksum import check_file
import re


@given('a file with path {file_path}')
def step_impl(context, file_path):
    context.file = file_path


@given('a checksum {checksum} of type {checksum_type}')
def step_impl(context, checksum, checksum_type):
    context.checksum = checksum
    context.checksum_type = checksum_type


@when('we validate the contents of the file against the checksum')
def step_impl(context):
    status, message = check_file(context.file, context.checksum_type, context.checksum)
    context.status = status
    context.status_message = message


@then('the validation will return {status}')
def step_impl(context, status):
    assert str(context.status) == status


@then('a message matching "{status_message_re}"')
def step_impl(context, status_message_re):
    assert re.match(status_message_re, context.status_message)
