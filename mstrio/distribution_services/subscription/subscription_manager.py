import logging
from typing import Optional

from packaging import version

from mstrio import config
from mstrio.api import subscriptions as subscriptions_
from mstrio.connection import Connection
from mstrio.utils import helper
from mstrio.utils.version_helper import class_version_handler, method_version_handler

from . import (
    CacheUpdateSubscription,
    EmailSubscription,
    FileSubscription,
    FTPSubscription,
    HistoryListSubscription,
    Subscription,
)
from .content import Content
from .delivery import Delivery

logger = logging.getLogger(__name__)


@method_version_handler('11.2.0203')
def list_subscriptions(
    connection: Connection,
    project_id: str | None = None,
    project_name: str | None = None,
    to_dictionary: bool = False,
    limit: int | None = None,
    **filters,
) -> list["Subscription"] | list[dict]:
    """Get all subscriptions per project as list of Subscription objects or
    dictionaries.

    Optionally filter the subscriptions by specifying filters.
    Specify either `project_id` or `project_name`.
    When `project_id` is provided (not `None`), `project_name` is omitted.

    Args:
        connection(object): MicroStrategy connection object
        project_id: Project ID
        project_name: Project name
        to_dictionary: If True returns a list of subscription dicts,
            otherwise (default) returns a list of subscription objects
        limit: limit the number of elements returned. If `None` (default), all
            objects are returned.
        **filters: Available filter parameters: ['id', 'multiple_contents',
            'name', 'editable', 'allow_delivery_changes'
            'allow_personalization_changes', 'allow_unsubscribe',
            'date_created', 'date_modified', 'owner', 'delivery']
    """
    project_id = helper.get_valid_project_id(
        connection=connection,
        project_id=project_id,
        project_name=project_name,
    )
    chunk_size = (
        1000
        if version.parse(connection.iserver_version) >= version.parse('11.3.0300')
        else 1000000
    )
    msg = 'Error getting subscription list.'
    objects = helper.fetch_objects_async(
        connection=connection,
        api=subscriptions_.list_subscriptions,
        async_api=subscriptions_.list_subscriptions_async,
        limit=limit,
        chunk_size=chunk_size,
        filters=filters,
        error_msg=msg,
        dict_unpack_value="subscriptions",
        project_id=project_id,
    )

    if to_dictionary:
        return objects
    else:
        return [
            dispatch_from_dict(
                source=obj,
                connection=connection,
                project_id=project_id,
            )
            for obj in objects
        ]


DeliveryMode = Delivery.DeliveryMode
subscription_type_from_delivery_mode_dict = {
    DeliveryMode.CACHE: CacheUpdateSubscription,
    DeliveryMode.EMAIL: EmailSubscription,
    DeliveryMode.FILE: FileSubscription,
    DeliveryMode.FTP: FTPSubscription,
    DeliveryMode.HISTORY_LIST: HistoryListSubscription,
}


def get_subscription_type_from_delivery_mode(mode: DeliveryMode):
    """Returns the subscription type of the provided Delivery Mode.

    Args:
        mode: DeliveryMode object of which to get the subscription type"""
    return subscription_type_from_delivery_mode_dict.get(mode, Subscription)


def dispatch_from_dict(source: dict, connection: Connection, project_id: str):
    """Returns the subscription type object from the provided source

    Args:
        source: dictionary of an object to return from the specified
            subscription
        connection: MicroStrategy connection object returned
            by `connection.Connection()`
        project_id: Project ID"""
    delivery_mode = DeliveryMode(source["delivery"]["mode"])
    sub_type = get_subscription_type_from_delivery_mode(delivery_mode)
    return sub_type.from_dict(source, connection, project_id)


