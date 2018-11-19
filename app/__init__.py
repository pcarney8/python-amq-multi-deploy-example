import json
import logging
import os

from logmatic import JsonFormatter
from proton import Message
from proton.handlers import MessagingHandler

import checksum


def create_messenger(broker_url, event_source, event_destination, file_type):
    return Messenger(broker_url, event_source, event_destination, file_type)


def _copy_attr(original, new, name, default=None):
    if hasattr(original, name):
        value = getattr(original, name)
        if value:
            setattr(new, name, value)
        else:
            setattr(new, name, default)


def _construct_failure_message(original_message, failure_type, from_queue):
    message = Message(original_message.body)
    _copy_attr(original_message, message, "properties", {})
    message.priority = original_message.priority
    message.properties["failure_type"] = failure_type
    message.properties["from_queue"] = from_queue
    message.address = "failures"
    return message


class Messenger(MessagingHandler):
    def __init__(self, broker_url, event_source, event_destination, file_type):
        super(Messenger, self).__init__()
        self.metrics_logger = self.init_logger()
        self.broker_url = broker_url
        self.event_source = event_source
        self.event_destination = event_destination
        self.file_type = file_type

    def init_logger(self):
        logger = logging.getLogger("granule_validator")
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def on_start(self, event):
        conn = event.container.connect(self.broker_url)
        event.container.create_receiver(conn, self.event_source)
        self.sender = event.container.create_sender(conn, None)

    def on_link_opened(self, event):
        print("We're ready to rock.")

    def on_message(self, event):
        self.metrics_logger.info("STAGE STARTED")

        granule = json.loads(event.message.body)

        self.metrics_logger.info("Submission Id: {}: START Validating checksum for {} files".format(
                                 granule['submission_id'], self.file_type))

        checksum_valid, status_messages = checksum.check_granule_files_of_type(granule, 'METADATA')

        self.metrics_logger.info("Submission Id: {}: END Validating checksum for {} files".format(
                                 granule['submission_id'], self.file_type))

        if checksum_valid:
            self.metrics_logger.info("Submission Id: {}: Checksum validation passed for {} files".format(
                                     granule['submission_id'], self.file_type))
            message = Message(json.dumps(granule))
            message.priority = event.message.priority
            message.address = self.event_destination
            self.sender.send(message)
        else:
            self.metrics_logger.info("Submission Id: {}: Checksum validation failed: {}".format(
                                     granule['submission_id'],
                                     json.dumps(status_messages)))
            self.sender.send(_construct_failure_message(event.message,
                                                        '{}_CHECKSUM_VALIDATION_FAILED'.format(self.file_type),
                                                        self.event_source))

        self.metrics_logger.info("STAGE ENDED")
