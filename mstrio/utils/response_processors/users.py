from mstrio.api import users as users_api
from mstrio.connection import Connection
from mstrio.utils.helper import fetch_objects_async


def get(connection: Connection, id: str):
    """Get user by a specified ID.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user

    Returns:
        dict representing user object
    """
    return users_api.get_user_info(connection=connection, id=id).json()


def get_addresses(connection: Connection, id: str):
    """Get addresses for a specified user.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user

    Returns:
        dict representing user addresses
    """
    return users_api.get_addresses_v2(connection=connection, id=id).json()


def get_security_roles(connection: Connection, id: str):
    """Get security roles for a specified user.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user

    Returns:
        dict representing user security roles
    """
    return users_api.get_user_security_roles(connection=connection, id=id).json()


def get_privileges(connection: Connection, id: str):
    """Get privileges for a specified user.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user

    Returns:
        dict representing user privileges
    """
    return users_api.get_user_privileges(connection=connection, id=id).json()


def update(connection: Connection, id: str, body: dict):
    """Update info for a specified user.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user
        body: body of the request

    Returns:
        dict representing user object
    """
    return users_api.update_user_info(connection=connection, id=id, body=body).json()


def create(connection: Connection, body: dict, username: str):
    """Create a user.

    Args:
        connection: MicroStrategy REST API connection object
        body: body of the request
        username: name of the user, for error purposes only

    Returns:
        dict representing user object
    """
    return users_api.create_user(
        connection=connection, body=body, username=username
    ).json()


def get_all(
    connection: Connection,
    limit: int,
    msg: str,
    name_begins: str,
    abbreviation_begins: str,
    filters,
):
    """Get list of users.

    Args:
        connection: MicroStrategy REST API connection object
        limit: limit of users to list
        msg: optional error message,
        name_begins: optional filter for name beginning with
        abbreviation_begins: optional filter for abbreviation beginning with
        filters: filters

    Returns:
        list of dicts representing users
    """
    return fetch_objects_async(
        connection=connection,
        api=users_api.get_users_info,
        async_api=users_api.get_users_info_async,
        limit=limit,
        chunk_size=1000,
        error_msg=msg,
        name_begins=name_begins,
        abbreviation_begins=abbreviation_begins,
        filters=filters,
    )


def create_address(connection: Connection, id: str, body: dict):
    """Create an email user address.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user
        body: body of the request

    Returns:
    created address dictionary
    """
    return users_api.create_address(connection=connection, id=id, body=body).json()


def create_address_v2(connection: Connection, id: str, body: dict):
    """Create a non-email user address.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user
        body: body of the request

    Returns:
        dict representing user addresses
    """
    return users_api.create_address_v2(connection=connection, id=id, body=body).json()


def update_address(connection: Connection, id: str, address_id: str, body: dict):
    """Update a user address.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user
        address_id: ID of the address
        body: body of the request

    Returns:
        True if successfully updated, False otherwise
    """
    return users_api.update_address_v2(
        connection=connection, id=id, address_id=address_id, body=body
    ).ok


def delete_address(connection: Connection, id: str, address_id: str):
    """Delete a user address.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user
        address_id: ID of the address

    Returns:
        True if successfully deleted, False otherwise
    """
    return users_api.delete_address(
        connection=connection, id=id, address_id=address_id
    ).ok


def get_security_filters(connection: Connection, id: str, projects: str | list[str]):
    """Get security filters for a user.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the user
        projects: IDs of the projects

    Returns:
        list of user security filters
    """
    return users_api.get_security_filters(
        connection=connection, id=id, projects=projects
    ).json()
