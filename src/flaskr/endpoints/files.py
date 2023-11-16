from pathlib import Path

from flask import stream_with_context, Response, request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from src import app_data
from src.utils.http_error_handling import error_to_http_response, FileAlreadyExistsError, FileNotProvidedError, \
    FilePathInvalidError

CHUNK_SIZE = 8192


def read_file_chunks(path):
    with open(path, 'rb') as fd:
        while True:
            buf = fd.read(CHUNK_SIZE)
            if buf:
                yield buf
            else:
                break


def get_absolute_file_path(file_path) -> Path:
    # Make sure we stay inside the data directory
    if '..' in file_path or '~' in file_path:
        raise FilePathInvalidError(f'Invalid file path: "{file_path}"')

    # Make sure the file path is valid
    if secure_filename(file_path) != file_path:
        raise FilePathInvalidError(f'Invalid file path: "{file_path}"')

    return (app_data.conf['root_path'] / file_path).resolve()


class EPFiles(Resource):

    @error_to_http_response
    def get(self, file_path):
        """Download a file

        :param file_path: The path to the file relative to the data directory.
        """
        absolute_file_path = app_data.conf['root_path'] / file_path  # type: Path

        if not absolute_file_path.exists():
            raise FileNotFoundError(f'File does not exist: "{file_path}"')

        return Response(
            stream_with_context(read_file_chunks(absolute_file_path)),
            headers={
                'Content-Disposition': f'attachment; filename={absolute_file_path.name}'
            }
        )

    @error_to_http_response
    def put(self, file_path):
        """Upload a file. The file must not exist yet.

        :param file_path: The path to the file relative to the data directory.
        """
        absolute_file_path = get_absolute_file_path(file_path)

        if absolute_file_path.exists():
            raise FileAlreadyExistsError(f'File already exists: "{file_path}"')

        if 'file' not in request.files:
            raise FileNotProvidedError('No file part')

        file = request.files['file']
        if file.filename == '':
            raise FileNotProvidedError('No selected file')

        if file:
            file.save(absolute_file_path)

        return {'message': 'File saved'}, 200

    @error_to_http_response
    def post(self, file_path):
        """Upload a file. If the file already exists, it will be overwritten.

        :param file_path: The path to the file relative to the data directory.
        """
        absolute_file_path = get_absolute_file_path(file_path)

        if 'file' not in request.files:
            raise FileNotProvidedError('No file part')

        file = request.files['file']
        if file.filename == '':
            raise FileNotProvidedError('No selected file')

        if file:
            file.save(absolute_file_path)

        return {'message': 'File saved'}, 200

    @error_to_http_response
    def delete(self, file_path):
        """Delete a file

        :param file_path: The path to the file relative to the data directory.
        """
        absolute_file_path = get_absolute_file_path(file_path)

        if not absolute_file_path.exists():
            return {'message': 'File does not exist'}, 200  # Status code 200 because the file is already gone

        absolute_file_path.unlink()

        return {'message': 'File deleted'}, 200
