from mstrio.utils.error_handlers import ErrorHandler


@ErrorHandler(err_msg='Error loading dataset {id} Check dataset ID')
def dataset_definition(connection, id, fields=None, whitelist=None):
    """Get the definition of a dataset.

    Args:
        connection (object): MicroStrategy connection object returned by
            connection.Connection()`.
        id (str): Identifier of a pre-existing dataset. Used when
            updating a pre-existing dataset.
        fields(list, optional): Specifies object types to be returned. Possible
            values include tables, columns, attributes, and metrics. If no value
            is set, attributes and metrics are returned.
        whitelist(list): list of errors for which we skip printing error
            messages

    Returns:
        HTTP response object returned by the MicroStrategy REST server.
    """
    connection._validate_project_selected()
    return connection.session.get(
        url=f'{connection.base_url}/api/datasets/{id}',
        params={'fields': fields}
    )


@ErrorHandler(err_msg='Error creating new dataset model.')
def create_dataset(connection, body):
    """Create a single-table dataset from external data uploaded to the
    MicroStrategy Intelligence Server.

    Args:
        connection (object): MicroStrategy connection object returned by
            `connection.Connection()`.
        body (str): JSON-formatted definition of the dataset. Generated by
            `utils.formjson()`.

    Returns:
        HTTP response object returned by the MicroStrategy REST server.
    """
    connection._validate_project_selected()
    return connection.session.post(
        url=f'{connection.base_url}/api/datasets',
        json=body
    )


@ErrorHandler(err_msg='Error updating dataset with ID {id}')
def update_dataset(connection, id, table_name, update_policy, body):
    """Update a single-table dataset with external data uploaded to the
    MicroStrategy Intelligence Server.

    Args:
        connection (object): MicroStrategy connection object returned by
            `connection.Connection()`.
        id (str): Identifier of a pre-existing dataset. Used when
            updating a pre-existing dataset.
        table_id (str): Identifier of the table to update within the
            MicroStrategy dataset.
        update_policy (str):  Update operation type: 'Add' (inserts new, unique
            rows), 'Update' (updates data in existing rows and columns),
            'Upsert' (updates existing data and inserts new rows), 'Replace'
            (similar to truncate, replaces the existing data with new data).
        body (str): JSON-formatted definition of the dataset. Generated by
            `utils.formjson()`.

    Returns:
        HTTP response object returned by the MicroStrategy REST server.
    """
    return connection.session.patch(
        url=f'{connection.base_url}/api/datasets/{id}/tables/{table_name}',
        headers={'updatePolicy': update_policy},
        json=body,
    )


@ErrorHandler(err_msg='Error deleting dataset with ID {id}')
def delete_dataset(connection, id):
    """Delete a dataset previously created using the REST API.

    Args:
        connection (object): MicroStrategy connection object returned by
            `connection.Connection()`.
        id (str): Identifier of a pre-existing dataset. Used when
            updating a pre-existing dataset.

    Returns:
        HTTP response object returned by the MicroStrategy REST server.
    """
    return connection.session.delete(url=f'{connection.base_url}/api/objects/{id}?type=3')


@ErrorHandler(err_msg='Error creating new dataset model.')
def create_multitable_dataset(connection, body):
    """Create the definition of a multi-table dataset.

    Args:
        connection (object): MicroStrategy connection object returned by
            `connection.Connection()`.
        body (dict): JSON-formatted payload containing the body of the request.

    Returns:
        HTTP response object returned by the MicroStrategy REST server.
    """
    connection._validate_project_selected()
    return connection.session.post(url=f'{connection.base_url}/api/datasets/models', json=body)


@ErrorHandler(err_msg='Error creating new data upload session.')
def upload_session(connection, id, body):
    """Create a multi-table dataset upload session.

    Args:
        connection (object): MicroStrategy connection object returned by
            `connection.Connection()`.
        id (str): Identifier of a pre-existing dataset. Used when
            updating a pre-existing dataset.
        body (dict): JSON-formatted payload containing the body of the request.

    Returns:
        HTTP response object returned by the MicroStrategy REST server.
    """
    connection._validate_project_selected()
    return connection.session.post(
        url=f'{connection.base_url}/api/datasets/{id}/uploadSessions',
        json=body
    )


@ErrorHandler(err_msg='Error uploading data to dataset {id}')
def upload(connection, id, session_id, body, throw_error=False):
    """Upload data to a multi-table dataset.

    Args:
        connection (object): MicroStrategy connection object returned by
            `connection.Connection()`.
        id (str): Identifier of a pre-existing dataset. Used when
            updating a pre-existing dataset.
        session_id (str): Identifer of the server session used for collecting
            uploaded data.
        body (dict): JSON-formatted payload containing the body of the request.
        throw_error (bool): Flag indicates if the error should be thrown

    Returns:
        HTTP response object returned by the MicroStrategy REST server.
    """
    connection._validate_project_selected()
    return connection.session.put(
        url=f'{connection.base_url}/api/datasets/{id}/uploadSessions/{session_id}',
        json=body
    )


@ErrorHandler(
    err_msg='Error publishing uploaded data for dataset with ID {id} Cancelling publication.')
def publish(connection, id, session_id, throw_error=False):
    """Publish a multi-table dataset.

    Args:
        connection (object): MicroStrategy connection object returned by
            `connection.Connection()`.
        id (str): Identifier of a pre-existing dataset. Used when
            updating a pre-existing dataset.
        session_id (str): Identifer for the server session used for collecting
            uploaded data.
        throw_error (bool): Flag indicates if the error should be thrown

    Returns:
        HTTP response object returned by the MicroStrategy REST server.
    """
    connection._validate_project_selected()
    url = f'{connection.base_url}/api/datasets/{id}/uploadSessions/{session_id}/publish'
    return connection.session.post(url=url)


@ErrorHandler(err_msg='Failed to check dataset {id} publication status.')
def publish_status(connection, id, session_id):
    """Get multi-table dataset publication status.

    Args:
        connection (object): MicroStrategy connection object returned by
            `connection.Connection()`.
        id (str): Identifier of a pre-existing dataset. Used when
            updating a pre-existing dataset.
        session_id (str): Identifer for the server session used for collecting
            uploaded data.

    Returns:
        HTTP response object returned by the MicroStrategy REST server
    """

    url = f'{connection.base_url}/api/datasets/{id}/uploadSessions/{session_id}/publishStatus'
    return connection.session.get(url=url)


@ErrorHandler(err_msg='Failed to cancel the publication of dataset with ID {id}')
def publish_cancel(connection, id, session_id):
    """Delete a multi-table dataset upload session and cancel publication.

    Args:
        connection (object): MicroStrategy connection object returned by
            `connection.Connection()`.
        id (str): Identifier of a pre-existing dataset. Used when
            updating a pre-existing dataset.
        session_id (str): Identifer for the server session used for collecting
            uploaded data.

    Returns:
        HTTP response object returned by the MicroStrategy REST server
    """
    url = f'{connection.base_url}/api/datasets/{id}/uploadSessions/{session_id}'
    return connection.session.delete(url=url)