@class_version_handler('11.2.0203')
class SubscriptionManager:
    """Manage subscriptions."""

    def __init__(
        self,
        connection: Connection,
        project_id: str | None = None,
        project_name: str | None = None,
    ):
        """Initialize the SubscriptionManager object.
        Specify either `project_id` or `project_name`.
        When `project_id` is provided (not `None`), `project_name` is omitted.

        Args:
            connection: MicroStrategy connection object returned
                by `connection.Connection()`
            project_id: Project ID
            project_name: Project name
        """
        self.connection = connection
        self.project_id = helper.get_valid_project_id(
            connection=connection,
            project_id=project_id,
            project_name=project_name,
        )

    def list_subscriptions(
        self, to_dictionary: bool = False, limit: int | None = None, **filters
    ):
        """Get all subscriptions as list of Subscription objects or
        dictionaries.

        Optionally filter the subscriptions by specifying filters.

        Args:
            to_dictionary: If True returns a list of subscription dicts,
                otherwise returns a list of subscription objects
            limit: limit the number of elements returned. If `None` (default),
                all objects are returned.
            **filters: Available filter parameters: ['id', 'name', 'editable',
                'allowDeliveryChanges', 'allowPersonalizationChanges',
                'allowUnsubscribe', 'dateCreated', 'dateModified', 'owner',
                'schedules', 'contents', 'recipients', 'delivery']
        """
        return list_subscriptions(
            connection=self.connection,
            project_id=self.project_id,
            to_dictionary=to_dictionary,
            limit=limit,
            **filters,
        )

    def delete(
        self, subscriptions: list[Subscription] | list[str], force=False
    ) -> bool:
        """Deletes all passed subscriptions. Returns True if successfully
        removed all subscriptions.

        Args:
            subscriptions: list of subscriptions to be deleted
        """
        subscriptions = (
            subscriptions if isinstance(subscriptions, list) else [subscriptions]
        )
        if not subscriptions and config.verbose:
            logger.info('No subscriptions passed.')
        else:
            temp_subs = []
            for subscription in subscriptions:
                if not isinstance(subscription, Subscription):
                    subscription = Subscription(
                        connection=self.connection,
                        id=subscription,
                        project_id=self.project_id,
                    )
                temp_subs.append(subscription)
            subscriptions = temp_subs
            succeeded = 0
            user_input = 'N'
            if not force:
                to_be_deleted = [
                    f"Subscription '{sub.name}' with ID: '{sub.id}'"
                    for sub in subscriptions
                ]
                print("Found subscriptions:")
                for sub in to_be_deleted:
                    print(sub)
                user_input = input(
                    "Are you sure you want to delete all of them? [Y/N]: "
                )
            if force or user_input == 'Y':
                succeeded = 0
                for subscription in subscriptions:
                    response = subscriptions_.remove_subscription(
                        self.connection,
                        subscription.id,
                        self.project_id,
                        error_msg=(
                            f"Subscription '{subscription.name}' with id "
                            f"'{subscription.id}' could not be deleted."
                        ),
                        exception_type=UserWarning,
                    )
                    if response.ok:
                        succeeded += 1
                        if config.verbose:
                            logger.info(
                                f"Deleted subscription '{subscription.name}' "
                                f"with ID '{subscription.id}'."
                            )

                return succeeded == len(subscriptions)

    def execute(self, subscriptions: list[Subscription] | list[str]):
        """Executes all passed subscriptions.

        Args:
            subscriptions: list of subscriptions to be executed
        """
        if not subscriptions and config.verbose:
            logger.info('No subscriptions passed.')
        else:
            subscriptions = (
                subscriptions if isinstance(subscriptions, list) else [subscriptions]
            )
            for subscription in subscriptions:
                if not isinstance(subscription, Subscription):
                    subscription = Subscription(
                        connection=self.connection,
                        id=subscription,
                        project_id=self.project_id,
                    )
                if subscription.delivery.mode in (
                    'EMAIL',
                    'FILE',
                    'HISTORY_LIST',
                    'FTP',
                ):
                    subscription.execute()
                else:
                    msg = (
                        f"Subscription '{subscription.name}' with ID "
                        f"'{subscription.id}' could not be executed. Delivery mode "
                        f"'{subscription.delivery.mode}' is not supported."
                    )
                    helper.exception_handler(msg, UserWarning)

    @method_version_handler('11.3.0000')
    def available_bursting_attributes(self, content: dict | Content):
        """Get a list of available attributes for bursting feature, for a given
        content.

        Args:
            content: content dictionary or Content object
                (from subscription.content)
        """
        c_id = content['id'] if isinstance(content, dict) else content.id
        c_type = content['type'] if isinstance(content, dict) else content.type

        response = subscriptions_.bursting_attributes(
            self.connection, self.project_id, c_id, c_type.upper()
        )

        if response.ok:
            return response.json()['burstingAttributes']

    @method_version_handler('11.3.0000')
    def available_recipients(
        self,
        content_id: str | None = None,
        content_type: str | None = None,
        content: Optional["Content"] = None,
        delivery_type='EMAIL',
    ) -> list[dict]:
        """List available recipients for a subscription contents.
        Specify either both `content_id` and `content_type` or just `content`
        object.

        Args:
            content_id: ID of the content
            content_type: type of the content
            content: Content object
            delivery_type: The delivery of the subscription, available values
                are: [EMAIL, FILE, PRINTER, HISTORY_LIST, CACHE, MOBILE, FTP].
        """
        if content_id and content_type:
            pass
        elif isinstance(content, Content):
            content_id = content.id
            content_type = content.type
        else:
            helper.exception_handler(
                'Specify either a content ID and type or content object.', ValueError
            )

        body = {
            "contents": [{"id": content_id, "type": content_type}],
        }

        response = subscriptions_.available_recipients(
            self.connection, self.project_id, body, delivery_type
        )

        if response.ok and config.verbose:
            return response.json()['recipients']
