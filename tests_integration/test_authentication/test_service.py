import logging

logger = logging.getLogger(__name__)


def test_authenticate(auth_service):
    auth_response = auth_service.authenticate()
    assert auth_response is not None
    logger.info("Authenticated successfully:\n%s", auth_response.model_dump_json(indent=4))


